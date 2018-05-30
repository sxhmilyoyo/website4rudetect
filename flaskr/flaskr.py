import ast
import csv
import click
import traceback
from flask import flash
from flask import Flask
from flask import g
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_bootstrap import Bootstrap
# from flask_paginate import get_page_parameter
from flask_paginate import Pagination
from flaskr.database import db_session
from flaskr.database import init_db
from flaskr.database import reinit_db
from flaskr.forms import LoginForm
from flaskr.forms import RegisterForm
from flaskr.models import Event
from flaskr.models import Rumor
from flaskr.models import User
from flaskr.models import Opinion
from flaskr.models import Event_Cluster
from flaskr.models import Statement
from flaskr.models import Snippet
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import make_response
from flask_uploads import UploadSet, TEXT, configure_uploads, UploadNotAllowed
from flaskr.config import UPLOADED_DATA_DIR, PROCESS_DATA_DIR
from flaskr.loadData import add_data
import json
import os
from sqlalchemy import exists
from sqlalchemy import and_
from sqlalchemy import desc
import shutil
from werkzeug.utils import secure_filename

import sys
sys.path.append("..")
# import RuDetect27.main


PER_PAGE = 5
SUPPORT_TWEETS = []
OPPOSE_TWEETS = []
SUPPORT_SNIPPETS = []
OPPOSE_SNIPPETS = []

UPLOADS_DEFAULT_DEST = str(UPLOADED_DATA_DIR)
UPLOADS_DEFAULT_URL = 'http://localhost:5000/data/'
UPLOADED_FILES_DEST = str(UPLOADED_DATA_DIR)
UPLOADED_FILES_URL = 'http://localhost:5000/data/'
# It allow TEXT, DOCUMENTS, DATA, and IMAGES extentions in flask-upload
# for now only accept TEXT

app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask.db'),
    SECRET_KEY='test',
    USERNAME='test',
    PASSWORD='test'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# It allow TEXT, DOCUMENTS, DATA, and IMAGES extentions in flask-upload
# for now only accept TEXT
docs = UploadSet('docs', extensions=('pkl'))
configure_uploads(app, docs)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.cli.command('initdb')
def initd_command():
    """Initialize the databse."""
    init_db()
    print("Initialized the databse.")


@app.cli.command('reinitdb')
def reinitd_command():
    """Reconstruct data before first request for testing."""
    reinit_db()
    print("Re-Initialized the databse.")


@app.cli.command('addevent')
@click.option('--event')
def addevent_command(event):
    """Add event data to DB."""
    try:
        db_session.remove()
        add_data(event)
    except Exception as e:
        print(e)
        traceback.print_exc()
        db_session.rollback()
        db_session.remove()
    print("Load event{} to DB.".format(event))


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Close the database again at the end of the request."""
    db_session.remove()


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login."""
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('show_rumors', current_user=current_user))
            else:
                error = "Invalid password"
        else:
            error = "Invalid username"
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    """Logout."""
    logout_user()
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        print('test')
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

        return redirect(url_for('login', error="Signup successfully"))
    return render_template('signup.html', form=form)


@app.route('/')
def show_rumors():
    """Show the rumors entries."""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    events = Event.query.all()
    print(current_user.is_authenticated)
    print(current_user.username)
    # events = [event for event in os.listdir("../data") if os.path.isdir('../data/'+event)]
    res = []
    for event in events:
        # head
        head = "#" + event.name
        # topics
        clusters = sorted(set([c.cluster_name for c in event.clusters]))
        statements = {}
        topics = {}
        for cluster in clusters:
            # with open('../data/'+event.name+'/'+cluster+'/targets.json') as fp:
            #     topic = json.load(fp)
            statementsDB = getStatementsFromDB(event.name, cluster)
            # event_cluster = Event_Cluster.query.filter_by(
            #     event_name=event.name, cluster_name=cluster).first()
            statements_cluster = [(statement.id, statement.content) for statement in statementsDB]
            topics_cluster = list(set([statement.target for statement in statementsDB]))
            print(event, cluster, statements)
            statements[cluster] = statements_cluster
            topics[cluster] = topics_cluster
        res.append({'head': head, 'statements': statements, 'topics': topics})
    print(res)
    # test = [{'head': 'head1', 'topics': [['test1', 'test1', 'test1'], ['test2', 'test2', 'test2']]},
    #         {'head': 'head1', 'topics': [['test1', 'test1', 'test1'], ['test2', 'test2', 'test2']]},
    #         {'head': 'head1', 'topics': [['test1', 'test1', 'test1'], ['test2', 'test2', 'test2']]}
    #         ]
    return render_template('show_rumors.html', items=res, events=events, current_user=current_user)


def getTweets(event, cluster):
    """Get the details for event type."""
    details = []
    with open(os.path.join("../data", event, cluster, "corpus.csv")) as fp:
        reader = csv.reader(fp, delimiter='\t')
        next(reader)
        for r in reader:
            details.append(r)
    return details[:len(details) // 2], details[len(details) // 2:]


# @app.route('/abstract/<event>/<cluster>/<topics>')
# @app.route('/abstract/<event>/<cluster>/<topics>/<int:per_page>')
# def getTweets4Statement(event, cluster, topics, per_page=5):
@app.route('/abstract/<statement_id>/<head>/<topics>')
@app.route('/abstract/<statement_id>/<head>/<topics>/<int:per_page>')
def getTweets4Statement(statement_id, head, topics, per_page=5):
    """Get the details for event gabapentin."""
    global PER_PAGE
    global SUPPORT_TWEETS
    global OPPOSE_TWEETS
    global SUPPORT_TWEETS
    global OPPOSE_TWEETS
    # session['event'] = event
    # session['per_page'] = per_page
    PER_PAGE = per_page
    print(PER_PAGE)
    # print(session['per_page'])
    statement = Statement.query.filter_by(id=statement_id).first().content

    support_tweets, oppose_tweets = getSupportOpposeTweetsFromDB(statement_id)
    SUPPORT_TWEETS = support_tweets[:]
    OPPOSE_TWEETS = oppose_tweets[:]
    tweets = getTweetsFromDB(statement_id)
    print(len(SUPPORT_TWEETS))

    support_snippets, oppose_snippets = getSupportOpposeSnippetsFromDB(statement_id)
    SUPPORT_SNIPPETS = support_snippets[:]
    OPPOSE_SNIPPETS = oppose_snippets[:]
    snippets = getSnippetsFromDB(statement_id)

    topics = ast.literal_eval(topics)
    return render_template('abstract.html', statement_id=statement_id, statement=statement, topics=topics, head=head,
                           oppose_tweets=oppose_tweets[:PER_PAGE], support_tweets=support_tweets[:PER_PAGE], tweets=tweets,
                           chart_support_tweets=len(SUPPORT_TWEETS), chart_oppose_tweets=len(OPPOSE_TWEETS),
                           oppose_snippets=oppose_snippets[:PER_PAGE], support_snippets=support_snippets[:PER_PAGE], snippets=snippets,
                           chart_support_snippets=len(SUPPORT_SNIPPETS), chart_oppose_snippets=len(OPPOSE_SNIPPETS))


def get_tweets_for_page(data, page, per_page, count):
    """Get tweets for each page for pagination."""
    page -= 1
    if 5 * page + per_page < count:
        return data[per_page * page:per_page * page + per_page]
    else:
        return data[per_page * page:]


@app.route('/detail/<statement_id>/<head>/<topics>/<attitude>', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/detail/<statement_id>/<head>/<topics>/<attitude>/<int:page>', methods=['GET', 'POST'])
def show_tweets(statement_id, head, topics, attitude, page):
    """Show all the tweets with attitude in pagination way."""
    per_page = 10
    # pro, con = getTweets(event, cluster)
    statement = Statement.query.filter_by(id=statement_id).first().content    
    support, oppose = getSupportOpposeTweetsFromDB(statement_id)
    # print(getTweets('gabapentin'))
    if attitude == 'support':
        count = len(support)
        tweets = get_tweets_for_page(support, page, per_page, count)
    elif attitude == 'oppose':
        count = len(oppose)
        tweets = get_tweets_for_page(oppose, page, per_page, count)
    pagination = Pagination(page=page, total=count, per_page=per_page,
                            search=False, css_framework='bootstrap4')
    topics = ast.literal_eval(topics)
    return render_template('detail.html',
                           head=head,
                           data=tweets,
                           pagination=pagination,
                           statement_id=statement_id,
                           statement=statement,
                           attitude=attitude,
                           topics=topics,
                           offset=(page-1)*per_page
                           )


@app.route('/loadmore')
def load_more():
    """Load more data and return jsonified data to js function."""
    # if session.get('event') and session.get('per_page'):
    # print(session.get('per_page'))
    global PER_PAGE
    global SUPPORT_TWEETS
    global OPPOSE_TWEETS
    global SUPPORT_TWEETS
    global OPPOSE_TWEETS
    # print(PER_PAGE)
    # per_page = session.get('per_page')
    # pro_res = session['pro'][PER_PAGE:PER_PAGE+5]
    # con_res = session['con'][PER_PAGE:PER_PAGE+5]
    # session['per_page'] = per_page + 5
    idx = PER_PAGE
    augument = PER_PAGE + 5
    if augument > len(SUPPORT_TWEETS):
        augument = len(SUPPORT_TWEETS)
    support_res = SUPPORT_TWEETS[PER_PAGE:augument]
    oppose_res = OPPOSE_TWEETS[PER_PAGE:augument]
    support_res = SUPPORT_TWEETS[PER_PAGE:augument]
    oppose_res = OPPOSE_TWEETS[PER_PAGE:augument]
    PER_PAGE = augument
    print("=" * 100)
    print(PER_PAGE)
    return jsonify(support=support_res, oppose=oppose_res, idx=idx)


@app.route('/addopinion/<tweet_id>/<flag>/<opinion_value>')
def add_opinion(tweet_id, flag, opinion_value):
    """Add user's opinion to rumor."""
    print("tweet_id", tweet_id)
    print("opinion", opinion_value)
    print("user_id", current_user.id)
    rumor = Rumor.query.filter_by(tweet_id=tweet_id).first()
    rumor_id = rumor.id
    # check if the record existance
    existed = db_session.query(exists().where(and_(
        Opinion.flag == flag,
        Opinion.stance == opinion_value,
        Opinion.rumor_id == rumor_id,
        Opinion.user_name == current_user.username
    ))).scalar()
    if existed:
        # record existed
        print("record existed")
        print("Opinion", Opinion.query.all())
        r = make_response('existed', 200)
        return r
    else:
        # check if record updation
        print("checking update")
        q = db_session.query(Opinion).filter(and_(
            Opinion.flag == flag,
            Opinion.rumor_id == rumor_id,
            Opinion.user_name == current_user.username
        ))
        if q.all():
            # update record
            print("updating record...")
            q.update({"stance": opinion_value})
            db_session.commit()
            r = make_response('updated', 200)
            return r
    # insert new record
    print("insert record...")
    opinion = Opinion(flag=flag, stance=opinion_value)
    opinion.rumor = rumor
    current_user.rumors.append(opinion)
    db_session.add(current_user)
    db_session.commit()
    print("Opinion", Opinion.query.all())
    r = make_response('inserted', 200)
    return r


# def getWholeTweets(event, cluster):
#     """Get whole tweets of an event."""
#     tweets = [(r.date, r.tweet_id, r.tweet) for r in db_session.query(
#         Rumor).filter(and_(Rumor.event_name == event, Rumor.cluster_name == cluster)).order_by(Rumor.date).all()]
#     return tweets


@app.route('/label/<event>/<cluster>')
def label_tweets(event, cluster):
    """Show tweets of an event to label."""
    tweets = getTweetsFromDB(event, cluster)
    return render_template('label_data.html', tweets=tweets)


def getTweetsFromDB(statement_id, stance=None, order='asc'):
    """Get tweets from database."""
    if stance:
        if order == 'asc':
            res = [(str(r.date), r.tweet_id, r.tweet)
                   for r in Rumor.query.filter_by(statement_id=statement_id,
                                                  stance=stance
                                                  ).order_by(Rumor.date).all()
                   ]
        elif order == 'desc':
            res = [(str(r.date), r.tweet_id, r.tweet)
                   for r in Rumor.query.filter_by(statement_id=statement_id,
                                                  stance=stance
                                                  ).order_by(desc(Rumor.date)).all()
                   ]
    else:
        if order == 'asc':
            res = [(str(r.date), r.tweet_id, r.tweet)
                   for r in Rumor.query.filter_by(statement_id=statement_id
                                                  ).order_by(Rumor.date).all()
                   ]
        elif order == 'desc':
            res = [(str(r.date), r.tweet_id, r.tweet)
                   for r in Rumor.query.filter_by(statement_id=statement_id
                                                  ).order_by(desc(Rumor.date)).all()
                   ]
    
    return res


def getStatementsFromDB(event, cluster):
    """Get statements for event_cluster from database."""
    statements = Event_Cluster.query.filter_by(event_name=event,
                                               cluster_name=cluster).first().statements
    return statements


def getSupportOpposeSnippetsFromDB(statement_id):
    """Get Snippets for event_cluster from database."""
    statement_stance = Statement.query.filter_by(id=statement_id).first().stance
    if statement_stance == 'FAVOR':
        support = getSnippetsFromDB(statement_id, 'FAVOR')
        oppose = getSnippetsFromDB(statement_id, 'AGAINST')
    elif statement_stance == 'AGAINST':
        support = getSnippetsFromDB(statement_id, 'AGAINST')
        oppose = getSnippetsFromDB(statement_id, 'FAVOR')
    return support, oppose

def getSnippetsFromDB(statement_id, stance=None):
    if stance:
        snippets = [(snippet.id, snippet.content, snippet.target) for snippet in Snippet.query.filter_by(statement_id=statement_id, stance=stance).all()]
    else:
        snippets = [(snippet.id, snippet.content, snippet.target) for snippet in Snippet.query.filter_by(statement_id=statement_id).all()]        
    return snippets


def getSupportOpposeTweetsFromDB(statement_id):
    statement_stance = Statement.query.filter_by(id=statement_id).first().stance
    if statement_stance == 'FAVOR':
        support = getTweetsFromDB(statement_id, 'FAVOR', 'desc')
        oppose = getTweetsFromDB(statement_id, 'AGAINST', 'desc')
    elif statement_stance == 'AGAINST':
        support = getTweetsFromDB(statement_id, 'AGAINST', 'desc')
        oppose = getTweetsFromDB(statement_id, 'FAVOR', 'desc')
    return support, oppose

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a document."""
    if request.method == 'POST' and 'doc' in request.files:
        try:
            filename = docs.save(request.files['doc'])
            filename = secure_filename(filename)
            print(filename)
            url = docs.url(filename)
            user = User.query.filter_by(id=current_user.id).first()
            user.file_name = filename
            user.file_url = url
            db_session.add(user)
            db_session.commit()
            flash("Doc saved.", "success")
        except UploadNotAllowed:
            flash("The format is not correct.", "danger")
    return render_template('upload.html')


def copyFile():
    """Copy uploaded file to process folder."""
    user = User.query.filter_by(id=current_user.id).first()
    filename = user.file_name
    print ("filename", filename)
    uploadFilePath = UPLOADED_DATA_DIR / 'docs' / filename
    noSuffixFilname = filename.split(".")[0]
    processFolderPath = PROCESS_DATA_DIR / noSuffixFilname
    finalFolder = processFolderPath / 'final' / 'rawData'
    if not finalFolder.exists():
        finalFolder.mkdir(parents=True)
    shutil.copy(str(uploadFilePath), str(finalFolder / "tweets.pkl"))
    return noSuffixFilname


@app.route('/process')
def process():
    """Process upload data with Rudetect system."""
    eventFolderName = copyFile()
    r = make_response('finished', 200)
    print(PROCESS_DATA_DIR, eventFolderName)
    RuDetect27.main.main(str(PROCESS_DATA_DIR), eventFolderName)
    return r


# @app.before_first_request
# def setup():
#     """Reconstruct data before first request for testing."""
#     reinit_db()

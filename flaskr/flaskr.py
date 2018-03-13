import csv
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
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import make_response
import json
import os

PER_PAGE = 5
PRO = []
CON = []

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.cli.command('initdb')
def initd_command():
    """Initialize the databse."""
    init_db()
    print("Initialized the databse.")


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
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

        return redirect(url_for('login', error="Signup successfully"))
    return render_template('signup.html', form=form)


@app.route('/')
def show_rumors():
    """Show the rumors entries."""
    events = Event.query.all()
    print(current_user.is_authenticated)
    print(current_user.username)
    # events = [event for event in os.listdir("../data") if os.path.isdir('../data/'+event)]
    res = []
    for event in events:
        # head
        head = "#"+event.name
        # topics
        clusters = sorted(set([c.cluster_name for c in event.clusters]))
        topics = []
        for cluster in clusters:
            # with open('../data/'+event.name+'/'+cluster+'/targets.json') as fp:
            #     topic = json.load(fp)
            topic = Rumor.query.filter_by(event_name=event.name, cluster_name=cluster).first().target.split(";")
            print(event, cluster, topic)
            topics.append(topic)
        res.append({'head': head, 'topics': topics})
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


@app.route('/abstract/<event>/<cluster>')
@app.route('/abstract/<event>/<cluster>/<int:per_page>')
def getTweets4Event(event, cluster, per_page=5):
    """Get the details for event gabapentin."""
    global PER_PAGE
    global PRO
    global CON
    # session['event'] = event
    # session['per_page'] = per_page
    PER_PAGE = per_page
    print(PER_PAGE)
    # print(session['per_page'])
    pro = [(r.tweet_id, r.tweet) for r in Rumor.query.filter_by(stance='FAVOR').all()]
    con = [(r.tweet_id, r.tweet) for r in Rumor.query.filter_by(stance='AGAINST').all()]
    # pro, con = getTweets(event, cluster)
    PRO = pro[:]
    CON = con[:]
    # session['pro'] = pro
    # session['con'] = con
    return render_template('abstract.html', pro=pro[:PER_PAGE],
                           con=con[:PER_PAGE], event=event, cluster=cluster)


def get_tweets_for_page(event, data, page, per_page, count):
    """Get tweets for each page for pagination."""
    page -= 1
    if 5 * page + per_page < count:
        return data[per_page * page:per_page * page + per_page]
    else:
        return data[per_page * page:]


@app.route('/detail/<event>/<cluster>/<attitude>', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/detail/<event>/<cluster>/<attitude>/<int:page>', methods=['GET', 'POST'])
def show_tweets(event, attitude, cluster, page):
    """Show all the tweets with attitude in pagination way."""
    per_page = 10
    pro, con = getTweets(event, cluster)
    # print(getTweets('gabapentin'))
    if attitude == 'pro':
        count = len(pro)
        tweets = get_tweets_for_page(event, pro, page, per_page, count)
    elif attitude == 'con':
        count = len(con)
        tweets = get_tweets_for_page(event, con, page, per_page, count)
    pagination = Pagination(page=page, total=count, per_page=per_page,
                            search=False, css_framework='bootstrap4')
    return render_template('detail.html',
                           data=tweets,
                           pagination=pagination,
                           event=event,
                           attitude=attitude
                           )


@app.route('/loadmore')
def load_more():
    """Load more data and return jsonified data to js function."""
    # if session.get('event') and session.get('per_page'):
    # print(session.get('per_page'))
    global PER_PAGE
    global PRO
    global CON
    # print(PER_PAGE)
    # per_page = session.get('per_page')
    # pro_res = session['pro'][PER_PAGE:PER_PAGE+5]
    # con_res = session['con'][PER_PAGE:PER_PAGE+5]
    # session['per_page'] = per_page + 5
    augument = PER_PAGE + 5
    if augument > len(PRO):
        augument = len(PRO)
    pro_res = PRO[PER_PAGE:augument]
    con_res = CON[PER_PAGE:augument]
    PER_PAGE = augument
    print("="*100)
    print(PER_PAGE)
    return jsonify(pro=pro_res, con=con_res)


@app.route('/addopinion/<tweet_id>/<opinion_value>')
def add_opinion(tweet_id, opinion_value):
    """Add user's opinion to rumor."""
    r = make_response()
    r.status = '200'
    print("tweet_id", tweet_id)
    print("opinion", opinion_value)
    print("user_id", current_user.id)
    opinion = Opinion(stance=opinion_value)
    opinion.rumor = Rumor.query.filter_by(tweet_id=tweet_id).first()
    current_user.rumors.append(opinion)
    db_session.add(current_user)
    db_session.commit()
    return r



@app.before_first_request
def setup():
    """Reconstruct data before first request for testing."""
    reinit_db()

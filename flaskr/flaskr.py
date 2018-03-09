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
from flaskr.database import init_db, reinit_db
from flaskr.models import Event
import json
import os
from sqlalchemy import event

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


@app.cli.command('initdb')
def initd_command():
    """Initialize the databse."""
    init_db()
    print("Initialized the databse.")


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Close the database again at the end of the request."""
    db_session.remove()


@app.route('/')
def show_rumors():
    """Show the rumors entries."""
    # db = get_db()
    # cur = db.execute('select title, text from entries order by id desc')
    # entries = cur.fetchall()
    events = [event for event in os.listdir("../data") if os.path.isdir('../data/'+event)]
    res = []
    for event in events:
        # head
        tmp = []
        for i in event.split('_'):
            if not i.isdigit():
                tmp.append(i)
        head = "#"+''.join(tmp)
        # topics
        clusters = [cluster for cluster in os.listdir('../data/'+event) if os.path.isdir('../data/'+event+'/'+cluster)]
        topics = []
        for cluster in clusters:
            with open('../data/'+event+'/'+cluster+'/targets.json') as fp:
                topic = json.load(fp)
            topics.append(topic)
        res.append({'head': head, 'topics': topics})
    print(res)
    # test = [{'head': 'head1', 'topics': [['test1', 'test1', 'test1'], ['test2', 'test2', 'test2']]},
    #         {'head': 'head1', 'topics': [['test1', 'test1', 'test1'], ['test2', 'test2', 'test2']]},
    #         {'head': 'head1', 'topics': [['test1', 'test1', 'test1'], ['test2', 'test2', 'test2']]}
    #         ]
    return render_template('show_rumors.html', items=res, events=events)
#
#
# @app.route('/add', methods=['POST'])
# def add_entry():
#     """Add the new entry."""
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Logout."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


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
    pro, con = getTweets(event, cluster)
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


@app.route('/detail/<event>/<cluster>/<attitude>', defaults={'page': 1})
@app.route('/detail/<event>/<cluster>/<attitude>/<int:page>')
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


@app.before_first_request
def setup():
    """Reconstruct data before first request for testing."""
    reinit_db()

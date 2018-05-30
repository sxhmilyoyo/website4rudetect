import csv
from datetime import datetime
import json
from flaskr.database import db_session
from flaskr.models import Cluster
from flaskr.models import Event
from flaskr.models import Rumor
from flaskr.models import Event_Cluster
from flaskr.models import Statement
from flaskr.models import User
from flaskr.models import Snippet
# from flaskr.models import MyMixin
from pathlib import Path
from sqlalchemy import event
from sqlalchemy import exists
from werkzeug.security import generate_password_hash


# @event.listens_for(Event.__table__, 'after_create', propagate=True)
@event.listens_for(Snippet.__table__, 'after_create', propagate=True)
# @event.listens_for(Cluster.__table__, 'after_create', propagate=True)
def initialize_data(*args, **kwargs):
    """Initialize the data in the database."""
    # load events
    print("initialize data...")
    dataRootPath = Path("data")
    print(str(dataRootPath))
    events = [e for e in dataRootPath.iterdir() if e.is_dir()]
    for e in events:
        print(e)
        terms = [term for term in e.name.split('_') if not term.isdigit()]
        edited_event = " ".join(terms)
        clustersPath = e / 'clusterData'
        clusters = [cluster for cluster in clustersPath.iterdir() if cluster.is_dir()]
        if db_session.query(exists().where(Event.name == edited_event)).scalar():
            tableEvent = db_session.query(Event).filter(Event.name == edited_event).first()
        else:
            tableEvent = Event(name=edited_event)
        for cluster in clusters:
            print(cluster)
            if db_session.query(exists().where(Cluster.name == cluster.name)).scalar():
                clusterTable = db_session.query(Cluster).filter(Cluster.name == cluster.name).first()
            else:
                clusterTable = Cluster(name=cluster.name)
            event_cluster_id = edited_event + "_" + cluster.name
            # tableEvent_Cluster = Event_Cluster(id=event_cluster_id, svo_dict=svo_query, snippets=snippets)
            tableEvent_Cluster = Event_Cluster(id=event_cluster_id)
            tableEvent_Cluster.cluster = clusterTable
            tableEvent.clusters.append(tableEvent_Cluster)

            # get statements
            statements = getStatements(cluster)
            # get rumors
            rumors = getRumors(cluster)
            # get index_statement_2_index_rumor
            index_statement_2_index_rumor = getIndex(cluster)
            for index, rumor in enumerate(rumors):
                # idx = edited_event + "_" + str(i) + "_" + rumor[0]
                # associate rumors with event_cluster
                if db_session.query(exists().where(Rumor.tweet_id == rumor[0])).scalar():
                    tableRumor = db_session.query(Rumor).filter(Rumor.tweet_id == rumor[0]).first()
                else:
                    tableRumor = Rumor(
                        tweet_id=rumor[0], target=rumor[1], tweet=rumor[-1],
                        stance=rumor[3], date=datetime.strptime(rumor[4], '%Y-%m-%d %H:%M:%S')
                        )
                # tableSvo.rumors.append(tableRumor)
                tableEvent_Cluster.rumors.append(tableRumor)
                # associate rumors with statement
                for index_statement in index_statement_2_index_rumor:
                    if index in index_statement_2_index_rumor[index_statement]:
                        # print("statement index {}; rumor index {}".format(index_statement, index))
                        statement_id = event_cluster_id + "_" + index_statement
                        # print("statement id {}".format(statement_id))
                        # print(db_session.query(exists().where(Statement.id == statement_id)).scalar())
                        if db_session.query(exists().where(Statement.id == statement_id)).scalar():
                            tableStatement = db_session.query(Statement).filter(Statement.id == statement_id).first()
                            # print("duplicated")
                        else:
                            if len(statements[int(index_statement)]) == 5 and statements[int(index_statement)][1] and statements[int(index_statement)][-1] and statements[int(index_statement)][3]:
                                topic = statements[int(index_statement)][1]
                                statement = statements[int(index_statement)][-1]
                                stance = statements[int(index_statement)][3]
                                tableStatement = Statement(id=statement_id, content=statement, target=topic, stance=stance)
                            else:
                                # print("invalid statement.")
                                continue

                        snippets = getSnippets(cluster, index_statement)
                        for snippet in snippets:
                            snippet_id = statement_id + "_" + snippet[0]
                            if db_session.query(exists().where(Snippet.id == snippet_id)).scalar():
                                tableSnippet = db_session.query(Snippet).filter(Snippet.id == snippet_id).first()
                            else:
                                if len(snippet) == 7 and snippet[4] and snippet[1] and snippet[3]:
                                    content = snippet[4]
                                    target = snippet[1]
                                    stance = snippet[3]
                                    tableSnippet = Snippet(id=snippet_id, content=content, target=target, stance=stance)
                                else:
                                    # print("invalid snippet.")
                                    continue
                            tableStatement.snippets.append(tableSnippet)
                            tableStatement.rumors.append(tableRumor)
                            tableEvent_Cluster.statements.append(tableStatement)
                            db_session.add(tableEvent_Cluster)
                            db_session.commit()

    print("add admin...")
    hashed_password = generate_password_hash('1234', method='sha256')
    new_user = User(username='admin', email='admin@admin.com', password=hashed_password)
    db_session.add(new_user)
    db_session.commit()


def add_data(eventName):
    """Initialize the data in the database."""
    # load events
    print("adding {} data...".format(eventName))
    dataRootPath = Path("data")
    print(str(dataRootPath))
    eventPath = dataRootPath / eventName
    terms = [term for term in eventPath.name.split('_') if not term.isdigit()]
    edited_event = " ".join(terms)
    clustersPath = eventPath / 'clusterData'
    clusters = [cluster for cluster in clustersPath.iterdir() if cluster.is_dir()]
    if db_session.query(exists().where(Event.name == edited_event)).scalar():
        tableEvent = db_session.query(Event).filter(Event.name == edited_event).first()
    else:
        tableEvent = Event(name=edited_event)
    for cluster in clusters:
        print(cluster)
        if db_session.query(exists().where(Cluster.name == cluster.name)).scalar():
            clusterTable = db_session.query(Cluster).filter(Cluster.name == cluster.name).first()
        else:
            clusterTable = Cluster(name=cluster.name)
        event_cluster_id = edited_event + "_" + cluster.name
        # svo_query = getSvoQuery(cluster)
        tableEvent_Cluster = Event_Cluster(id=event_cluster_id)
        tableEvent_Cluster.cluster = clusterTable
        tableEvent.clusters.append(tableEvent_Cluster)

        # get statements
        statements = getStatements(cluster)
        # get rumors
        rumors = getRumors(cluster)
        # get index_statement_2_index_rumor
        index_statement_2_index_rumor = getIndex(cluster)
        for index, rumor in enumerate(rumors):
            # idx = edited_event + "_" + str(i) + "_" + rumor[0]
            # associate rumors with event_cluster
            if db_session.query(exists().where(Rumor.tweet_id == rumor[0])).scalar():
                tableRumor = db_session.query(Rumor).filter(Rumor.tweet_id == rumor[0]).first()
            else:
                tableRumor = Rumor(
                    tweet_id=rumor[0], target=rumor[1], tweet=rumor[-1],
                    stance=rumor[3], date=datetime.strptime(rumor[4], '%Y-%m-%d %H:%M:%S')
                    )
            tableEvent_Cluster.rumors.append(tableRumor)
            # associate rumors with statement
            for index_statement in index_statement_2_index_rumor:
                if index in index_statement_2_index_rumor[index_statement]:
                    statement_id = event_cluster_id + "_" + index_statement
                    
                    if db_session.query(exists().where(Statement.id == statement_id)).scalar():
                        tableStatement = db_session.query(Statement).filter(Statement.id == statement_id).first()
                    else:
                        if len(statements[int(index_statement)]) == 5 and statements[int(index_statement)][1] and statements[int(index_statement)][-1] and statements[int(index_statement)][3]:
                            topic = statements[int(index_statement)][1]
                            statement = statements[int(index_statement)][-1]
                            stance = statements[int(index_statement)][3]
                            tableStatement = Statement(id=statement_id, content=statement, target=topic, stance=stance)
                        else:
                            # print("invalid statement.")
                            continue

                    snippets = getSnippets(cluster, index_statement)
                    for snippet in snippets:
                        snippet_id = statement_id + '_' + snippet[0]
                        if db_session.query(exists().where(Snippet.id == snippet_id)).scalar():
                            # print("1")
                            tableSnippet = db_session.query(Snippet).filter(Snippet.id == snippet_id).first()
                        else:
                            if len(snippet) == 7 and snippet[4] and snippet[1] and snippet[3]:
                                # print("2")
                                content = snippet[4]
                                target = snippet[1]
                                stance = snippet[3]
                                tableSnippet = Snippet(id=snippet_id, content=content, target=target, stance=stance)
                            else:
                                # print("invalid snippet.")
                                continue
                        # print("snippet {}".format(tableSnippet))
                        tableStatement.snippets.append(tableSnippet)
                        tableStatement.rumors.append(tableRumor)
                        tableEvent_Cluster.statements.append(tableStatement)
                        db_session.add(tableEvent_Cluster)
                        db_session.commit()
                        # print("commit.")



def getRumors(folderPath):
    """Get the tweets details for each cluster."""
    details = []
    with (folderPath / "corpus_classification.csv").open() as fp:
        reader = csv.reader(fp, delimiter='\t')
        next(reader)
        for r in reader:
            details.append(r)
    return details
# event.listen(MyMixin, 'after_create', initialize_data)

def getStatements(folderPath):
    """Get the statements details for each cluster."""
    statements = []
    with (folderPath / "corpus_statements_classification.csv").open() as fp:
        reader = csv.reader(fp, delimiter='\t')
        next(reader)
        for r in reader:
            statements.append(r)
    return statements


# def getSvoQuery(folderPath):
#     """Get the svo and query for each cluster."""
#     with (folderPath / "candidate_statements.txt").open() as fp:
#         svo_query = fp.readlines(fp)
#     return svo_query


def getSnippets(folderPath, index_statement):
    """Get snippets for each statement."""
    snippets = []
    with (folderPath / "corpus_snippets_classification.csv").open() as fp:
        reader = csv.reader(fp, delimiter='\t')
        next(reader)
        for r in reader:
            if r[6][0] == index_statement:
                snippets.append(r)
    return snippets


def getIndex(folderPath):
    """Get index_statement_2_index_rumor for each cluster."""
    with (folderPath / "index_candiadate_statement_2_index_tweet.json").open() as fp:
        index = json.load(fp)
    return index
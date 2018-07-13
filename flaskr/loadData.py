from flaskr.database import db_session
from flaskr.models import Cluster
from flaskr.models import Event
from flaskr.models import Rumor
from flaskr.models import Event_Cluster
from flaskr.models import Statement
from flaskr.models import User
from flaskr.models import Snippet
from sqlalchemy import exists

from werkzeug.security import generate_password_hash
from sqlalchemy import event
from flaskr.createDatabaseTable import CreateDatabaseTable
from flaskr.Helper import Helper
from pathlib import Path


class LoadData(object):
    """Load Data class: load data to database.

    Arguments:
        object
    """

    def __init__(self, rootpath):
        self.dataRootPath = Path(rootpath)

    # @event.listens_for(Event.__table__, 'after_create', propagate=True)
    # @event.listens_for(Snippet.__table__, 'after_create', propagate=True)
    # @event.listens_for(Cluster.__table__, 'after_create', propagate=True)
    def initialize_data(self, *args, **kwargs):
        """Initialize the data in the database."""
        # load events
        print("initialize data...")
        events = [e for e in self.dataRootPath.iterdir() if e.is_dir()]

        # add data
        for e in events:
            # if e.name != "BandyLee_0110_0115":
            #     continue
            self.add_data(e.name)

    def add_data(self, eventName):
        """Initialize the data in the database."""
        # load events
        print("adding {} data...".format(eventName))

        eventPath = self.dataRootPath / eventName

        terms = [term for term in eventPath.name.split(
            '_') if not term.isdigit()]
        edited_event = " ".join(terms)
        tableEvent = CreateDatabaseTable.create_event(edited_event)

        clustersPath = eventPath / 'clusterData'
        clusters = [cluster for cluster in clustersPath.iterdir()
                    if cluster.is_dir()]
        for cluster in clusters:
            clusterTable = CreateDatabaseTable.create_cluster(cluster)
            event_cluster_id = edited_event + "_" + cluster.name
            tableEvent_Cluster = CreateDatabaseTable.combine_event_cluster(
                event_cluster_id, tableEvent, clusterTable)
            # get statements
            statementClusters = [statementCluster for statementCluster in (
                cluster / "classification").iterdir() if statementCluster.is_dir()]
            for statementCluster in statementClusters:
                # load data
                statement = Helper.getRepresentativeClaim(statementCluster)
                rumors = Helper.getClusterClaims(statementCluster)
                # snippets = Helper.getNews(cluster, statementCluster.name)
                snippets = Helper.getSnippets(statementCluster)
                # check all data
                if not (statement and rumors and snippets):
                    continue

                print("successfully load cluster data ", statementCluster)
                # print("statement ", statement)
                statement_id = event_cluster_id + "_" + statementCluster.name
                tableStatement = CreateDatabaseTable.create_statement(
                    statement_id, statement)
                if not tableStatement:
                    continue
                # continue
                # tableRumor = CreateDatabaseTable.create_rumor(rumor, rumor_id)
                # tableEvent_Cluster.rumors.append(tableRumor)

                # get rumors

                for indexRumor, rumor in enumerate(rumors):
                    rumor_id = statement_id + "_" + str(indexRumor)
                    tableRumor = CreateDatabaseTable.create_rumor(
                        rumor, rumor_id)
                    if not tableRumor:
                        continue
                    tableEvent_Cluster.rumors.append(tableRumor)
                    tableStatement.rumors.append(tableRumor)
                    
                # # news
                # for indexSnippet, snippet in enumerate(snippets):
                #     snippet_id = statement_id + "_" + str(indexSnippet)
                #     tableSnippet = CreateDatabaseTable.create_snippet(
                #         snippet_id, snippet)
                #     if not tableSnippet:
                #         continue
                #     tableStatement.snippets.append(tableSnippet)

                # snippets
                for indexSnippet, snippet in enumerate(snippets):
                    snippet_id = statement_id + "_" + str(indexSnippet)
                    tableSnippet = CreateDatabaseTable.create_snippet(
                        snippet_id, snippet)
                    if not tableSnippet:
                        continue
                    tableStatement.snippets.append(tableSnippet)

                tableEvent_Cluster.statements.append(tableStatement)
                db_session.add(tableEvent_Cluster)
                # print("commit")
                db_session.commit()

    @classmethod
    def add_user(cls, password, username, email):
        """Add user to the database"""
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email,
                        password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

    @classmethod
    def delete_data(cls, eventname):
        """Delete event data from database: Snippet, Rumor, Statement, Event_Cluster, Event"""
        event_clusters = db_session.query(Event_Cluster).filter(
            Event_Cluster.event_name == eventname).all()
        for event_cluster in event_clusters:
            statements = db_session.query(Statement).filter(
                Statement.event_cluster_id == event_cluster.id).all()
            for statement in statements:
                # delete snippets
                db_session.query(Snippet).filter(
                    Snippet.statement_id == statement.id).delete()
            # delete rumors
            db_session.query(Rumor).filter(
                Rumor.event_cluster_id == event_cluster.id).delete()
            # delete statements
            db_session.query(Statement).filter(
                Statement.event_cluster_id == event_cluster.id).delete()
        # delete event_clusters
        db_session.query(Event_Cluster).filter(
            Event_Cluster.event_name == eventname).delete()
        # delete events
        db_session.query(Event).filter(Event.name == eventname).delete()

        db_session.commit()

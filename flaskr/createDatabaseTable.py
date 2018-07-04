from flaskr.database import db_session
from flaskr.models import Cluster
from flaskr.models import Event
from flaskr.models import Rumor
from flaskr.models import Event_Cluster
from flaskr.models import Statement
from flaskr.models import User
from flaskr.models import Snippet
from sqlalchemy import exists
from datetime import datetime
from nltk import sent_tokenize


class CreateDatabaseTable(object):
    """Create tables for database.

    """

    @classmethod
    def create_event(cls, event_name):
        """Create Event table.

        Arguments:
            event_name {str} -- name of event

        Returns:
            table -- event table
        """
        if db_session.query(exists().where(Event.name == event_name)).scalar():
            tableEvent = db_session.query(Event).filter(
                Event.name == event_name).first()
        else:
            tableEvent = Event(name=event_name)
        return tableEvent

    @classmethod
    def create_cluster(cls, cluster):
        """Create Cluster table.

        Arguments:
            cluster {Path} -- the path of cluster

        Returns:
            table -- cluster table
        """
        print(cluster)
        if db_session.query(exists().where(Cluster.name == cluster.name)).scalar():
            clusterTable = db_session.query(Cluster).filter(
                Cluster.name == cluster.name).first()
        else:
            clusterTable = Cluster(name=cluster.name)
        return clusterTable
        # tableEvent_Cluster = Event_Cluster(id=event_cluster_id, svo_dict=svo_query, snippets=snippets)

    @classmethod
    def combine_event_cluster(cls, event_cluster_id, tableEvent, clusterTable):
        """Combine Event table with Cluster table.

        Arguments:
            event_cluster_id {str} -- the id for this table
            tableEvent {table} -- Event table
            clusterTable {table} -- Cluster table

        Returns:
            table -- Event_Cluster table
        """
        tableEvent_Cluster = Event_Cluster(id=event_cluster_id)
        tableEvent_Cluster.cluster = clusterTable
        tableEvent.clusters.append(tableEvent_Cluster)
        return tableEvent_Cluster

    @classmethod
    def create_rumor(cls, rumor, rumorID):
        """Create Rumor table.

        Arguments:
            rumor {list} -- the list contains rumor information

        Returns:
            table -- Rumor table
        """
        if db_session.query(exists().where(Rumor.tweet_id == rumorID)).scalar():
            tableRumor = db_session.query(Rumor).filter(
                Rumor.tweet_id == rumorID).first()
        else:
            tableRumor = Rumor(
                tweet_id=rumorID, target=rumor[1], tweet=rumor[2],
                stance=rumor[3], date=datetime.strptime(
                    rumor[4], '%Y-%m-%d %H:%M:%S')
            )
        return tableRumor
        # tableSvo.rumors.append(tableRumor)
        # associate rumors with statement
        # for index_statement in index_statement_2_index_rumor:
        # if index in index_statement_2_index_rumor[index_statement]:
        # print("statement index {}; rumor index {}".format(index_statement, index))

        # print("statement id {}".format(statement_id))
        # print(db_session.query(exists().where(Statement.id == statement_id)).scalar())

    @classmethod
    def create_statement(cls, statement_id, statement):
        """Create Statement Table.

        Arguments:
            statement_id {str} -- the id of statement
            index_statement {int} -- the index of statement
            statements {list} -- the list contains statements

        Returns:
            table -- Statement table
        """
        if db_session.query(exists().where(Statement.id == statement_id)).scalar():
            tableStatement = db_session.query(Statement).filter(
                Statement.id == statement_id).first()
            # print("duplicated")
        else:
            print("statement ", statement)
            if len(statement) == 4:
                topic = statement[1]
                content = statement[2]
                stance = statement[3]
                print("stance ", stance)
                tableStatement = Statement(
                    id=statement_id, content=content, target=topic, stance=stance)
            else:
                print("invalid statement.")
                print("length ", len(statement))
                print("statement ", statement)
                return None
        return tableStatement

    @classmethod
    def create_snippet(cls, snippet_id, snippet):
        """Create Snippet Table.

        Arguments:
            snippet_id {str} -- the id of snippet
            snippet {list} -- the list contains snippet information

        Returns:
            table -- Snippet table
        """
        if db_session.query(exists().where(Snippet.id == snippet_id)).scalar():
            tableSnippet = db_session.query(Snippet).filter(
                Snippet.id == snippet_id).first()
        else:
            if snippet:
                body = snippet["body"]
                bodyList = []
                # splitBody = body.split("\n")
                # tokenBody = [sent_tokenize(sb) for sb in splitBody]
                # bodyList = [j for i in tokenBody if i != [] for j in i]

                highLightIndices = []
                sentences = snippet["summary"]["sentences"]

                preEnd = 0
                for sentence in sentences:
                    # print("sentence ", sentence)
                    # print("bodyList ", bodyList)
                    if sentence in body:
                        start = body.find(sentence)
                        bodyList.append(body[preEnd:start])
                        end = body.find(sentence)+len(sentence)
                        bodyList.append(body[start:end])
                        highLightIndex = len(bodyList)-1
                        preEnd = end
                        highLightIndices.append(highLightIndex)
                    else:
                        print("missing sentence.")
                bodyList.append(body[end:])
                # print("bodyList ==========")
                # print(bodyList)
                # print("highLightIndices ==========")
                # print(highLightIndices)

                content = {"content": bodyList}
                summary = {"hightlight": highLightIndices}
                title_stance = snippet["sentiment"]["body"]["polarity"]
                body_stance = snippet["sentiment"]["body"]["polarity"]

                tableSnippet = Snippet(
                    id=snippet_id, content=content, summary=summary, title_stance=title_stance, body_stance=body_stance)
            else:
                # print("invalid snippet.")
                return None
        return tableSnippet

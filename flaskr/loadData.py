import csv
from datetime import datetime
import json
from flaskr.database import db_session
from flaskr.models import Cluster
from flaskr.models import Event
from flaskr.models import Rumor
from flaskr.models import Svo
from flaskr.models import User
# from flaskr.models import MyMixin
from pathlib import Path
from sqlalchemy import event
from sqlalchemy import exists
from werkzeug.security import generate_password_hash


# @event.listens_for(Event.__table__, 'after_create', propagate=True)
@event.listens_for(Rumor.__table__, 'after_create', propagate=True)
# @event.listens_for(Cluster.__table__, 'after_create', propagate=True)
def initialize_data(*args, **kwargs):
    """Initialize the data in the database."""
    # load events
    print("initialize data...")
    dataRootPath = Path("data")
    print(str(dataRootPath))
    events = [e for e in dataRootPath.iterdir() if e.is_dir()]
    for e in events:
        terms = [term for term in e.name.split('_') if not term.isdigit()]
        edited_event = " ".join(terms)
        clusters = [cluster for cluster in e.iterdir() if cluster.is_dir()]
        if db_session.query(exists().where(Event.name == Event.name)).scalar():
            clusterTable = db_session.query(Event).filter(Event.name == edited_event).first()
        else:
            tableEvent = Event(name=edited_event)
        for cluster in clusters:
            if db_session.query(exists().where(Cluster.name == cluster.name)).scalar():
                clusterTable = db_session.query(Cluster).filter(Cluster.name == cluster.name).first()
            else:
                clusterTable = Cluster(name=cluster.name)
            idx = edited_event + "_" + cluster.name
            svo_query = getSvoQuery(cluster)
            snippets = getSnippets(cluster, cluster.name)
            tableSvo = Svo(id=idx, svo_dict=svo_query, snippets=snippets)
            tableSvo.cluster = clusterTable
            tableEvent.clusters.append(tableSvo)

            rumors = getRumors(cluster)
            for i, rumor in enumerate(rumors):
                # idx = edited_event + "_" + str(i) + "_" + rumor[0]
                tableRumor = Rumor(
                    tweet_id=rumor[0], target=rumor[1], tweet=rumor[2],
                    stance=rumor[3], date=datetime.strptime(rumor[4], '%Y-%m-%d %H:%M:%S')
                    )
                tableSvo.rumors.append(tableRumor)
            db_session.add(tableSvo)
            db_session.commit()

    print("add admin...")
    hashed_password = generate_password_hash('1234', method='sha256')
    new_user = User(username='admin', email='admin@admin.com', password=hashed_password)
    db_session.add(new_user)
    db_session.commit()


def getRumors(folderPath):
    """Get the details for each cluster."""
    details = []
    with (folderPath / "corpus.csv").open() as fp:
        reader = csv.reader(fp, delimiter='\t')
        next(reader)
        for r in reader:
            details.append(r)
    return details
# event.listen(MyMixin, 'after_create', initialize_data)


def getSvoQuery(folderPath):
    """Get the svo and query for each cluster."""
    with (folderPath / "subject2svoqueries.json").open() as fp:
        svo_query = json.load(fp)
    return svo_query


def getSnippets(folderPath, cluster_name):
    """Get snippets for each cluster."""
    with (folderPath / "snippets.json").open() as fp:
        snippets = json.load(fp)
    return snippets

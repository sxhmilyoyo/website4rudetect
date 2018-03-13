import csv
from flaskr.database import db_session
from flaskr.models import Cluster
from flaskr.models import Event
from flaskr.models import Rumor
from flaskr.models import User
# from flaskr.models import MyMixin
from pathlib import Path
from sqlalchemy import event
from werkzeug.security import generate_password_hash


# @event.listens_for(Event.__table__, 'after_create', propagate=True)
@event.listens_for(Rumor.__table__, 'after_create', propagate=True)
# @event.listens_for(Cluster.__table__, 'after_create', propagate=True)
def initialize_data(*args, **kwargs):
    """Initialize the data in the database."""
    # load events
    print("initialize data...")
    dataRootPath = Path("../data")
    events = [e for e in dataRootPath.iterdir() if e.is_dir()]
    for e in events:
        terms = [term for term in e.name.split('_') if not term.isdigit()]
        edited_event = " ".join(terms)
        clusters = [cluster for cluster in e.iterdir() if cluster.is_dir()]
        tableEvent = Event(name=edited_event)
        for cluster in clusters:
            clusterTable = Cluster(name=cluster.name)
            rumors = getRumors(cluster)
            for i, rumor in enumerate(rumors):
                idx = edited_event + "_" + str(i) + "_" + rumor[0]
                rumorAssocTable = Rumor(
                    id=idx, tweet_id=rumor[0], target=rumor[1], tweet=rumor[2],
                    stance=rumor[3]
                    )
                rumorAssocTable.cluster = clusterTable
                tableEvent.clusters.append(rumorAssocTable)
        db_session.add(tableEvent)
        db_session.commit()

    print("add admin...")
    hashed_password = generate_password_hash('1234', method='sha256')
    new_user = User(username='admin', email='admin@admin.com', password=hashed_password)
    db_session.add(new_user)
    db_session.commit()


def getRumors(folderPath):
    """Get the details for event type."""
    details = []
    with (folderPath / "corpus.csv").open() as fp:
        reader = csv.reader(fp, delimiter='\t')
        next(reader)
        for r in reader:
            details.append(r)
    return details
# event.listen(MyMixin, 'after_create', initialize_data)

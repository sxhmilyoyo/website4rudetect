import csv
from flaskr.database import db_session
from flaskr.models import Event
from flaskr.models import Rumor
from flaskr.models import Cluster
# from flaskr.models import MyMixin
from flaskr.database import Base
import os
from pathlib import Path
from sqlalchemy import event


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
                idx = edited_event + "_" + str(i)
                rumorAssocTable = Rumor(
                    id=idx, tweet_id=rumor[0], target=rumor[1], tweet=rumor[2],
                    stance=rumor[3]
                    )
                rumorAssocTable.cluster = clusterTable
                tableEvent.clusters.append(rumorAssocTable)
        db_session.add(tableEvent)
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

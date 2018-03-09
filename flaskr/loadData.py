import csv
from flaskr.database import db_session
from flaskr.models import Event
from flaskr.models import Rumor
from flaskr.models import association_table
import os
from pathlib import Path
from sqlalchemy import event


@event.listens_for(association_table, 'after_create')
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
        for cluster in clusters:
            tableEvent = Event(name=edited_event, cluster=cluster.name)
            rumors = getRumors(cluster)
            for rumor in rumors:
                tableEvent.rumors.append(
                    Rumor(tweet_id=rumor[0], target=rumor[1], tweet=rumor[2],
                          stance=rumor[3]
                          )
                )
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

from flaskr.config import SQLALCHEMY_DATABASE_URI
from flaskr.config import SQLALCHEMY_MIGRATE_REPO
from migrate.versioning import api
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Import all modules that might define models."""
    from flaskr.models import Event, Rumor, Cluster, User, Opinion, Snippet, Event_Cluster, Origin_Statement, Statement
    # import flaskr.loadData
    Base.metadata.create_all(bind=engine)
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'databse repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))


def reinit_db():
    """Delte databse and re-construct database."""
    import flaskr.models
    import flaskr.loadData
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'databse repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

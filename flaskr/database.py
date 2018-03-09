from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////Users/xuhao/Workplace/Rudetect_website/database/flask.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Import all modules that might define models."""
    import flaskr.models
    Base.metadata.create_all(bind=engine)


def reinit_db():
    import flaskr.models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

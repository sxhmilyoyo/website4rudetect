import os
from pathlib import Path


appdir = os.path.abspath(os.path.dirname(__file__))
basedir = Path(os.path.dirname(appdir))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(str(basedir), 'flask.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(str(basedir), 'db_repository')

UPLOADED_DATA_DIR = basedir / 'upload'
PROCESS_DATA_DIR = basedir / 'data'

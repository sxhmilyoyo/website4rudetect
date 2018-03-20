import os


appdir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.dirname(appdir)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

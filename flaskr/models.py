from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from flaskr.database import Base
from flaskr.database import db_session
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin


# class MyMixin(object):
#
#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__.lower()
#
#     __table_args__ = {'mysql_engine': 'InnoDB'}
#     __mapper_args__= {'always_refresh': True}
#
#     id =  Column(Integer, primary_key=True)


class Rumor(Base):
    """Rumor association table."""

    __tablename__ = 'rumor'
    id = Column(String(100), primary_key=True)
    cluster_name = Column(String(5), ForeignKey('cluster.name'), primary_key=True)
    event_name = Column(String(50), ForeignKey('event.name'), primary_key=True)
    tweet_id = Column(String(50))
    target = Column(String(50))
    tweet = Column(Text)
    stance = Column(String(20))

    users = relationship('Opinion', backref=backref('rumor'), lazy=True)

    __table__args__ = (UniqueConstraint('id', 'cluster_name', 'event_name', name='_id_cluster_event_ck'))
    # rumor = relationship('Rumor', back_populates='events')
    # cluster = relationship('Cluster', )
    # event = relationship('Event', back_populates='rumors')

    def __repr__(self):
        return '<Record: cluster_name %r, event_name %r, rumor_id %r>' % (self.cluster_name, self.event_name, self.id)


class Cluster(Base):
    """Cluster model."""

    __tablename__ = 'cluster'
    id = Column(Integer, primary_key=True)
    name = Column(String(5), unique=True)
    # event_id = Column(Integer, ForeignKey('events.id'),
    #                   nullable=False)
    events = relationship('Rumor', backref=backref('cluster', lazy=True))
    # __table__args__ = (UniqueConstraint('id', 'name', name='_id_name_ck'))
    # def __init__(self, tweet_id=None, target=None, tweet=None, stance=None):
    #     """Construct the model."""
    #     self.tweet_id = tweet_id
    #     self.target = target
    #     self.tweet = tweet
    #     self.stance = stance

    def __repr__(self):
        """Show entries in this format."""
        return '<Cluster Name %r>' % (self.name)


class Event(Base):
    """Event model."""

    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    clusters = relationship('Rumor', backref=backref('event', lazy=True))

    def __repr__(self):
        """Show entries in this format."""
        return '<Event Name %r>' % (self.name)


class User(UserMixin, Base):
    """User model."""

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))

    rumors = relationship('Opinion', backref=backref('user'), lazy=True)

    def __repr__(self):
        """Show entries in this format."""
        return '<User name %r>' % (self.username)


class Opinion(Base):
    """Opinion association model."""

    __tablename__ = 'opinion'
    user_name = Column(String(50), ForeignKey('user.username'), primary_key=True)
    rumor_name = Column(String(100), ForeignKey('rumor.id'), primary_key=True)
    stance = Column(String(10), primary_key=True)

    __table__args__ = (UniqueConstraint('user_name', 'rumor_name', 'stance', name='_user_rumor_stance_ck'))

    def __repr__(self):
        """Show entries in this format."""
        return '<Opinion %r, User %r, Rumor %r>' % (self.stance, self.user_name, self.rumor_name)

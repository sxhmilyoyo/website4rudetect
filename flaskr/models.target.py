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


class Target(Base):
    """Target table."""

    __tablename__ = 'target'

    cluster_name = Column(String(5), ForeignKey('cluster.name'), primary_key=True)
    event_name = Column(String(50), ForeignKey('event.name'), primary_key=True)
    target = Column(String(50), unique=True)

    # __table__args__ = (UniqueConstraint('id', 'cluster_name', 'event_name', name='_id_cluster_event_ck'))
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
    events = relationship('Target', uselist=False, backref=backref('cluster', lazy=True))

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
    clusters = relationship('Target', backref=backref('event', lazy=True))

    def __repr__(self):
        """Show entries in this format."""
        return '<Event Name %r>' % (self.name)

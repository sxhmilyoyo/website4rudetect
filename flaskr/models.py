from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
from sqlalchemy import DateTime
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from flaskr.database import Base
from flaskr.database import db_session
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from sqlalchemy_utils import JSONType
from sqlalchemy_utils import force_auto_coercion
from sqlalchemy_json import NestedMutable
from sqlalchemy_utils import ScalarListType
from sqlalchemy.ext.associationproxy import association_proxy
from itertools import chain

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
    id = Column(Integer, primary_key=True)
    # cluster_name = Column(String(5), ForeignKey('cluster.name'), primary_key=True)
    # event_name = Column(String(50), ForeignKey('event.name'), primary_key=True)
    tweet_id = Column(String(50), unique=True)
    target = Column(String(50))
    tweet = Column(Text)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    stance = Column(String(20))

    users = relationship('Opinion', backref=backref('rumor'), lazy=True)
    # __table__args__ = (UniqueConstraint('id', 'cluster_name', 'event_name', name='_id_cluster_event_ck'))
    # rumor = relationship('Rumor', back_populates='events')
    # cluster = relationship('Cluster', )
    # event = relationship('Event', back_populates='rumors')

    # Rumor to Event_Cluster: Many to One
    # event_cluster_id = Column(String(100), ForeignKey('event_cluster.id'))
    # event_cluster = relationship("Event_Cluster", backref="rumors")
    event = association_proxy("cluster_association", "event")

    # Rumor to Statement: Many to One
    statement_id = Column(String(100), ForeignKey('statement.id'))
    statement = relationship("Statement", backref="rumors")

    def __repr__(self):
        return '<Rumor: cluster_name %r, event_name %r, rumor_id %r>' % (self.event_cluster.cluster_name, self.event_cluster.event_name, self.id)


class Cluster(Base):
    """Cluster model."""

    __tablename__ = 'cluster'
    id = Column(Integer, primary_key=True)
    name = Column(String(5), unique=True)
    # event_id = Column(Integer, ForeignKey('events.id'),
    #                   nullable=False)
    # events = relationship('Rumor', backref=backref('cluster', lazy=True))
    # __table__args__ = (UniqueConstraint('id', 'name', name='_id_name_ck'))
    # def __init__(self, tweet_id=None, target=None, tweet=None, stance=None):
    #     """Construct the model."""
    #     self.tweet_id = tweet_id
    #     self.target = target
    #     self.tweet = tweet
    #     self.stance = stance

    # events = relationship(
    #     'Event_Cluster', backref=backref('cluster', lazy=True))

    events = association_proxy("event_associations", "event", 
                        creator=lambda c: Event_Cluster(event=c))

    @property
    def statements(self):
        return list(chain(*[c.statements for c in self.event_associations]))

    def __repr__(self):
        """Show entries in this format."""
        return '<Cluster Name %r>' % (self.name)


class Event(Base):
    """Event model."""

    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    # clusters = relationship('Rumor', backref=backref('event', lazy=True))
    # clusters = relationship(
    #     'Event_Cluster', backref=backref('event', lazy=True))

    clusters = association_proxy("cluster_associations", "cluster", 
                        creator=lambda s: Event_Cluster(cluster=s))

    @property
    def statements(self):
        return list(chain(*[s.statements for s in self.cluster_associations]))

    def __repr__(self):
        """Show entries in this format."""
        return '<Event Name %r>' % (self.name)


class User(UserMixin, Base):
    """User model."""

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(80))
    file_name = Column(String(50), default=None, nullable=True)
    file_url = Column(String(), default=None, nullable=True)

    rumors = relationship('Opinion', backref=backref('user'), lazy=True)

    def __repr__(self):
        """Show entries in this format."""
        return '<User name %r>' % (self.username)


class Opinion(Base):
    """Opinion association model."""

    __tablename__ = 'opinion'
    user_name = Column(String(50), ForeignKey(
        'user.username'), primary_key=True)
    rumor_id = Column(String(100), ForeignKey('rumor.id'), primary_key=True)
    flag = Column(String(10), primary_key=True)
    stance = Column(String(10), primary_key=True)

    __table__args__ = (UniqueConstraint(
        'user_name', 'rumor_id', 'stance', name='_user_rumor_stance_ck'))

    def __repr__(self):
        """Show entries in this format."""
        return '<Opinion %r, User %r, Rumor %r>' % (self.stance, self.user_name, self.rumor_id)


class Event_Cluster(Base):
    """Association table between cluster and event"""

    __tablename__ = 'event_cluster'
    # id = Column(String(100), primary_key=True)
    cluster_id = Column(Integer, ForeignKey(
        'cluster.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'), primary_key=True)

    cluster = relationship("Cluster", backref="event_associations")
    event = relationship("Event", backref="cluster_associations")

    statements = relationship("Statement")

    # svo_dict = Column(NestedMutable.as_mutable(JSONType))
    # snippets = Column(NestedMutable.as_mutable(JSONType))

    def __repr__(self):
        return '<Event_Cluster: cluster_name %r, event_name %r>' % (self.cluster_name, self.event_name)

class Origin_Statement(Base):
    """Original Statement Model."""

    __tablename__ = 'origin_statement'
    id = Column(String(200), primary_key=True)
    content = Column(Text, unique=True)
    target = Column(String(50))
    stance = Column(String(20))
    # snippets = Column(NestedMutable.as_mutable(JSONType))

    # Statement to Event: One to One
    event_id = Column(Integer, ForeignKey('event.id'))
    event_cluster = relationship("Event", backref=backref("origin_statement", uselist=False))

    def __repr__(self):
        return '<Original Statement: id %r, event_id %r, content %r>' % (self.id, self.event_id, self.content)

class Snippet(Base):
    """Snippet Model."""

    __tablename__ = 'snippet'
    id = Column(String(200), primary_key=True)
    topic = Column(String(20))
    content = Column(Text)
    stance = Column(String(20))
    # Snippet to Statement: Many to One
    statement_id = Column(String(200), ForeignKey('statement.id'))
    statement = relationship("Statement", backref="snippets")

    def __repr__(self):
        return '<Snippet : id %r, statement_id %r, content %r>' % (self.id, self.statement_id, self.content)

class Statement(Base):
    """Statement Model."""

    __tablename__ = 'statement'
    __table_args__ = (
        ForeignKeyConstraint(['event_id', 'cluster_id'], 
        ['event_cluster.event_id', 'event_cluster.cluster_id']),
    )
    id = Column(String(200), primary_key=True)
    cluster_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)
    content = Column(Text, unique=True)
    target = Column(String(50))
    stance = Column(String(20))
    # snippets = Column(NestedMutable.as_mutable(JSONType))

    # Statement to Event_Cluster: Many to One
    # event_cluster_id = Column(String(100), ForeignKey('event_cluster.id'))
    # event_cluster = relationship("Event_Cluster", backref="statements")
    event = association_proxy("cluster_association", "event")
    def __repr__(self):
        return '<Statement: id %r, content %r>' % (self.id, self.content)
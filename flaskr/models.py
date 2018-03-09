from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, event, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from flaskr.database import Base, db_session


association_table = Table('association', Base.metadata,
                          Column('event_id', Integer, ForeignKey(
                              'events.id'), primary_key=True),
                          Column('rumor_id', Integer, ForeignKey(
                              'rumors.id'), primary_key=True)
                          )


class Rumor(Base):
    """Tweet model."""

    __tablename__ = 'rumors'
    id = Column(Integer, primary_key=True)
    tweet_id = Column(String(50), unique=True)
    target = Column(String(50))
    tweet = Column(Text)
    stance = Column(String(20))
    # event_id = Column(Integer, ForeignKey('events.id'),
    #                   nullable=False)
    events = relationship('Event', secondary=association_table, backref=backref('rumors', lazy=True))

    # def __init__(self, tweet_id=None, target=None, tweet=None, stance=None):
    #     """Construct the model."""
    #     self.tweet_id = tweet_id
    #     self.target = target
    #     self.tweet = tweet
    #     self.stance = stance

    def __repr__(self):
        """Show entries in this format."""
        return '<Tweet ID %r>' % (self.tweet_id)


class Event(Base):
    """Event model."""

    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cluster = Column(String(10))
    __table__args__ = (UniqueConstraint('name', 'cluster', name='_name_cluster_ck'))

    def __repr__(self):
        """Show entries in this format."""
        return '<Event %r>' % (self.name)

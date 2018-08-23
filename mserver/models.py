import datetime

import bcrypt
from sqlalchemy import Column, String, Integer, Boolean, Time, DateTime, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=True)
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)

    added_songs = relationship('Song', back_populates='user')

    repr_fields = ['username', 'is_superuser']

    def set_password(self, password):
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())


class DummySong(object):
    def __init__(self, **kwargs):
        self.search_id = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def search_key(self):
        return '{source}-{id}'.format(source=self.source, id=self.search_id or self.id)


class Song(Base, DummySong):
    __tablename__ = 'song'
    id = Column(Integer(), Sequence('song_id_seq'), primary_key=True)
    title = Column(String(250), nullable=False)
    artist = Column(String(250), nullable=True)
    album = Column(String(250), nullable=True)
    duration = Column(Time(), nullable=True)
    path = Column(String(500), nullable=True)
    created = Column(DateTime(), default=datetime.datetime.now)
    user_id = Column(ForeignKey('user.id'))
    user = relationship(User, back_populates='added_songs')
    source = Column(String(100))
    search_id = Column(String(500))
    available = Column(Boolean(), default=False)
    downloading = Column(Boolean(), default=False)
    error = Column(Boolean(), default=False)

    repr_fields = ['title', 'source', 'available']

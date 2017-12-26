import datetime

from sqlalchemy import Column, String, Integer, Boolean, Time, DateTime, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(200), nullable=True)
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)

    added_songs = relationship('Song', back_populates='user')


class SongPlayList(Base):
    __tablename__ = 'song_playlist'
    song_id = Column(ForeignKey('song.id'), primary_key=True)
    playlist_id = Column(ForeignKey('playlist.id'), primary_key=True)


class Song(Base):
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
    playlists = relationship('PlayList', secondary=SongPlayList.__tablename__, back_populates='songs')

    # Attributes used in search.
    source = ''
    available = True
    search_id = ''


class PlayList(Base):
    __tablename__ = 'playlist'
    id = Column(Integer(), Sequence('playlist_id_seq'), primary_key=True)
    name = Column(String(50))
    created = Column(DateTime(), default=datetime.datetime.now)

    songs = relationship('Song', secondary=SongPlayList.__tablename__, back_populates='playlists')

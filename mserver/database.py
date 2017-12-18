import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from .settings import BASE_DIR

sqlite_path = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'mserver.db'))

engine = create_engine(sqlite_path, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def base_model_repr(self):
    return '<{classname} {string}>'.format(classname=self.__class__.__name__, string=str(self))


Base.__repr__ = base_model_repr


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import mserver.models
    mserver.models.User
    Base.metadata.create_all(bind=engine)

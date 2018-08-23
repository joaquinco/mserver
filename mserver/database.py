from flask_sqlalchemy import SQLAlchemy

from mserver.application import app

db = SQLAlchemy(app)

Base = db.Model


def base_model_repr(self):
    """
    Allow objects to define repr_fields to show upon object representation.
    """
    if hasattr(self, 'repr_fields'):
        extra = '({})'.format(', '.join(['{key}={value}'.format(key=k, value=v) for (k, v) in {
            k: getattr(self, k)
            for k in self.repr_fields
        }.items()]))
    else:
        extra = str(id(self))
    return '<{classname} {extra}>'.format(classname=self.__class__.__name__, extra=extra)


Base.__repr__ = base_model_repr


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import mserver.models

    mserver.models.User
    db.create_all()

    return db

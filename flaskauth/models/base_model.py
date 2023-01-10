from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.declarative import declared_attr
from flaskauth import app

_PLURALS = {"y": "ies"}

db = SQLAlchemy(app)
ma = Marshmallow(app)


class BaseModel(object):
    # FIXME: Removing the `__tablename__` attrs from the
    # child tables results in `sqlalchemy.exc.ArgumentError`
    # exceptions.  What is the root cause?
    @declared_attr
    def __tablename__(cls):
        name = cls.__name__
        if _PLURALS.get(name[-1].lower(), False):
            name = name[:-1] + _PLURALS[name[-1].lower()]
        else:
            name = name + "s"
        return name
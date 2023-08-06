from flask_sqlalchemy import (SQLAlchemy as _SQLAlchemy,
                              BaseQuery as _Query, _QueryProperty)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy_unchained import (
    BaseModel as _BaseModel, DeclarativeMeta, QueryMixin as _QueryMixin,
    SessionManager, ModelManager, declarative_base, foreign_key)


class BaseQuery(_QueryMixin, _Query):
    pass


class BaseModel(_BaseModel):
    #: Query class used by :attr:`query`. Defaults to
    # :class:`SQLAlchemy.Query`, which defaults to :class:`BaseQuery`.
    query_class = None

    #: Convenience property to query the database for instances of this model
    # using the current session. Equivalent to ``db.session.query(Model)``
    # unless :attr:`query_class` has been changed.
    query = None


class SQLAlchemyUnchained(_SQLAlchemy):
    def __init__(self, app=None, use_native_unicode=True, session_options=None,
                 metadata=None, query_class=BaseQuery, model_class=BaseModel):
        super().__init__(app=app, use_native_unicode=use_native_unicode,
                         session_options=session_options, metadata=metadata,
                         query_class=query_class, model_class=model_class)
        self.association_proxy = association_proxy
        self.declared_attr = declared_attr
        self.foreign_key = foreign_key
        self.hybrid_method = hybrid_method
        self.hybrid_property = hybrid_property

        SessionManager.set_session_factory(lambda: self.session())
        self.SessionManager = SessionManager
        self.ModelManager = ModelManager

    def make_declarative_base(self, model, metadata=None,
                              query_class=BaseQuery) -> BaseModel:
        model = declarative_base(model=model, metadata=metadata)

        if not getattr(model, 'query_class', None):
            model.query_class = query_class
        model.query = _QueryProperty(self)

        return model

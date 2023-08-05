from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy, BaseQuery as _Query
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy_unchained import (BaseModel, DeclarativeMeta, ModelRegistry,
                                  QueryMixin, declarative_base, foreign_key)


class BaseQuery(QueryMixin, _Query):
    pass


class SQLAlchemy(BaseSQLAlchemy):
    def __init__(self, app=None, use_native_unicode=True, session_options=None,
                 metadata=None, query_class=BaseQuery, model_class=BaseModel):
        super().__init__(app=app, use_native_unicode=use_native_unicode,
                         session_options=session_options, metadata=metadata,
                         query_class=query_class, model_class=model_class)
        ModelRegistry().register_base_model_class(self.Model)

        self.association_proxy = association_proxy
        self.declared_attr = declared_attr
        self.foreign_key = foreign_key
        self.hybrid_method = hybrid_method
        self.hybrid_property = hybrid_property

    def make_declarative_base(self, model, metadata=None) -> BaseModel:
        return declarative_base(lambda: self.session(), model=model,
                                metaclass=DeclarativeMeta, metadata=metadata,
                                query_class=self.Query)

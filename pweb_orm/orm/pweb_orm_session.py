from __future__ import annotations
from flask_sqlalchemy.session import Session
import typing as t
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as sa_orm
from pweb_orm.orm.pweb_saas import PWebSaaS


class PWebORMSession(Session):

    def get_bind(self, mapper: t.Union[t.Any, None] = None, clause: t.Union[t.Any, None] = None, bind: t.Union[sa.engine.Engine, sa.engine.Connection, None] = None, **kwargs: t.Any, ) -> t.Union[sa.engine.Engine, sa.engine.Connection]:
        if bind is not None:
            return bind

        engines = self._db.engines
        saas_bind_key = None
        if not self._is_bind_key(mapper.local_table):
            saas_bind_key = PWebSaaS.get_tenant_key()

        if mapper is not None:
            try:
                mapper = sa.inspect(mapper)
            except sa_exc.NoInspectionAvailable as e:
                if isinstance(mapper, type):
                    raise sa_orm.exc.UnmappedClassError(mapper) from e
                raise

            engine = self._clause_to_engine(mapper.local_table, engines, saas_bind_key=saas_bind_key)

            if engine is not None:
                return engine

        if clause is not None:
            engine = self._clause_to_engine(clause, engines, saas_bind_key=saas_bind_key)

            if engine is not None:
                return engine

        if saas_bind_key in engines:
            return engines[saas_bind_key]

        return super().get_bind(mapper=mapper, clause=clause, bind=bind, kwargs=kwargs)

    def _is_bind_key(self, clause: sa.ClauseElement):
        table = None
        if clause is not None:
            if isinstance(clause, sa.Table):
                table = clause
            elif isinstance(clause, sa.UpdateBase) and isinstance(clause.table, sa.Table):
                table = clause.table

        if table is not None and "bind_key" in table.metadata.info:
            key = table.metadata.info["bind_key"]
            if key:
                return True
        return False

    def _clause_to_engine(self, clause: sa.ClauseElement | None, engines: t.Mapping[str | None, sa.engine.Engine], saas_bind_key=None) -> sa.engine.Engine | None:
        """If the clause is a table, return the engine associated with the table's metadata's bind key. """

        """
            This function copied from flask_sqlalchemy >> session.py
            It used for resolve bind key from Model Meta __bind_key__ = "PWebSaaS" this way.
            Here added custom bind key custom resolver for SaaS System
        """

        table = None
        if clause is not None:
            if isinstance(clause, sa.Table):
                table = clause
            elif isinstance(clause, sa.UpdateBase) and isinstance(clause.table, sa.Table):
                table = clause.table

        if table is not None and "bind_key" in table.metadata.info:
            key = table.metadata.info["bind_key"]

            if key is None and saas_bind_key:
                key = saas_bind_key

            if key not in engines:
                raise sa_exc.UnboundExecutionError(f"Bind key '{key}' is not in 'SQLALCHEMY_BINDS' config.")

            return engines[key]

        return None

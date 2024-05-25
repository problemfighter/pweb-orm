from __future__ import annotations
from flask_sqlalchemy.session import Session, _clause_to_engine
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

        if mapper is not None:
            try:
                mapper = sa.inspect(mapper)
            except sa_exc.NoInspectionAvailable as e:
                if isinstance(mapper, type):
                    raise sa_orm.exc.UnmappedClassError(mapper) from e

                raise

            engine = _clause_to_engine(mapper.local_table, engines)

            if engine is not None:
                return engine

        # Check the bind key on Model
        if clause is not None:
            engine = _clause_to_engine(clause, engines)

            if engine is not None:
                return engine

        bind_key = PWebSaaS.get_tenant_key()
        if bind_key in engines:
            return engines[bind_key]

        return super().get_bind(mapper=mapper, clause=clause, bind=bind, kwargs=kwargs)

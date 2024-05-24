from abc import ABC, abstractmethod
from flask import g, current_app


class PWebSaaSConst:
    TENANT_KEY = "tkey"


class PWebSaaSTenantResolver(ABC):

    @abstractmethod
    def get_tenant_key(self) -> str | None:
        pass


class PWebSaaS:
    tenantResolver: PWebSaaSTenantResolver = None

    @staticmethod
    def init_tenant_key(tenant_key=None):
        if tenant_key:
            return tenant_key
        elif PWebSaaS.tenantResolver:
            tenant_key = PWebSaaS.tenantResolver.get_tenant_key()

        if tenant_key:
            PWebSaaS.set_tenant_key(tenant_key)

        return tenant_key

    @staticmethod
    def set_tenant_key(key: str):
        g.pweb_saas = {PWebSaaSConst.TENANT_KEY: key}
        current_app.add_to_context_data(key=PWebSaaSConst.TENANT_KEY, value=key)

    @staticmethod
    def get_tenant_key():
        if "pweb_saas" in g and PWebSaaSConst.TENANT_KEY in g.pweb_saas:
            return g.pweb_saas[PWebSaaSConst.TENANT_KEY]
        tenant_key = current_app.get_context_data(key=PWebSaaSConst.TENANT_KEY)
        return PWebSaaS.init_tenant_key(tenant_key=tenant_key)

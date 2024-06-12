import contextvars
from abc import ABC, abstractmethod
from flask import g, request


class PWebSaaSConst:
    TENANT_KEY = "tkey"


class PWebSaaSTenantResolver(ABC):

    @abstractmethod
    def get_tenant_key(self) -> str | None:
        pass


tenant_key_context_var = contextvars.ContextVar("tenant_key", default=None)


class PWebSaaS:
    tenantResolver: PWebSaaSTenantResolver = None

    @staticmethod
    def init_tenant_key(tenant_key=None):
        try:
            if tenant_key:
                return tenant_key
            elif PWebSaaS.tenantResolver:
                tenant_key = PWebSaaS.tenantResolver.get_tenant_key()

            if tenant_key:
                PWebSaaS.set_tenant_key(tenant_key)
        except:
            pass
        return tenant_key

    @staticmethod
    def set_tenant_key(key: str):
        g.pweb_saas = {PWebSaaSConst.TENANT_KEY: key}
        if PWebSaaS.is_background_request():
            tenant_key_context_var.set(key)

    @staticmethod
    def is_background_request() -> bool:
        try:
            url = request.url
            return False
        except:
            return True

    @staticmethod
    def get_tenant_key():
        if "pweb_saas" in g and PWebSaaSConst.TENANT_KEY in g.pweb_saas:
            return g.pweb_saas[PWebSaaSConst.TENANT_KEY]
        tenant_key = None
        if PWebSaaS.is_background_request():
            tenant_key = tenant_key_context_var.get()
        return PWebSaaS.init_tenant_key(tenant_key=tenant_key)

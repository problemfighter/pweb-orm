import contextvars
import threading
from abc import ABC, abstractmethod
from flask import request, g
from ppy_common import Console
from saas.common.saas_excception import SaaSException


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
        except SaaSException as e:
            raise e
        except:
            pass
        return tenant_key

    @staticmethod
    def set_tenant_key(key: str):
        if PWebSaaS.is_background_request():
            tenant_key_context_var.set(key)
        else:
            g.pweb_saas = {PWebSaaSConst.TENANT_KEY: key}

    @staticmethod
    def is_background_request() -> bool:
        try:
            url = request.url
            return False
        except:
            return True

    @staticmethod
    def get_tenant_key():
        tenant_key = None
        if "pweb_saas" in g and PWebSaaSConst.TENANT_KEY in g.pweb_saas:
            tenant_key = g.pweb_saas[PWebSaaSConst.TENANT_KEY]
        elif PWebSaaS.is_background_request():
            tenant_key = tenant_key_context_var.get()
        Console.log(f"Existing Tenant Key: {tenant_key} Name: {threading.current_thread().name} ID: {threading.get_ident()}")
        return PWebSaaS.init_tenant_key(tenant_key=tenant_key)

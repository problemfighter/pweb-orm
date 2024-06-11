import threading
from pweb import PWebRegistry
from pweb_orm import PWebSaaS


class PWebSaaSContext(threading.Thread):
    _params: dict = None
    _tkey: str = None
    _method = None

    def __init__(self, tkey: str, method):
        threading.Thread.__init__(self)
        self._tkey = tkey
        self._method = method

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.join()

    def run(self):
        with PWebRegistry.pweb_app.app_context():
            PWebSaaS.set_tenant_key(self._tkey)
            if self._method and self._params:
                self._method(**self._params)
            elif self._method:
                self._method()

    def set_args_and_start(self, **kwargs):
        self._params = kwargs
        self.start()

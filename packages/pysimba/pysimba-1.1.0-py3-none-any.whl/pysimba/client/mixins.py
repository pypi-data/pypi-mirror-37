import os

from functools import lru_cache
from .core import Client


class ClientCapability:
    @property
    @lru_cache(maxsize=None)
    def client(self):
        return Client(
            app_id=os.getenv('CLIENT_APP_ID'),
            app_secret=os.getenv('CLIENT_APP_SECRET'),
            service_url=os.getenv('CLIENT_SERVICE_URL')
        )

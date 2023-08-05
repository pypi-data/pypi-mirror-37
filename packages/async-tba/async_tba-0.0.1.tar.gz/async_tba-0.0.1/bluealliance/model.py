import aiohttp
from .conn_state import ConnectionState
from typing import Any, Dict, Optional
from .mini_models import Datacache


class Model:
    def __init__(self, conn: ConnectionState, key: Optional[str] = None):
        self._connection = conn
        if key is not None:
            self.key = key
        # else no key (e.g. alliances)

    @property
    def connection(self) -> ConnectionState:
        return self._connection

    @property
    def _session(self) -> aiohttp.ClientSession:
        return self.connection.session

    @staticmethod
    def get_data_from_cache(cache: Dict[str, Datacache], datakey: str) -> Datacache:
        try:
            return cache[datakey]
        except KeyError:
            return Datacache(None, "", None)

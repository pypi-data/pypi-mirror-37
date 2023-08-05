import asyncio
import aiohttp
import logging
import time
from typing import List
from . import constants
from .mini_models import Datacache

logger = logging.getLogger(__name__)


class Route:
    def __init__(self, path: str):
        self.path = path
        self.url = constants.API_BASE_URL + path


def common_header(last_modified: str) -> dict:
    return {"If-Modified-Since": last_modified}


class ConnectionState:
    def __init__(
        self, x_tba_auth_key: str, event_loop: asyncio.base_events.BaseEventLoop
    ):
        self._session = aiohttp.ClientSession(
            headers={"X-TBA-Auth-Key": x_tba_auth_key},
            loop=event_loop if event_loop is not None else asyncio.get_event_loop(),
        )
        # HACK: Technically this cache will grow without bound and might store duplicate data.
        self._cache = {}  # route: data

    async def request(self, route: Route, **kwargs):
        url = route.url
        if url in self._cache and kwargs["headers"]["If-Modified-Since"] == "":
            if not self._cache[url].expiry < time.time():
                kwargs["headers"]["If-Modified-Since"] = self._cache[url].last_modified
            else:
                kwargs["headers"]["If-Modified-Since"] = ""
        async with self._session.get(url, **kwargs) as resp:
            if 300 > resp.status >= 200:
                # request OK
                data = await resp.json()
                c_control = resp.headers["Cache-Control"].split(", ")[1][8:]
                self._cache[url] = Datacache(
                    data, resp.headers["Last-Modified"], time.time() + float(c_control)
                )
                return data
            elif resp.status == 304:
                logger.debug("Returning {} from cache".format(url))
                return self._cache[url].data
            elif resp.status == 401:
                # somehow unauthorized..?
                raise PermissionError()

    def get_team(self, team_key: str, last_modified: str = "") -> dict:
        return self.request(
            Route(constants.API_TEAM_URL.format(team_key)),
            headers=common_header(last_modified),
        )

    def get_event(self, event_key: str, last_modified: str = "") -> dict:
        return self.request(
            Route(constants.API_EVENT_URL.format(event_key)),
            headers=common_header(last_modified),
        )

    def get_event_simple(self, event_key: str, last_modified: str = "") -> dict:
        return self.request(
            Route(constants.API_EVENT_URL.format(event_key) + "/simple"),
            headers=common_header(last_modified),
        )

    def get_robots(self, team_key: str, last_modified: str = "") -> list:
        r = Route(constants.API_TEAM_URL.format(team_key) + "/robots")
        return self.request(r, headers=common_header(last_modified))

    def get_alliances(self, event_key: str, last_modified: str = "") -> list:
        r = Route(constants.API_EVENT_URL.format(event_key) + "/alliances")
        return self.request(r, headers=common_header(last_modified))

    def get_team_event_keys(self, team_key: str, last_modified: str = "") -> List[str]:
        r = Route(constants.API_TEAM_URL.format(team_key) + "/events/keys")
        return self.request(r, headers=common_header(last_modified))

    def get_event_teams(self, event_key: str, last_modified: str = "") -> list:
        r = Route(constants.API_EVENT_URL.format(event_key) + "/teams")
        return self.request(r, headers=common_header(last_modified))

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    async def close(self):
        await self._session.close()

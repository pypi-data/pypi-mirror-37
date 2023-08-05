import asyncio
import aiohttp
from typing import Dict, Union
from . import constants
from .conn_state import ConnectionState
from .team import Team
from .event import Event, SimpleEvent
from .mini_models import Datacache


class Client:
    def __init__(
        self, x_tba_auth_key: str, event_loop: asyncio.base_events.BaseEventLoop = None
    ):
        self.status_last_modified = ""
        self.status = {}
        self._connection_state = ConnectionState(
            x_tba_auth_key,
            event_loop if event_loop is not None else asyncio.get_event_loop(),
        )

    async def get_status(self):
        async with self.session.get(
            constants.API_STATUS_URL,
            headers={"If-Modified-Since": self.status_last_modified},
        ) as r:
            if r.status == 200:
                s = await r.json()
                self.status = s
                self.status_last_modified = r.headers["Last-Modified"]
                return s
            elif r.status == 304:
                return self.status

    async def get_team(self, team_number: int) -> Team:
        t = await self._connection_state.get_team("frc" + str(team_number))
        return Team(self._connection_state, **t)

    async def get_event(self, event_key: str) -> Event:
        e = await self._connection_state.get_event(event_key)
        return Event(self._connection_state, **e)

    async def get_simple_event(self, event_key: str) -> Event:
        e = await self.connection_state.get_event_simple(event_key)
        return SimpleEvent(self._connection_state, **e)

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._connection_state.session

    @property
    def connection_state(self) -> ConnectionState:
        return self._connection_state

    async def close(self):
        await self._connection_state.close()

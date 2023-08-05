import aiohttp
from . import constants
from .conn_state import ConnectionState
from .mini_models import Datacache
from .model import Model
from .team import Team
from typing import Dict, List, Optional, Union


class Alliance(Model):
    def __init__(
        self,
        conn_state: ConnectionState,
        name: str = None,
        backup: Dict[str, str] = None,
        declines: List[str] = [],
        picks: List[str] = [],
        status: Dict[str, Union[str, None, Dict[str, int]]] = None,
    ):
        super().__init__(conn_state)

        self._name = name
        self._backup = backup
        self._declines = declines
        self._picks = picks
        # tourney status
        self._full_status = status
        self._level = status["level"]
        self._status = status["status"]
        self._record = status["record"]
        self._wins, self._losses, self._ties = (
            self._record["wins"],
            self._record["losses"],
            self._record["ties"],
        )

        self._current_level_record = status["current_level_record"]
        self._current_level_wins, self._current_level_losses, self._current_level_ties = (
            self._current_level_record["wins"],
            self._current_level_record["losses"],
            self._current_level_record["ties"],
        )

    async def get_declining_teams(self) -> List[Team]:
        return [
            Team(self.connection, **s)
            for s in [await self.connection.get_team(team) for team in self.declines]
        ]

    async def get_teams(self) -> List[Team]:
        return [
            Team(self.connection, **s)
            for s in [await self.connection.get_team(team) for team in self.picks]
        ]

    @property
    def name(self) -> str:
        """The alliance's name (e.g. Alliance 1)"""
        return self._name

    @property
    def backup(self) -> dict:
        """
        Dict detailing backup bot use.
        out: Team key that was replaced by the backup team.
        in: Team key that was called in as the backup.
        """
        return self._backup

    @property
    def picks(self) -> List[str]:
        """A list of team keys for the teams picked. Actual Team objects should be fetched with get_teams"""
        return self._picks

    @property
    def declines(self) -> List[str]:
        """A list of team keys for the teams that declined. Actual Team objects should be fetched with get_declining_teams"""
        return self._declines

    @property
    def status(self) -> str:
        """Playoff status (e.g. eliminated)"""
        return self._status

    @property
    def record(self) -> Dict[str, int]:
        """Overall playoff w/l/t record."""
        return self._record

    @property
    def wins(self) -> int:
        """Number of playoff wins."""
        return self._wins

    @property
    def losses(self) -> int:
        """Number of playoff losses."""
        return self._losses

    @property
    def ties(self) -> int:
        """Number of playoff ties."""
        return self._ties

    @property
    def current_level_record(self) -> Dict[str, int]:
        """w/l/t record for the alliance's current playoff round."""
        return self._current_level_record

    @property
    def current_level_wins(self) -> int:
        """Number of wins for the alliance's current playoff round."""
        return self._current_level_wins

    @property
    def current_level_losses(self) -> int:
        """Number of losses for the alliance's current playoff round."""
        return self._current_level_losses

    @property
    def current_level_ties(self) -> int:
        """Number of ties for the alliance's current playoff round."""
        return self._current_level_ties


class MatchAlliance(Model):
    def __init__(
        self,
        conn_state: ConnectionState,
        score: int = None,
        team_keys: List[str] = None,
        surrogate_team_keys: Optional[List[str]] = None,
        dq_team_keys: Optional[List[str]] = None,
    ):
        super().__init__(conn_state)

        self._score = score
        self._team_keys = team_keys
        self._surrogate_team_keys = surrogate_team_keys
        self._dq_team_keys = dq_team_keys

    @property
    def score(self) -> int:
        """Score for this alliance. Will be null or -1 for an unplayed match."""
        return self._score

    @property
    def team_keys(self) -> List[str]:
        """TBA Team keys (eg frc254) for teams on this alliance."""
        return self._team_keys

    async def get_teams(self):
        """Team objects for teams on this alliance."""
        return [
            Team(self.connection, **t)
            for t in [await self.connection.get_team(key) for key in self.team_keys]
        ]

    @property
    def surrogate_team_keys(self) -> List[str]:
        """TBA team keys (eg frc254) of any teams playing as a surrogate."""
        return self._surrogate_team_keys

    async def get_surrogate_teams(self) -> List[Team]:
        """Team objects of any teams playing as a surrogate."""
        return [
            Team(self.connection, **t)
            for t in [
                await self.connection.get_team(key) for key in self.surrogate_team_keys
            ]
        ]

    @property
    def dq_team_keys(self) -> List[str]:
        """TBA team keys (eg frc254) of any disqualified teams."""
        return self._dq_team_keys

    async def get_dq_teams(self) -> List[Team]:
        """Team objects of any disqualified teams."""
        return [
            Team(self.connection, **t)
            for t in [self.connection.get_team(key) for key in self.dq_team_keys]
        ]

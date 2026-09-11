from .club import Club
from .player import Player
from .category import Category
from .event import Event
from .match_log import MatchLog, Set
from .team import Team

_schema_namespace = {
    "Club": Club,
    "Player": Player,
    "Category": Category,
    "Event": Event,
    "MatchLog": MatchLog,
    "Set": Set,
    "Team": Team,
}

Club.model_rebuild(_types_namespace=_schema_namespace)
Player.model_rebuild(_types_namespace=_schema_namespace)
Category.model_rebuild(_types_namespace=_schema_namespace)
Event.model_rebuild(_types_namespace=_schema_namespace)
MatchLog.model_rebuild(_types_namespace=_schema_namespace)
Set.model_rebuild(_types_namespace=_schema_namespace)
Team.model_rebuild(_types_namespace=_schema_namespace)

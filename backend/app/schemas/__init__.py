from .club import Club
from .player import Player

_schema_namespace = {"Club": Club, "Player": Player}

Club.model_rebuild(_types_namespace=_schema_namespace)
Player.model_rebuild(_types_namespace=_schema_namespace)

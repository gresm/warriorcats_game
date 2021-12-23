from .entities import EntityStats, Action

KIT_ROLE = 0
STUDENT_ROLE = 1
WARRIOR_ROLE = 2
QUEEN_ROLE = 3
HERBALIST_ROLE = 4
LEADER_ROLE = 5


Hunt = Action("Hunt")
Fight = Action("Fight")
CollectHerbs = Action("CollectHerbs")
Patrol = Action("Patrol")


class CatStats(EntityStats):
    required_stats = {"age", "role"}
    stat_defaults = {"age": 0, "role": 0}


__all__ = [
    "KIT_ROLE",
    "STUDENT_ROLE",
    "WARRIOR_ROLE",
    "QUEEN_ROLE",
    "HERBALIST_ROLE",
    "LEADER_ROLE",
    "Hunt",
    "Fight",
    "CollectHerbs",
    "Patrol",
    "CatStats"
]

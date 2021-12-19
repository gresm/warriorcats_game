from .entities import EntityStats


class CatStats(EntityStats):
    required_stats = {"age"}

    stat_defaults = {"age": 0}

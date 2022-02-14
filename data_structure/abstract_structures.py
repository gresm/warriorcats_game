from __future__ import annotations

from . import Entity


class ClanStats:
    def __init__(self):
        self.herbs = 0
        self.prey = 0
        self.coins = 0


class Clan:
    def __init__(self, name: str):
        self.name = name
        self.stats = ClanStats()
        self.cats: set[Entity] = set()


class Game:
    def __init__(self, player1: str, *players: str):
        self._player_names = (player1, ) + players
        self.players = {name: Clan(name) for name in self._player_names}
        self.__player_names_iter = iter(self._player_names)
        self._current_player: str = ...

    @property
    def current_player(self):
        return self.players[self._current_player]

    def next_player(self):
        try:
            self._current_player = next(self.__player_names_iter)
        except StopIteration:
            self.__player_names_iter = iter(self._player_names)
            self.next_player()


__all__ = [
    "ClanStats",
    "Clan"
]

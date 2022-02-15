from __future__ import annotations

from . import Entity
from enum import Enum


class TaskType(Enum):
    win = 0
    reward = 1
    punishment = 2


class RewardType(Enum):
    coins = 0
    prey = 1
    herbs = 2
    heal = 3
    full_heal = 4


class TaskReward:
    def __init__(self, player: Clan, reward_type: RewardType, amount: int = 1):
        self.reward_type = reward_type
        self.amount = amount
        self.player = player

    def process_task(self):
        if self.reward_type == RewardType.coins:
            self.player.stats.coins += self.amount
        elif self.reward_type == RewardType.prey:
            self.player.stats.prey += self.amount
        elif self.reward_type == RewardType.herbs:
            self.player.stats.herbs += self.amount
        elif self.reward_type == RewardType.heal:
            heals_left = self.amount
            for cat in self.player.cats:
                if not heals_left:
                    break
                cat.info.health += 1
                heals_left -= 1
        elif self.reward_type == RewardType.full_heal:
            heals_left = self.amount
            for cat in self.player.cats:
                if not heals_left:
                    break
                cat.info.damage = 0
                heals_left -= 1


class BaseTask:
    def __init__(self, player: Clan, task_type: TaskType, reward_amount: int, reward_type: RewardType):
        self.player = player
        self.task_type = task_type
        self.task_reward = TaskReward(player, reward_type, reward_amount)

    def is_done(self) -> bool:
        pass


# TODO: finish class
class Tasks:
    pass


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
        # TODO: generate tasks
        self.tasks = ...


class Game:
    def __init__(self, player1: str, *players: str):
        self._player_names = (player1, ) + players
        self.players = {name: Clan(name) for name in self._player_names}
        self.winners: set[Clan] = set()
        self.__player_names_iter = iter(self._player_names)
        self._current_player: str = ...

    @property
    def current_player(self):
        return self.players[self._current_player]

    @property
    def game_ended(self):
        return not not self.winners

    def next_player(self):
        if self.game_ended:
            return
        try:
            self._current_player = next(self.__player_names_iter)
        except StopIteration:
            self.end_round()
            self.__player_names_iter = iter(self._player_names)
            self.next_player()

    def end_round(self):
        pass


__all__ = [
    "ClanStats",
    "Clan"
]

from __future__ import annotations

from . import Entity, generate_tasks
from enum import Enum


class TaskType(Enum):
    win = 0
    loose = 1
    reward = 2
    punishment = 3


class RewardType(Enum):
    coins = 0
    prey = 1
    herbs = 2
    heal = 3
    full_heal = 4
    damage = 5
    win = 5
    loose = 6


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
        elif self.reward_type == RewardType.damage:
            damages_left = self.amount
            for cat in self.player.cats:
                if not damages_left:
                    break
                cat.info.health -= 1
                damages_left -= 1


class BaseTask:
    def __init__(
            self, player: Clan, task_type: TaskType, reward_amount: int, reward_type: RewardType, description: str
    ):
        self.player = player
        self.task_type = task_type
        self.task_reward = TaskReward(player, reward_type, reward_amount)
        self.description = description
        self.done = False

    def check(self):
        if self.done:
            return True
        if self.is_done():
            self.task_reward.process_task()
            self.done = True
            return True
        return False

    def is_done(self) -> bool:
        pass


class Tasks:
    def __init__(self, *tasks: BaseTask):
        self.tasks = set(tasks)

    def check(self):
        remove_tasks = set()
        for task in self.tasks:
            if self.check():
                remove_tasks.add(task)
        for rm in remove_tasks:
            self.tasks.remove(rm)


class ClanStats:
    def __init__(self):
        self._herbs = 0
        self._prey = 0
        self.coins = 0

    @property
    def herbs(self):
        return self._herbs

    @herbs.setter
    def herbs(self, value):
        self._herbs = max(value, 0)

    @property
    def prey(self):
        return self.prey

    @prey.setter
    def prey(self, value):
        self.prey = max(value, 0)


class Clan:
    def __init__(self, name: str):
        self.name = name
        self.stats = ClanStats()
        self.cats: set[Entity] = set()
        self.tasks = generate_tasks(self)


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
    "Clan",
    "Game",
    "Tasks",
    "BaseTask",
    "TaskReward",
    "RewardType",
    "TaskType"
]

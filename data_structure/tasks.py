from .abstract_structures import BaseTask, TaskType, Tasks, RewardType, Clan
from . import constants as cst

import random as rd


class FoodDepravationChallengeTask(BaseTask):
    def __init__(self, player: Clan):
        super(FoodDepravationChallengeTask, self).__init__(
            player, TaskType.reward, rd.randint(5, 10), RewardType.prey,
            "This may help you when you are near death from starvation."
        )

    def is_done(self):
        return self.player.stats.prey <= 0


class HerbalistBeginnerTask(BaseTask):
    def __init__(self, player: Clan):
        super(HerbalistBeginnerTask, self).__init__(
            player, TaskType.reward, 5, RewardType.coins,
            f"You've found new hobby: collecting herbs, will you manage to collect them (5)"
        )

    def is_done(self) -> bool:
        return self.player.stats.herbs >= 5


class PreyOverloadTask(BaseTask):
    def __init__(self, player: Clan):
        self.required_prey = rd.randint(15, 25)
        super(PreyOverloadTask, self).__init__(
            player, TaskType.reward, rd.randint(30, 40), RewardType.coins,
            f"Get impressive amount of prey - {self.required_prey}."
        )

    def is_done(self) -> bool:
        return self.required_prey >= self.player.stats.prey


class HerbalistAdvancedTask(BaseTask):
    def __init__(self, player: Clan):
        super(HerbalistAdvancedTask, self).__init__(
            player, TaskType.reward, rd.randint(15, 20), RewardType.coins,
            f"You are getting better in collecting herbs, but will you manage to collect more? (25)"
        )

    def is_done(self) -> bool:
        return self.player.stats.herbs >= 25


class OverpopulationProblemTask(BaseTask):
    def __init__(self, player: Clan):
        self.max_entity_cramming = rd.randint(35, 45)
        self.damage = self.max_entity_cramming // 2
        super(OverpopulationProblemTask, self).__init__(
            player, TaskType.punishment, self.damage, RewardType.damage,
            f"Maybe don't reach the max entity cramming limit? ({self.damage})"
        )

    def is_done(self):
        return len(self.player.cats) >= self.max_entity_cramming


class HerbalistExpertTask(BaseTask):
    def __init__(self, player: Clan):
        super(HerbalistExpertTask, self).__init__(
            player, TaskType.reward, rd.randint(0, 20) * 10 + 100, RewardType.coins,
            f"If you manage to do this task, you can be named real herbalist expert (75)"
        )

    def is_done(self) -> bool:
        return self.player.stats.herbs >= 75


class ProsperityTask(BaseTask):
    def __init__(self, player: Clan):
        self.chosen = rd.randint(35, 40)
        super(ProsperityTask, self).__init__(
            player, TaskType.win, 1, RewardType.win,
            f"Guide your clan to the great future and make it the greatest clan ever (get {self.chosen} members)."
        )

    def is_done(self) -> bool:
        return len(self.player.cats) >= self.chosen


class SuicideTask(BaseTask):
    def __init__(self, player: Clan):
        self.chosen = rd.randint(1, 5)
        super(SuicideTask, self).__init__(
            player, TaskType.win, cst.liquid_victory_cost, RewardType.coins,
            f"Your task is to be a bad leader of your clan, and leave ony few alive ({self.chosen})."
        )

    def is_done(self):
        return len(self.player.cats) <= self.chosen


class LastClanStandingTask(BaseTask):
    def __init__(self, player: Clan):
        self.max_cats = rd.randint(2, 3)
        super(LastClanStandingTask, self).__init__(
            player, TaskType.win, 1, RewardType.win,
            f"Banish other clans from existence at any cost to get your revenge (Make them have only {self.max_cats}"
            f" cats)."
        )

    def is_done(self):
        for clan_name in self.player.game.players:
            clan = self.player.game.players[clan_name]

            if clan is self.player:
                continue

            if len(clan.cats) > self.max_cats:
                return False
        return True


_small_tasks = [
    FoodDepravationChallengeTask, HerbalistBeginnerTask, HerbalistBeginnerTask
]


_medium_tasks = [
    PreyOverloadTask, HerbalistAdvancedTask
]


_big_tasks = [
    OverpopulationProblemTask, HerbalistExpertTask
]


_win_tasks = [
    SuicideTask, ProsperityTask, ProsperityTask, ProsperityTask, ProsperityTask, LastClanStandingTask
]


def generate_tasks(player: Clan):
    tasks = set()

    for _ in range(rd.randint(3, 4)):
        tasks.add(rd.choice(_small_tasks))

    for _ in range(rd.randint(2, 3)):
        tasks.add(rd.choice(_medium_tasks))

    for _ in range(rd.randint(1, 2)):
        tasks.add(rd.choice(_big_tasks))
    tasks.add(rd.choice(_win_tasks))

    generated_tasks = set()

    for task_type in tasks:
        generated_tasks.add(task_type(player))

    return Tasks(*generated_tasks)


__all__ = [
    "generate_tasks"
]

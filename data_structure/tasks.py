from . import BaseTask, TaskType, Tasks, RewardType, Clan

import random as rd


class PreyOverloadTask(BaseTask):
    def __init__(self, player: Clan):
        self.required_prey = rd.randint(20, 30)
        super(PreyOverloadTask, self).__init__(
            player, TaskType.reward, rd.randint(30, 40), RewardType.coins,
            f"Get impressive amount of prey - {self.required_prey}."
        )

    def is_done(self) -> bool:
        return self.required_prey >= self.player.stats.prey


class FoodDepravationChallengeTask(BaseTask):
    def __init__(self, player: Clan):
        super(FoodDepravationChallengeTask, self).__init__(
            player, TaskType.reward, rd.randint(5, 10), RewardType.prey,
            "This may help you when you are near death from starvation."
        )

    def is_done(self):
        return self.player.stats.prey <= 0


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


class SuicideTask(BaseTask):
    def __init__(self, player: Clan):
        self.chosen = rd.randint(1, 5)
        super(SuicideTask, self).__init__(
            player, TaskType.win, 1000, RewardType.coins,
            f"Your task is to be a bad leader of your clan, and leave ony few alive ({self.chosen})."
        )

    def is_done(self):
        return len(self.player.cats) <= self.chosen


_small_tasks = [
    FoodDepravationChallengeTask
]


_medium_tasks = [
    PreyOverloadTask
]


_big_tasks = [
    OverpopulationProblemTask
]


_win_reward_tasks = [
    SuicideTask
]


def generate_tasks(player: Clan):
    tasks = set()

    for _ in range(rd.randint(2, 3)):
        tasks.add(rd.choice(_small_tasks)(player))

    for _ in range(rd.randint(1, 2)):
        tasks.add(rd.choice(_medium_tasks)(player))

    tasks.add(rd.choice(_big_tasks)(player))
    tasks.add(rd.choice(_win_reward_tasks)(player))
    return Tasks(*tasks)


__all__ = [
    "generate_tasks"
]

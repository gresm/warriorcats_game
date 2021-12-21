from __future__ import annotations

import pygame as pg


class Scene:
    _instances_cnt: int = -1
    instances: dict[int, Scene] = {}

    _scenes_cnt = -1
    # noinspection PyUnresolvedReferences
    scenes: dict[int, type[Scene]] = {}

    class_id: int = -1

    def __init__(self):
        self._instances_cnt += 1
        self.instances[self._instances_cnt] = self
        self.instance_id = self.current_instance_id()

    def __init_subclass__(cls, **kwargs):
        Scene._scenes_cnt += 1
        Scene.scenes[Scene._scenes_cnt] = cls
        cls.class_id = cls.current_class_id()

    @classmethod
    def current_instance_id(cls):
        return cls._instances_cnt

    @classmethod
    def current_class_id(cls):
        return cls._scenes_cnt

    def draw(self, surface: pg.Surface):
        pass


class SceneManager:
    def __init__(self):
        self.current: Scene | None = None

    def draw(self, surface: pg.Surface):
        if self.current is not None:
            self.current.draw(surface)

    def set_active_scene(self, scene_id: int):
        if scene_id in Scene.instances:
            self.current = Scene.instances[scene_id]

    def spawn_scene(self, scene_id):
        if scene_id in Scene.scenes:
            Scene.scenes[scene_id]()
            self.current = Scene.instances[Scene.current_instance_id()]
            return Scene.current_instance_id()
        return -1

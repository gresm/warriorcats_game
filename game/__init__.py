from .base_scene import SceneManager, Scene as BaseScene
from .window import *
from .custom_loaders import *
from . import load_assets as assets

scene_manager = SceneManager()
del SceneManager

from pygame import mixer

from girlsday_game.game import Game
from girlsday_game.music import Music


def test_music():
    mixer.__PYGAMEinit__()
    Music(Game)
    assert True

from girlsday_game.music import Music
from girlsday_game.game import Game
from pygame import mixer


def test_music():
    mixer.__PYGAMEinit__()
    Music_class = Music(Game)
    assert True
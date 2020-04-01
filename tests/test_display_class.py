from girlsday_game.display import Display
from girlsday_game.game import Game


def test_display():
    Display(Game, 800, 600)
    assert True

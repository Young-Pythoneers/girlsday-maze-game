from girlsday_game.game import Game
from girlsday_game.listener import EventListener


def test_even_listener():
    EventListener(Game)
    assert True

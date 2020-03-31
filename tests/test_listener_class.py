from girlsday_game.game import Game
from girlsday_game.listener import EventListener

def test_even_listener():
    listener_class = EventListener(Game)
    assert True
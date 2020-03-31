from girlsday_game.entity_keeper import EntityKeeper, Grid, GridPoint
from girlsday_game.timer_keeper import TimerKeeper


def test_entity_keeper():
    entity_keeper_class = EntityKeeper()
    assert True


def test_grid_point():
    gridpoint_class = GridPoint(EntityKeeper, 0, 0, 0, 0, 0, 0)
    assert True


def test_grid():
    grid_class = Grid(TimerKeeper())
    assert True

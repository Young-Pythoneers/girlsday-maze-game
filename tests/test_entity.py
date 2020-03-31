from girlsday_game.entity import Entity, GridEntity, Tile, Wall, Player, Enemy, Goal, Score, PhysicalEntity, \
    Projectile, Particle, Rocket, RocketDuck
from girlsday_game.entity_keeper import Grid


def test_entity():
    Entity()
    assert True


def test_grid_entity():
    GridEntity()
    assert True


def test_tile():
    Tile()
    assert True


def test_wall():
    Wall(Grid())
    assert True


def test_player():
    Player()
    assert True


def test_enemy():
    Enemy()
    assert True


def test_goal():
    Goal()
    assert True


def test_score():
    Score()
    assert True


def test_physical_entity():
    PhysicalEntity()
    assert True


def test_projectile():
    Projectile()
    assert True


def test_particle():
    Particle()
    assert True


def test_rocket():
    Rocket()
    assert True


def test_rocket_duck():
    RocketDuck()
    assert True

import pygame

from girlsday_game.entity import (
    Enemy,
    Entity,
    EntityContainer,
    Goal,
    Grid,
    GridMover,
    GridPoint,
    Particle,
    PhysicalEntity,
    Player,
    Rocket,
    RocketDuck,
    Score,
    Tile,
    Transitional,
    Wall,
)
from girlsday_game.timer import TimerContainer


def test_entity():
    Entity()
    assert True


def test_transitional():
    Transitional()
    assert True


def test_grid_mover():
    GridMover(EntityContainer())
    assert True


def test_tile():
    Tile()
    assert True


def test_wall():
    Wall(GridPoint(0, 0, 0, 0, 0, 0))
    assert True


def test_player():
    pygame.init()
    Player(Goal(), Score())
    assert True


def test_enemy():
    pygame.init()
    Enemy(Player(Goal(), Score()))
    assert True


def test_goal():
    Goal()
    assert True


def test_score():
    pygame.init()
    Score()
    assert True


def test_physical_entity():
    PhysicalEntity(0, 0, 0, 0)
    assert True


def test_particle():
    Particle(0, 0, 0, 0, TimerContainer())
    assert True


def test_rocket():
    Rocket(0, 0, 0, 0)
    assert True


def test_rocket_duck():
    RocketDuck(0, 0, 0, 0)
    assert True


def test_entity_keeper():
    EntityContainer()
    assert True


def test_grid_point():
    GridPoint(EntityContainer, 0, 0, 0, 0, 0, 0)
    assert True


def test_grid():
    Grid(TimerContainer())
    assert True

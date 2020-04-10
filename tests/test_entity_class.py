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
    Score,
    Tile,
    Transitional,
    Wall,
)
from girlsday_game.timer import TimerContainer
from girlsday_game.game import Game


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
    Player()
    assert True


def test_enemy():
    pygame.init()
    Enemy()
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
    game = Game()
    Particle(0, 0, 0, 0, game.grid)
    assert True


def test_entity_keeper():
    EntityContainer()
    assert True


def test_grid_point():
    GridPoint( 0, 0, 0, 0, 0, 0, EntityContainer())
    assert True


def test_grid():
    Grid(TimerContainer(),"../levels/lvl1.txt", Game())
    assert True

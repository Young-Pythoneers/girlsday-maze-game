from girlsday_game.entity import Entity
from girlsday_game.transition import (
    CosTransition,
    InstantTransition,
    LinearTransition,
    Transition,
    WobblyTransition,
)


def test_transition():
    Transition(Entity)
    assert True


def test_linear_transition():
    LinearTransition(Entity)
    assert True


def test_cosine_transition():
    CosTransition(Entity)
    assert True


def test_wobbly_transition():
    WobblyTransition(Entity)
    assert True


def test_instant_transition():
    InstantTransition(Entity)
    assert True

from girlsday_game.entity import Entity
from girlsday_game.transition import (
    CosTransition,
    InstantTransition,
    LinearTransition,
    Transition,
    WobblyTransition,
)


def test_transition():
    transition_class = Transition(Entity)
    assert True


def test_linear_transition():
    linear_transition_class = LinearTransition(Entity)
    assert True


def test_cosine_transition():
    cosine_transition_class = CosTransition(Entity)
    assert True


def test_wobbly_transition():
    wobbly_transition_class = WobblyTransition(Entity)
    assert True


def test_instant_transition():
    instant_transition_class = InstantTransition(Entity)
    assert True

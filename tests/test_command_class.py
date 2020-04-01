from girlsday_game.command import (
    AttackCommand,
    Command,
    JumpCommand,
    LoopCommand,
    MoveCommand,
    PiepCommand,
    Program,
)


def test_command():
    Command()
    assert True


def test_program():
    Program()
    assert True


def test_move_command():
    MoveCommand()
    assert True


def test_attack_command():
    AttackCommand()
    assert True


def test_jump_command():
    JumpCommand()
    assert True


def test_piep_command():
    PiepCommand()
    assert True


def test_loop_command():
    LoopCommand
    assert True

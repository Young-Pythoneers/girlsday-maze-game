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
    command_class = Command()
    assert True


def test_program():
    program_class = Program()
    assert True


def test_move_command():
    move_command_class = MoveCommand()
    assert True


def test_attack_command():
    attack_command_class = AttackCommand()
    assert True


def test_jump_command():
    jump_command_class = JumpCommand()
    assert True


def test_piep_command():
    piep_command_class = PiepCommand()
    assert True


def test_loop_command():
    loop_command_class = LoopCommand
    assert True

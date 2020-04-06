from abc import ABC

from girlsday_game.music import Music
from typing import Tuple

class Scope:
    def __init__(self, parent_scope):
        self.scope = {}
        self.parent_scope = parent_scope


class Command(ABC):
    def __init__(self):
        self.children = []
        self.command_pointer = 0
        self.scope = Scope(None)

    def do_command(self, ent, parent_scope) -> Tuple[bool, bool]:
        ...

    def add_child(self, command):
        self.children.append(command)


class Program(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, ent, parent_scope) -> Tuple[bool, bool]:
        while True:
            if self.command_pointer >= len(self.children):
                return False, False
            command = self.children[self.command_pointer]
            increment, success = command.do_command(ent, self.scope)
            if increment:
                self.command_pointer += 1
            if success:
                return False, True


class MoveLeftCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        entity.transition.define_transition(entity.entity_container.grid_x - 2, entity.entity_container.grid_y)
        return True, True


class MoveRightCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        entity.transition.define_transition(entity.entity_container.grid_x + 2, entity.entity_container.grid_y)
        return True, True

class MoveUpCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        entity.transition.define_transition(entity.entity_container.grid_x, entity.entity_container.grid_y - 2)
        return True, True

class MoveDownCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        entity.transition.define_transition(entity.entity_container.grid_x, entity.entity_container.grid_y + 2)
        return True, True

class MoveInDirectionCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        entity.transition.define_transition(entity.entity_container.grid_x, entity.entity_container.grid_y + 2)
        return True, True

class MooCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        Music.sound_handler("../sounds/moo.wav", 0)
        entity.transition.define_transition(entity.entity_container.grid_x, entity.entity_container.grid_y)
        return True, True

class VlaCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        print("VlaCommand")
        return True, True

class FlipCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        print("FlipCommand")
        return True, True

class FloerpCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        print("FloerpCommand")
        return True, True

class InfLoopCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        self.scope.parent_scope = parent_scope
        while True:
            command = self.children[self.command_pointer]
            increment, success = command.do_command(entity, self.scope)
            if increment:
                self.command_pointer += 1
            if self.command_pointer == len(self.children):
                self.command_pointer = 0
            if success:
                return False, True

class LoopCommand(Command):
    def __init__(self, repeats):
        Command.__init__(self)
        self.repeats = repeats
        self.iterator = 0

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        self.scope.parent_scope = parent_scope
        while True:
            loop_break = not self.iterator < self.repeats
            if self.command_pointer == 0:
                if loop_break:
                    self.iterator = 0
                    return True, False
                else:
                    self.iterator += 1
            command = self.children[self.command_pointer]
            increment, success = command.do_command(entity, self.scope)
            if increment:
                self.command_pointer += 1
            if self.command_pointer == len(self.children):
                self.command_pointer = 0
            if success:
                return False, True

class LoopUntilBool(Command):
    def __init__(self, boolean_statement):
        Command.__init__(self)
        self.boolean_statement = boolean_statement

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        self.scope.parent_scope = parent_scope
        while True:
            loop_break = self.boolean_statement.is_true(entity, self.scope)
            if self.command_pointer == 0 and loop_break:
                return True, False
            command = self.children[self.command_pointer]
            increment, success = command.do_command(entity, self.scope)
            if increment:
                self.command_pointer += 1
            if self.command_pointer == len(self.children):
                self.command_pointer = 0
            if success:
                return False, True


class IfCommand(Command):
    def __init__(self, boolean_statement):
        Command.__init__(self)
        self.boolean_statement = boolean_statement
        self.internal_state = False

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        if self.internal_state or self.boolean_statement.is_true(entity, parent_scope):
            self.internal_state = True
            command = self.children[0]
            increment, success = command.do_command(entity, parent_scope)
            if increment and not self.boolean_statement.is_true(entity, parent_scope):
                self.internal_state = False
        else:
            increment = True
            success = False
        return increment, success

class IfElseCommand(Command):
    def __init__(self, boolean_statement):
        Command.__init__(self)
        self.boolean_statement = boolean_statement
        self.internal_state = False

    def do_command(self, entity, parent_scope) -> Tuple[bool, bool]:
        if self.internal_state or self.boolean_statement.is_true(entity, parent_scope):
            self.internal_state = True
            command = self.children[0]
            increment, success = command.do_command(entity, parent_scope)
            if increment and not self.boolean_statement.is_true(entity, parent_scope):
                self.internal_state = False
        else:
            command = self.children[1]
            increment, success = command.do_command(entity)
        return increment, success

class BooleanOperator:
    def __init__(self):
        self.children = []

    def add_child(self, command):
        self.children.append(command)

class BooleanStatement:
    def is_true(self, entity, parent_scope):
        ...

class WallOnLeft(BooleanStatement):
    def is_true(self, entity, parent_scope):
        grid_x = entity.entity_container.grid_x - 1
        grid_y = entity.entity_container.grid_y
        left_neighbors = entity.entity_container.entity_container.grid[grid_y][grid_x].entities
        return len(left_neighbors) > 0

class WallOnRight(BooleanStatement):
    def is_true(self, entity, parent_scope):
        grid_x = entity.entity_container.grid_x + 1
        grid_y = entity.entity_container.grid_y
        left_neighbors = entity.entity_container.entity_container.grid[grid_y][grid_x].entities
        return len(left_neighbors) > 0

class WallOnUp(BooleanStatement):
    def is_true(self, entity, parent_scope):
        grid_x = entity.entity_container.grid_x
        grid_y = entity.entity_container.grid_y - 1
        left_neighbors = entity.entity_container.entity_container.grid[grid_y][grid_x].entities
        return len(left_neighbors) > 0

class WallOnDown(BooleanStatement):
    def is_true(self, entity, parent_scope):
        grid_x = entity.entity_container.grid_x
        grid_y = entity.entity_container.grid_y + 1
        left_neighbors = entity.entity_container.entity_container.grid[grid_y][grid_x].entities
        return len(left_neighbors) > 0

class BooleanAnd(BooleanOperator, BooleanStatement):
    def __init__(self):
        BooleanOperator.__init__(self)
        BooleanStatement.__init__(self)

    def is_true(self, entity, parent_scope):
        return self.children[0].is_true(entity, parent_scope) and self.children[1].is_true(entity, parent_scope)

class BooleanOr(BooleanOperator, BooleanStatement):
    def __init__(self):
        BooleanOperator.__init__(self)
        BooleanStatement.__init__(self)

    def is_true(self, entity, parent_scope):
        return self.children[0].is_true(entity, parent_scope) or self.children[1].is_true(entity, parent_scope)

class BooleanNot(BooleanOperator, BooleanStatement):
    def __init__(self):
        BooleanOperator.__init__(self)
        BooleanStatement.__init__(self)

    def is_true(self, entity, parent_scope):
        return not self.children[0].is_true(entity, parent_scope)


class CommandFactory:
    def make_enemy_program(self):
        program = Program()
        loop = InfLoopCommand()

        loop_until_right = LoopUntilBool(WallOnRight())
        loop_until_right.add_child(MoveRightCommand())

        loop_until_down = LoopUntilBool(WallOnDown())
        loop_until_down.add_child(MoveDownCommand())

        loop_until_left = LoopUntilBool(WallOnLeft())
        loop_until_left.add_child(MoveLeftCommand())

        loop_until_up = LoopUntilBool(WallOnUp())
        loop_until_up.add_child(MoveUpCommand())

        loop.add_child(loop_until_right)
        loop.add_child(loop_until_down)
        loop.add_child(loop_until_left)
        loop.add_child(loop_until_up)

        program.add_child(loop)
        return program

if __name__ == "__main__":
    entity = None
    program = Program()

    loop = LoopCommand(2)

    loop.add_child(VlaCommand())

    loop2 = LoopCommand(3)
    loop2.add_child(FlipCommand())

    loop.add_child(loop2)

    program.add_child(loop)

    do_we_continue = True
    while do_we_continue:
        _, do_we_continue = program.do_command(entity, None)
    print("done")
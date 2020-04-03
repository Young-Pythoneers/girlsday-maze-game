from abc import ABC

from girlsday_game.music import Music


class Command(ABC):
    def __init__(self):
        self.parent = None
        self.children = []
        self.command_pointer = 0

    def do_command(self, ent):
        ...

    def add_child(self, command):
        command.parent = self
        self.children.append(command)


class Program(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        if self.command_pointer >= len(self.children):
            return False
        command = self.children[self.command_pointer]
        command.do_command(entity)
        return self.command_pointer < len(self.children)

    def add_child(self, command):
        command.parent = self
        self.children.append(command)


class MoveLeftCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        self.parent.command_pointer += 1
        entity.transition.define_transition(entity.entity_container.grid_x - 2, entity.entity_container.grid_y)


class MoveRightCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        self.parent.command_pointer += 1
        entity.transition.define_transition(entity.entity_container.grid_x + 2, entity.entity_container.grid_y)

class MoveUpCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        self.parent.command_pointer += 1
        entity.transition.define_transition(entity.entity_container.grid_x, entity.entity_container.grid_y - 2)

class MoveDownCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        self.parent.command_pointer += 1
        entity.transition.define_transition(entity.entity_container.grid_x, entity.entity_container.grid_y + 2)

class MooCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        self.parent.command_pointer += 1
        Music.sound_handler("../sounds/moo.wav", 0)
        entity.transition.define_transition(entity.entity_container.grid_x, entity.entity_container.grid_y)

class LoopCommand(Command):
    def __init__(self, repeats):
        Command.__init__(self)
        self.loop_break = False
        self.repeats = repeats
        self.iterator = 1

    def do_command(self, entity):
        # print("LoopCommand")
        command = self.children[self.command_pointer]
        command.do_command(entity)
        self.loop_break = self.repeats != -1 and not self.iterator < self.repeats
        if self.command_pointer == len(self.children):
            if self.loop_break:
                self.iterator = 1
                self.parent.command_pointer += 1
            else:
                self.iterator += 1
            self.command_pointer = 0


class IfElseCommand(Command):
    def __init__(self, boolean_statement):
        Command.__init__(self)
        self.boolean_statement = boolean_statement

    def do_command(self, ent):
        if self.boolean_statement.is_true(ent):
            command = self.children[0]
        else:
            command = self.children[1]
        self.parent.command_pointer += 1
        command.do_command(ent)

class BooleanStatement:
    def is_true(self, ent):
        ...

class ObjectOnLeft(BooleanStatement):
    def is_true(self, ent):
        grid_x = ent.entity_container.grid_x - 1
        grid_y = ent.entity_container.grid_y
        left_neighbors = ent.entity_container.entity_container.grid[grid_y][grid_x].entities
        return len(left_neighbors) > 0



class CommandFactory:
    def make_enemy_program(self):
        program = Program()
        loop = LoopCommand(-1)#-1 means infinite repeats
        if_else_command = IfElseCommand(ObjectOnLeft())
        if_else_command.add_child(MoveRightCommand())
        if_else_command.add_child(MoveLeftCommand())
        loop.add_child(if_else_command)
        loop.add_child(MooCommand())
        program.add_child(loop)
        return program
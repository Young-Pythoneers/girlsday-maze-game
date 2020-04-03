from abc import ABC


class Command(ABC):
    def __init__(self):
        self.parent = None
        self.children = []
        self.command_pointer = 0

    def do_command(self, ent):
        ...

    def add_child(self, command):
        ...


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


class MoveCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        self.parent.command_pointer += 1
        print("MoveCommand")


class AttackCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        self.parent.command_pointer += 1
        print("AttackCommand")


class JumpCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        self.parent.command_pointer += 1
        print("JumpCommand")


class PiepCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self, entity):
        self.parent.command_pointer += 1
        print("PiepCommand")

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

    def add_child(self, command):
        command.parent = self
        self.children.append(command)

class CommandFactory:
    def make_enemy_program(self):
        program = Program()
        loop = LoopCommand(-1)#-1 means infinite repeats
        loop.add_child(MoveRightCommand())
        loop.add_child(MoveLeftCommand())
        program.add_child(loop)
        return program


if __name__ == "__main__":
    program = Program()

    loop = LoopCommand(2)
    loop.add_child(MoveCommand())
    loop.add_child(AttackCommand())

    loop2 = LoopCommand(2)
    loop2.add_child(JumpCommand())

    loop3 = LoopCommand(2)
    loop3.add_child(PiepCommand())

    loop2.add_child(loop3)

    loop.add_child(loop2)

    program.add_child(loop)
    # print(program.children)
    while True:
        do_we_continue = program.do_command()
        if not do_we_continue:
            break
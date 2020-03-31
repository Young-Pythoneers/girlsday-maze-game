class Command:
    def __init__(self):
        self.parent = None
        self.children = []
        self.command_pointer = 0

    def do_command(self):
        ...

    def add_child(self, command):
        ...


class Program(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self):
        if self.command_pointer >= len(self.children):
            return False
        command = self.children[self.command_pointer]
        command.do_command()
        return self.command_pointer < len(self.children)

    def add_child(self, command):
        command.parent = self
        self.children.append(command)


class MoveCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self):
        self.parent.command_pointer += 1
        print("MoveCommand")


class AttackCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self):
        self.parent.command_pointer += 1
        print("AttackCommand")


class JumpCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self):
        self.parent.command_pointer += 1
        print("JumpCommand")


class PiepCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def do_command(self):
        self.parent.command_pointer += 1
        print("PiepCommand")


class LoopCommand(Command):
    def __init__(self, repeats):
        Command.__init__(self)
        self.loop_break = False
        self.repeats = repeats
        self.iterator = 1

    def do_command(self):
        # print("LoopCommand")
        command = self.children[self.command_pointer]
        command.do_command()
        self.loop_break = not self.iterator < self.repeats
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

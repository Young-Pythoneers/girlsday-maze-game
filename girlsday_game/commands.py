class CommandList:
    def __init__(self):
        self.command_list = [EndCommand()]
        self.command_pointer = 0

    def add_command(self, command):
        command.command_list = command
        end_command = self.command_list.pop(-1)
        self.command_list.append(command)
        self.command_list.append(end_command)

    def get_next_command(self):
        while True:
            command = self.command_list[self.command_pointer].get_command()
            if not isinstance(command, LoopEndCommand):
                break
        return command

    def do_next_command(self, entity):
        command = self.get_next_command()
        command.do_command(entity)

class Command:
    def __init__(self, command_list):
        self.command_list = command_list

    def get_command(self):
        self.command_list.command_pointer += 1
        return self

    def do_command(self, entity):
        print("Command")

class EndCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def get_command(self):
        #do not increase command pointer
        return self

    def do_command(self, entity):
        print("EndCommand")

class LoopEndCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def get_command(self):
        # do not increase command pointer
        return self

    def do_command(self, entity):
        print("LoopEndCommand")

class LoopCommand(CommandList, Command):
    def __init__(self):
        CommandList.__init__(self)
        Command.__init__(self)
        self.end_loop = False

    def get_command(self):
        command = self.get_next_command()
        if isinstance(command, LoopEndCommand) and not self.end_loop:
            self.command_pointer = 0
            command = self.get_next_command()
            #to not increase command_pointer of
        return command


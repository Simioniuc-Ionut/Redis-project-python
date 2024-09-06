# Commands
from app.command_pattern import CommandInterface as Command


class CommandPing(Command):
    def __init__(self, receiver):
        self.__receiver = receiver

    def execute(self):
        return self.__receiver.ping()




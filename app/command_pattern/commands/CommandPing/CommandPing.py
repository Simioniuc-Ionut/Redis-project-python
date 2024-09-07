# Commands
from app.command_pattern.commands.CommandInterface import Command


class CommandPing(Command):
    def __init__(self, receiver):
        self.__receiver = receiver

    def execute(self):
        self.__receiver.ping()




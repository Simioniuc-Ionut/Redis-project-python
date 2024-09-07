# Commands
from app.command_pattern.commands.CommandInterface import Command


class CommandPing(Command):
    def __init__(self, receiver):
        self.__receiver = receiver

    async def execute(self):
        await self.__receiver.ping()




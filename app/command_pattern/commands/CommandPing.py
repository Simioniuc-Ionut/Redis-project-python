# Commands
from app.command_pattern.commands.Command import Command


class CommandPing(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    async def execute(self):
        await self.receiver.send_message(b"+PONG\r\n")



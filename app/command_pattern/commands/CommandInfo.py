from app.command_pattern.commands.Command import Command
from app import Globals


class CommandInfo(Command):

    def __init__(self, receiver):
        self.receiver = receiver
        self.role = Globals.global_role
        self.port = Globals.global_port

    async def execute(self):
        if self.role is not "master":
            self.role = "slave"
        message = f"${str(len(self.role) + 5)}\r\nrole:{self.role}\r\n"
        await self.receiver.send_message(message.encode())

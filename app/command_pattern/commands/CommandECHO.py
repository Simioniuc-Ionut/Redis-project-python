

from app.command_pattern.commands.Command import Command
class CommandECHO(Command):
    def __init__(self, receiver, message):
        self.receiver = receiver
        self.message = message

    async def execute(self):
        # debug
        print("CommandECHO execute , msg is " + self.message)
        await self.receiver.send_message(self.message.encode()) # will encode the strings to bytes

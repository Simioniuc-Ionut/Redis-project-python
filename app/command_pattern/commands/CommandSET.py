
from app.command_pattern.commands.Command import Command
class CommandSET(Command):
    def __init__(self, receiver, key, value, receiver_own_map):
        self.receiver = receiver
        self.key = key
        self.value = value
        self.map = receiver_own_map

    async def execute(self):
        self.map.update({self.key: self.value})
        await self.receiver.send_message(b"+OK\r\n")


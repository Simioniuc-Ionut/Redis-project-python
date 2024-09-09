import asyncio

from app.command_pattern.commands.Command import Command


class CommandPX(Command): # in milliseconds
    def __init__(self, receiver, key, milliseconds, receiver_own_map):
        self.receiver = receiver
        self.key = key
        self.time = milliseconds
        self.map = receiver_own_map

    async def execute(self):
        asyncio.create_task(self.__expire())

    async def __expire(self):
        seconds = int(self.time) / 1000
        await asyncio.sleep(seconds)
        self.map.pop(self.key, None)
        # we put None to avoid the KeyError if the key is not in the map
        # else we would have to check if the key is in the map before popping it

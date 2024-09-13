import asyncio

from app.command_pattern.commands.Command import Command


class CommandExpire(Command):
    def __init__(self, receiver, key, time: int, receiver_own_map, is_seconds: bool):
        self.receiver = receiver
        self.key = key
        self.time_seconds = time if is_seconds else time / 1000  # Convert to seconds
        self.map = receiver_own_map

    async def execute(self):
        asyncio.create_task(self.__expire())

    async def __expire(self):
        await asyncio.sleep(self.time_seconds)  # wait in seconds
        self.map.pop(self.key, None)

    # we put None to avoid the KeyError if the key is not in the map
    # else we would have to check if the key is in the map before popping it

import asyncio

from app.command_pattern.commands.Command import Command


class CommandExpire(Command):
    def __init__(self, receiver, key, time: int, receiver_own_map, is_seconds: bool, is_multiple_key: bool):
        self.receiver = receiver
        self.key = key
        self.time_seconds = time if is_seconds else time / 1000  # convert to seconds
        self.map = receiver_own_map
        self.is_multiple_keys = is_multiple_key

    async def execute(self):
        asyncio.create_task(self.__expire())

    async def __expire(self):
        if self.is_multiple_keys is False:
            await asyncio.sleep(self.time_seconds)  # wait in seconds
            self.map.pop(self.key, None)
        else:
            await asyncio.sleep(self.time_seconds)
            self.map = {}
        # we put None to avoid the KeyError if the key is not in the map
        # else we would have to check if the key is in the map before popping it

import asyncio

from app.command_pattern.commands.Command import Command

class CommandExpire(Command):
    """
    CommandExpire class to handle the EXPIRE command in the command pattern.

    Attributes:
    receiver (Receiver): The receiver object to handle communication.
    key (str): The key to set the expiration time for.
    time_seconds (float): The expiration time in seconds.
    map (dict): The dictionary representing the key-value store.
    """

    def __init__(self, receiver, key, time: int, receiver_own_map, is_seconds: bool):
        """
        Initialize the CommandExpire with a receiver, key, time, receiver's own map, and a flag indicating if the time is in seconds.

        Parameters:
        receiver (Receiver): The receiver object to handle communication.
        key (str): The key to set the expiration time for.
        time (int): The expiration time.
        receiver_own_map (dict): The dictionary representing the key-value store.
        is_seconds (bool): Flag indicating if the time is in seconds.
        """
        self.receiver = receiver
        self.key = key
        self.time_seconds = time if is_seconds else time / 1000  # Convert to seconds
        self.map = receiver_own_map

    async def execute(self):
        """
        Execute the EXPIRE command by creating a task to expire the key after the specified time.
        """
        asyncio.create_task(self.__expire())

    async def __expire(self):
        """
        Expire the key after the specified time by sleeping for the time duration and then removing the key from the map.
        """
        await asyncio.sleep(self.time_seconds)  # wait in seconds
        self.map.pop(self.key, None)

    # we put None to avoid the KeyError if the key is not in the map
    # else we would have to check if the key is in the map before popping it
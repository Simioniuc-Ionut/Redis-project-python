
from app.command_pattern.commands.Command import Command
class CommandSET(Command):
    """
    CommandSET is a command class that implements the SET operation for a key-value store.

    Attributes:
    receiver (object): The receiver object that will handle the response.
    key (str): The key to be set in the key-value store.
    value (str): The value to be associated with the key.
    map (dict): The dictionary representing the key-value store.
    """
    def __init__(self, receiver, key, value, receiver_own_map):
        """
        Initialize the CommandSET with a receiver, key, value, and the key-value store.

        Parameters:
        receiver (object): The receiver object that will handle the response.
        key (str): The key to be set in the key-value store.
        value (str): The value to be associated with the key.
        receiver_own_map (dict): The dictionary representing the key-value store.
        """
        self.receiver = receiver
        self.key = key
        self.value = value
        self.map = receiver_own_map

    async def execute(self):
        """
        Execute the SET command by updating the key-value store and sending a response.

        This method updates the key-value store with the provided key and value,
        and then sends an "+OK" response to the receiver.
        """
        self.map.update({self.key: self.value})
        await self.receiver.send_message(b"+OK\r\n")

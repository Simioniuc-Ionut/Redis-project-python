from app.command_pattern.commands.Command import Command

class CommandKEYS(Command):
    """
    CommandKEYS class to handle the KEYS command in the command pattern.

    Attributes:
    receiver (Receiver): The receiver object to handle communication.
    keys (dict): The dictionary representing the key-value store.
    pattern (str): The pattern to match keys against.
    """

    def __init__(self, receiver, pattern):
        """
        Initialize the CommandKEYS with a receiver and a pattern.

        Parameters:
        receiver (Receiver): The receiver object to handle communication.
        pattern (str): The pattern to match keys against.
        """
        self.receiver = receiver
        self.keys = receiver.own_map
        self.pattern = pattern

    async def execute(self):
        """
        Execute the KEYS command by filtering keys based on the pattern and sending the result to the client.
        """
        import fnmatch
        filtered_keys = fnmatch.filter(self.keys.keys(), self.pattern)
        # print("Filtered keys:", filtered_keys)  # debug
        message = "*" + str(len(filtered_keys)) + "\r\n"
        for key in filtered_keys:
            message += "$" + str(len(key)) + "\r\n" + key + "\r\n"
        await self.receiver.send_message(message.encode())
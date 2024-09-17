from app.command_pattern.commands.Command import Command

class CommandGET(Command):
    """
    CommandGET class to handle the GET command in the command pattern.

    Attributes:
    receiver (Receiver): The receiver object to handle communication.
    key (str): The key to retrieve the value for.
    map (dict): The dictionary representing the key-value store.
    """

    def __init__(self, receiver, receiver_own_map, key):
        """
        Initialize the CommandGET with a receiver, the receiver's own map, and a key.

        Parameters:
        receiver (Receiver): The receiver object to handle communication.
        receiver_own_map (dict): The dictionary representing the key-value store.
        key (str): The key to retrieve the value for.
        """
        self.receiver = receiver
        self.key = key
        self.map = receiver_own_map

    async def execute(self):
        """
        Execute the GET command by retrieving the value for the key and sending it to the client.

        If the key is not found in the map, send a nil response. Otherwise, send the value.
        """
        if self.key not in self.map:
            await self.receiver.send_message(b"$-1\r\n")
        else:
            value = self.map[self.key]
            message = "$" + str(len(value)) + "\r\n" + value + "\r\n"
            # debug
            print("CommandGET execute , msg is " + message)
            await self.receiver.send_message(message.encode())
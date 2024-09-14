from app.command_pattern.commands.Command import Command

class CommandECHO(Command):
    """
    CommandECHO class to handle the ECHO command in the command pattern.

    Attributes:
    receiver (Receiver): The receiver object to handle communication.
    message (str): The message to be echoed back to the client.
    """

    def __init__(self, receiver, message):
        """
        Initialize the CommandECHO with a receiver and a message.

        Parameters:
        receiver (Receiver): The receiver object to handle communication.
        message (str): The message to be echoed back to the client.
        """
        self.receiver = receiver
        self.message = message

    async def execute(self):
        """
        Execute the ECHO command by sending the message back to the client.

        This method encodes the message to bytes before sending.
        """
        # debug
        print("CommandECHO execute , msg is " + self.message)
        await self.receiver.send_message(self.message.encode())  # will encode the strings to bytes
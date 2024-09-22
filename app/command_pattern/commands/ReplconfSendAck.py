from app.command_pattern.commands.Command import Command


class CommandReplconfSendACK(Command):
    """
    The REPLCONF GETACK command.
    """

    def __init__(self, receiver):
        """
        Initialize the command.

        Parameters:
        receiver (object): The receiver object that will handle the response.
        option (str): The option for the REPLCONF command.
        value (str): The value for the REPLCONF command.
        """
        super().__init__(receiver)

    async def execute(self):
        """
        Execute the command.
        """
        msg = f"*3\r\n$8\r\nREPLCONF\r\n$3\r\nACK\r\n$1\r\n0\r\n"
        await self.receiver.send_message(msg.encode())

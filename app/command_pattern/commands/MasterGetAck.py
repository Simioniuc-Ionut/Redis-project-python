
from app.command_pattern.commands.Command import Command
class CommandMasterGetAck(Command):
    """
    The GETACK command.
    """

    def __init__(self, receiver):
        """
        Initialize the command.

        Parameters:
        receiver (object): The receiver object that will handle the response.
        """
        super().__init__(receiver)

    async def execute(self):
        """
        Execute the command.
        """
        response = f"*3\r\n$8\r\nREPLCONF\r\n$6\r\nGETACK\r\n$1\r\n*\r\n"
        await self.receiver.send_message(response.encode())
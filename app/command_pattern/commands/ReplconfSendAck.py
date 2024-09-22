from app.command_pattern.commands.Command import Command
from app import Globals
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
        msg = f"*3\r\n$8\r\nREPLCONF\r\n$3\r\nACK\r\n${len(str(Globals.global_offset))}\r\n{Globals.global_offset}\r\n"
        # print("Sending ACK ", msg)
        await self.receiver.send_message(msg.encode())

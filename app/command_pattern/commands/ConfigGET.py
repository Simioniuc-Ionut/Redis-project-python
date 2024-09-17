from app.command_pattern.commands.Command import Command
from app import Globals

class CommandConfigGet(Command):
    """
    CommandConfigGet class to handle the CONFIG GET command in the command pattern.

    Attributes:
    receiver (Receiver): The receiver object to handle communication.
    get_name (str): The name of the configuration parameter to get.
    message (str): The message to be sent to the client.
    """

    def __init__(self, receiver, get_name):
        """
        Initialize the CommandConfigGet with a receiver and the name of the configuration parameter.

        Parameters:
        receiver (Receiver): The receiver object to handle communication.
        get_name (str): The name of the configuration parameter to get.
        """
        self.get_name = get_name
        self.receiver = receiver
        self.message = None

    async def execute(self):
        """
        Execute the CONFIG GET command by determining the configuration parameter and sending the response to the client.
        """
        response = ""
        #print("in execute config get ", self.get_name)
        # For `CONFIG GET dir`
        if self.get_name == "dir":
            response = await self._get_directory()

        # For `CONFIG GET dbfilename`
        elif self.get_name == "dbfilename":
            response = await self._get_dbfilename()

        # Send answer to client
        await self.receiver.send_message(response.encode())

    async def _get_directory(self):
        """
        Get the directory configuration parameter.

        Returns:
        str: The response message for the directory configuration parameter.
        """
        #print("global dir ,dbname is ", Globals.global_dir, Globals.global_dbfilename)
        # Message RESP2 `CONFIG GET dir`
        response = "*2\r\n$3\r\ndir\r\n"
        response+= f"${len(Globals.global_dir)}\r\n{Globals.global_dir}\r\n"
        return response

    async def _get_dbfilename(self):
        """
        Get the dbfilename configuration parameter.

        Returns:
        str: The response message for the dbfilename configuration parameter.
        """
        # find directory "rdbfiles"
        response = "*2\r\n$9\r\ndbfilename\r\n"
        response += f"${len(Globals.global_dbfilename)}\r\n{Globals.global_dbfilename}\r\n"

        return response
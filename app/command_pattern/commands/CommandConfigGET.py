from app.command_pattern.commands.Command import Command
from app import Globals

class CommandConfigGet(Command):
    def __init__(self, receiver, get_name):
        self.get_name = get_name
        self.receiver = receiver
        self.message = None

    async def execute(self):
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

        #print("global dir ,dbname is ", Globals.global_dir, Globals.global_dbfilename)
        # Message RESP2 `CONFIG GET dir`
        response = "*2\r\n$3\r\ndir\r\n"
        response+= f"${len(Globals.global_dir)}\r\n{Globals.global_dir}\r\n"
        return response

    async def _get_dbfilename(self):
        # find directory "rdbfiles"
        response = "*2\r\n$9\r\ndbfilename\r\n"
        response += f"${len(Globals.global_dbfilename)}\r\n{Globals.global_dbfilename}\r\n"

        return response

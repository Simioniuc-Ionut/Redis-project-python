from app.command_pattern.commands.Command import Command
import os
from app import Globals

def find_directory(root_dir, target_dir_name):
    for root, dirs, files in os.walk(root_dir):
        if target_dir_name in dirs:
            return os.path.join(root, target_dir_name)
    return None


# Utilization for list the files in a directory
def list_files_in_directory(directory_path):
    try:
        return os.listdir(directory_path)
    except FileNotFoundError:
        return None


async def _get_directory():
    dir_path = find_directory(os.getcwd(), Globals.global_dir)

    if dir_path is not None:
        # Message RESP2 `CONFIG GET dir`
        response = "*2\r\n$3\r\ndir\r\n"
        response += f"${len(dir_path)}\r\n{dir_path}\r\n"
    else:
        response = "*2\r\n$3\r\ndir\r\n$-1\r\n"

    return response


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
        # Căutăm directorul "rdbfiles"
        print("global dir ,dbname is ", Globals.global_dir, Globals.global_dbfilename)

        # Mesaj RESP2 pentru `CONFIG GET dir`
        response = "*2\r\n$3\r\ndir\r\n"
        response+= f"${len(Globals.global_dir)}\r\n{Globals.global_dir}\r\n"
        return response

    async def _get_dbfilename(self):
        # find directory "rdbfiles"
        response = "*2\r\n$9\r\ndbfilename\r\n"
        response += f"${len(Globals.global_dbfilename)}\r\n{Globals.global_dbfilename}\r\n"

        return response

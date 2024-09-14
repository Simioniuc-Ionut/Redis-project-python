import asyncio
from app.command_pattern.ProcessCommands import process_ping, process_echo, process_set, process_get, \
    process_config_get, process_keys, process_info
from app import Globals

class Receiver:
    """
    Receiver class handles incoming messages from a client socket and processes commands.

    Attributes:
    client_socket (socket.socket): The client socket for communication.
    own_map (dict): The dictionary representing the key-value store.
    """

    def __init__(self, client_socket, keys):
        """
        Initialize the Receiver with a client socket and a key-value store.

        Parameters:
        client_socket (socket.socket): The client socket for communication.
        keys (dict): The dictionary representing the key-value store.
        """
        self.client_socket = client_socket
        self.own_map = keys

    async def receive_message(self):
        """
        Receive a message from the client socket asynchronously.

        Returns:
        bytes: The received message.
        """
        loop = asyncio.get_running_loop()
        return await loop.sock_recv(self.client_socket, 1024)

    async def send_message(self, message):
        """
        Send a message to the client socket asynchronously.

        Parameters:
        message (bytes): The message to be sent.
        """
        loop = asyncio.get_running_loop()
        await loop.sock_sendall(self.client_socket, message)

    async def process_message(self, message, invoker):
        """
        Process the received message and execute the corresponding command.

        Parameters:
        message (bytes): The received message.
        invoker (object): The invoker object that manages command execution.
        """
        if message:
            lines = message.decode().split("\r\n")
            if lines[0][:1] == "*":
                await self._process_array_message(lines, invoker)
            else:
                print("Invalid message format")
        else:
            print("No message received")

    async def _process_array_message(self, lines, invoker):
        """
        Process an array message and extract arguments.

        Parameters:
        lines (list): The list of lines in the message.
        invoker (object): The invoker object that manages command execution.
        """
        num_args = int(lines[0][1:])
        arguments = []
        index = 1
        for _ in range(num_args):
            index += 1
            argument = lines[index]
            arguments.append(argument)
            index += 1

        print("Arguments:", arguments)
        await self._handle_commands(arguments, invoker)

    async def _handle_commands(self, arguments, invoker):
        """
        Handle the extracted commands and execute the corresponding function.

        Parameters:
        arguments (list): The list of arguments for the command.
        invoker (object): The invoker object that manages command execution.
        """
        command = arguments[0].upper()
        if command == "PING":
            await process_ping(self, invoker)
        elif command == "ECHO":
            await process_echo(self, arguments, invoker)
        elif command == "SET":
            await process_set(self, arguments, invoker)
        elif command == "GET":
            await process_get(self, arguments, invoker)
        elif command == "CONFIG" and arguments[1].upper() == "GET":
            await process_config_get(self, arguments[2], invoker)
        elif command == "KEYS":
            await process_keys(self, arguments, invoker)
        elif command == "-P":
            port = arguments[1]
            if Globals.global_port is not port:
                print("That port not exist ", port)
            elif arguments[2].upper() == "INFO":
                await process_info(self, arguments, invoker)
import asyncio
from app.command_pattern.ProcessCommands import process_ping, process_echo, process_set, process_get, \
    process_config_get, process_keys, process_info, process_replication_config, process_psync, process_send_rdb_file
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
                nr_elements = int(lines[0][1:])  # *3 ,nr elements is 3
                await self._process_array_message(lines, invoker, nr_elements)

            else:
                print("Invalid message format")
        else:
            print("No message received")

    async def _process_array_message(self, lines, invoker, nr_elements):
        """
        Process an array message and extract arguments.

        Parameters:
        lines (list): The list of lines in the message.
        invoker (object): The invoker object that manages command execution.
        """
        # print("Array message:", lines)
        arguments = []
        index = 1
        #Array message: ['*3', '$3', 'SET', '$3', 'foo', '$3', '123', '*3', '$3', 'SET', '$3', 'bar', '$3', '456', '']
        for _ in range(nr_elements):
            index += 1
            argument = lines[index]
            arguments.append(argument)
            index += 1

        print("Arguments:", arguments)
        await self._handle_commands(arguments, invoker)
        # Check if there are more lines to process
        if index < len(lines) and lines[index] != '':
            new_lines = lines[index:]  # rest of the message
            new_nr_elements = int(new_lines[0][1:])  # *3 ,nr elements is 3
            await self._process_array_message(new_lines, invoker, new_nr_elements)  # we assume that is an array message

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
        elif command == "INFO":
            await process_info(self, arguments, invoker)
        elif command == "REPLCONF":  # send from replica to master
            await process_replication_config(self, arguments, invoker)
        elif command == "PSYNC":  # send from replica to master
            await process_psync(self, arguments, invoker)
            """After sending the FULLRESYNC response, the master will then send a RDB file of its current 
                state to the  replica. The replica is expected to load the file into memory, replacing its
                 current state."""
            # we need to send and empty rdb file
            await process_send_rdb_file(self, invoker)
            # we need to keep the replica connection with server master
            Globals.global_replica_connections.append(self)  # add the replica connection to the list

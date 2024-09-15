import asyncio

from app.command_pattern.commands.CommandPing import CommandPing, CommandPingReplication
from app.command_pattern.invoker.Invoker import Invoker
from app.connection.ConnectionRedis import ConnectionRedis


class MasterReceiver:
    """
    MasterReceiver class handles communication with the master server.

    Attributes:
    reader (StreamReader): The reader stream for receiving messages.
    writer (StreamWriter): The writer stream for sending messages.
    """

    def __init__(self, reader, writer):
        """
       Initialize the MasterReceiver with reader and writer streams.

       Parameters:
       reader (StreamReader): The reader stream for receiving messages.
       writer (StreamWriter): The writer stream for sending messages.
       """
        self.reader = reader
        self.writer = writer

    # async def receive_message(self):
    #     """
    #     Receive a message from the master server asynchronously.
    #
    #     Returns:
    #     bytes: The received message.
    #     """
    #     return await self.reader.read(1024)

    # async def send_message(self, message):
    #     """
    #     Send a message to the master server asynchronously.
    #
    #     Parameters:
    #     message (bytes): The message to be sent.
    #     """
    #     self.writer.write(message)
    #     await self.writer.drain()

    async def start_replica_server(self,master_host, master_port):
        """
        Start the replica server and connect to the master server.

        Parameters:
        master_host (str): The hostname of the master server.
        master_port (int): The port number of the master server.
        """
        print(f"Connecting to master at {master_host}:{master_port}...")
        connection = ConnectionRedis(master_host=master_host, master_port=master_port)
        reader, writer = await connection.connect_to_master()
        master_receiver = MasterReceiver(reader, writer)
        await self.start_handshake(master_receiver)

    async def start_handshake(self, reader, writer):
        invoker = Invoker()
        invoker.add_command(CommandPingReplication(reader, writer))
        response = await invoker.execute_commands()
        print("Handshake received: ", response)


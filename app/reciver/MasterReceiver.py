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

    def __init__(self):
        """
       Initialize the MasterReceiver with reader and writer streams.

       Parameters:
       reader (StreamReader): The reader stream for receiving messages.
       writer (StreamWriter): The writer stream for sending messages.
       """
        self.reader = None
        self.writer = None

    async def start_replica_server(self, master_host, master_port):
        """
        Start the replica server and connect to the master server.

        Parameters:
        master_host (str): The hostname of the master server.
        master_port (int): The port number of the master server.
        """
        print(f"Connecting to master at {master_host}:{master_port}...")
        connection = ConnectionRedis(master_host=master_host, master_port=master_port)
        await connection.perform_handshake()
        # self.reader, self.writer = await connection.connect_to_master()  # wait for connection to master
        # await self.start_handshake(self.reader, self.writer)

    # async def start_handshake(self, reader, writer):
    #     invoker = Invoker()
    #     invoker.add_command(CommandPingReplication(reader, writer))
    #     response = await invoker.execute_commands()
    #     print("Handshake received: ", response)


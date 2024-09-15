import asyncio
import argparse

from app.command_pattern.commands.CommandPing import CommandPing
from app.command_pattern.invoker.Invoker import Invoker
from app.observer_pattern.RDBFileHandler import load_rdb_file, start_monitoring_directory
from app.connection.ConnectionRedis import ConnectionRedis
from app.EventLoop import EventLoop
from app import Globals
from app.reciver.MasterReceiver import MasterReceiver


async def main_loop(server_set):
    """
    Main loop to accept and handle client connections.

    Parameters:
    server_set (ConnectionRedis): The server socket manager for accepting client connections.
    """
    while True:
        client_socket = await server_set.accept_client()
        print("Globals keys ", Globals.global_keys)
        loop = EventLoop(client_socket, Globals.global_keys)
        asyncio.create_task(loop.start())  # Handle client asynchronously


async def main():
    """
    Main function to start the server, parse arguments, load RDB file, and start monitoring the directory.
    """
    print("Starting server...")

    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, help='Directory to store the data')
    parser.add_argument('--dbfilename', type=str, help='Name of the file to store the data')
    parser.add_argument('--port', type=int, help='Port number to listen on', default=6379)
    parser.add_argument('--replicaof', type=str, help='Replicate data to another server', default='master')
    args = parser.parse_args()  # Parse arguments

    Globals.global_dir = args.dir
    Globals.global_dbfilename = args.dbfilename
    Globals.global_role = args.replicaof
    Globals.global_port = args.port

    # If server is started as a replica, connect to the master server
    if args.replicaof != 'master':

        print("Starting as replica server")
        master_host, master_port = args.replicaof.split(':')
        master_receiver = MasterReceiver(master_host, master_port)
        await master_receiver.start_replica_server(master_host, master_port)
    else:
        print("Starting as master server")

        if Globals.global_dir and Globals.global_dbfilename:
            # Load the RDB file initially (if it exists)
            await load_rdb_file(Globals.global_dir, Globals.global_dbfilename)

            # Start monitoring the directory for changes
            observer = start_monitoring_directory(Globals.global_dir, Globals.global_dbfilename,
                                                  lambda: load_rdb_file(Globals.global_dir, Globals.global_dbfilename))

        # Start the main loop
        server_set = ConnectionRedis(args.port)
        await main_loop(server_set)  # Execution will be blocked here until the main_loop is finished

        # Stop the observer
        try:
            while True:
                await asyncio.sleep(1)  # Keep the script running
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    asyncio.run(main())


async def start_replica_server(master_host, master_port):
    """
    Start the replica server and connect to the master server.

    Parameters:
    master_host (str): The hostname of the master server.
    master_port (int): The port number of the master server.
    """
    print(f"Connecting to master at {master_host}:{master_port}...")
    # Connect to the master server

    reader, writer = await asyncio.open_connection(master_host, master_port)
    print("Connected to master")

    # Handshake with the master server
    await start_handshake(writer)


async def start_handshake(receiver):
    invoker = Invoker()
    invoker.add_command(CommandPing(receiver))
    await invoker.execute_commands()

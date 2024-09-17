import asyncio
import argparse
import socket

from app.command_pattern.commands.Ping import CommandPing
from app.command_pattern.invoker.Invoker import Invoker
from app.observer_pattern.RDBFileHandler import load_rdb_file, start_monitoring_directory
from app.connection.ConnectionRedis import ConnectionRedis
from app.EventLoop import EventLoop
from app import Globals
from app.reciver.MasterReceiver import MasterReceiver


def set_globals_variables(args):
    Globals.global_dir = args.dir
    Globals.global_dbfilename = args.dbfilename
    if args.replicaof == 'master':
        Globals.global_role = "master"
    else:
        Globals.global_role = "replica"
    Globals.global_port = args.port


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


def perform_handshake(host, port, slave_port):
    with socket.create_connection((host, port)) as s:
        s.send("*1\r\n$4\r\nPING\r\n".encode())
        s.recv(1024)
        s.send(
            f"*3\r\n$8\r\nREPLCONF\r\n$14\r\nlistening-port\r\n$4\r\n{slave_port}\r\n".encode()
        )
        s.recv(1024)
        s.send("*3\r\n$8\r\nREPLCONF\r\n$4\r\ncapa\r\n$6\r\npsync2\r\n".encode())
        s.recv(1024)
        s.send("*3\r\n$5\r\nPSYNC\r\n$1\r\n?\r\n$2\r\n-1\r\n".encode())
        s.recv(1024)


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

    set_globals_variables(args)

    # If server is started as a replica, connect to the master server
    if args.replicaof != 'master':
        print("Starting as replica server")
        host, port = args.replicaof.split()
        perform_handshake(host, port, args.port)

        # master_host, master_port = args.replicaof.split()
        # master_receiver = MasterReceiver()
        # await master_receiver.start_replica_server(master_host, master_port)

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

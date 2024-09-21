import asyncio
import argparse
import socket

from app.command_pattern.commands.Ping import CommandPing
from app.command_pattern.invoker.Invoker import Invoker
from app.observer_pattern.RDBFileHandler import load_rdb_file, start_monitoring_directory
from app.connection.ConnectionRedis import ConnectionRedis
from app.EventLoop import EventLoop
from app import Globals

def set_globals_variables(args):
    Globals.global_dir = args.dir
    Globals.global_dbfilename = args.dbfilename
    if args.replicaof == 'master':
        Globals.global_role = "master"
    else:
        Globals.global_role = "replica"
    Globals.global_port = args.port


async def perform_handshake(host, port, slave_port):
    loop = asyncio.get_running_loop()
    s = socket.create_connection((host, port))  # Creează socket-ul fără context manager `with`.
    await loop.sock_sendall(s, "*1\r\n$4\r\nPING\r\n".encode())
    await loop.sock_recv(s, 1024)
    await loop.sock_sendall(s, f"*3\r\n$8\r\nREPLCONF\r\n$14\r\nlistening-port\r\n$4\r\n{slave_port}\r\n".encode())
    await loop.sock_recv(s, 1024)
    await loop.sock_sendall(s, "*3\r\n$8\r\nREPLCONF\r\n$4\r\ncapa\r\n$6\r\npsync2\r\n".encode())
    await loop.sock_recv(s, 1024)
    await loop.sock_sendall(s, "*3\r\n$5\r\nPSYNC\r\n$1\r\n?\r\n$2\r\n-1\r\n".encode())
    msg = await loop.sock_recv(s, 1024)
    print("Handshake completed, ", msg, " from ", s)
    msg = str(msg)
    if "REDIS" not in msg:
        msg = await loop.sock_recv(s, 1024)
        print("Handshake completed, ", msg, " ", s)
    msg = await loop.sock_recv(s, 1024)
    print("Handshake completed, ", msg, " from ", s)
    msg = await loop.sock_recv(s, 1024)
    print("Handshake completed, ", msg, " from ", s)
    msg = await loop.sock_recv(s, 1024)
    print("Handshake completed, ", msg, " from ", s)
    return s


async def master_main_loop(server_set):
    """
    Main loop to accept and handle client connections for the master server.

    Parameters:
    server_set (ConnectionRedis): The server socket manager for accepting client connections.
    """
    while True:
        client_socket = await server_set.accept_client()
        print("Globals keys ", Globals.global_keys)
        loop = EventLoop(client_socket, Globals.global_keys)
        asyncio.create_task(loop.start())  # Handle client asynchronously

async def replica_main_loop(server_set, master_socket):
    """
    Main loop to handle the connection with the master server and accept client connections for the replica server.

    Parameters:
    server_set (ConnectionRedis): The server socket manager for accepting client connections.
    master_socket (socket): The socket connected to the master server.
    """
    try:
        keys = Globals.global_keys
        # Handle master connection
        print("Master connection established  with master socket: ", master_socket)
        loop = EventLoop(master_socket, keys)
        asyncio.create_task(loop.start(True))  # Handle master connection asynchronously
        print("Master connection closed")
        # Accept client connections
        while True:
            try:
                client_socket = await server_set.accept_client()
                print("Globals keys ", keys, " client socket ", client_socket)
                loop = EventLoop(client_socket, keys)
                asyncio.create_task(loop.start())  # Handle client asynchronously
            except Exception as e:
                print(f"Error accepting client connection: {e}")
    except Exception as e:
        print(f"Error in replica main loop: {e}")
    # try:
    #     keys = Globals.global_keys
    #
    #     # Handle master connection in a separate task
    #     print("Master connection established with master socket:", master_socket)
    #     master_loop = EventLoop(master_socket, keys)
    #     master_task = asyncio.create_task(master_loop.start(True))  # Task for master connection
    #
    #     # Task for accepting client connections
    #     async def accept_clients():
    #         while True:
    #             try:
    #                 client_socket = await server_set.accept_client()  # Accept client connection
    #                 print("Client connected: ", client_socket)
    #                 client_loop = EventLoop(client_socket, keys)
    #                 asyncio.create_task(client_loop.start())  # Task for each client
    #             except Exception as e:
    #                 print(f"Error accepting client connection: {e}")
    #
    #     # Create a task for accepting clients
    #     accept_clients_task = asyncio.create_task(accept_clients())
    #
    #     # Wait for both master connection and client acceptor to run in parallel
    #     await asyncio.gather(master_task, accept_clients_task)
    #
    # except Exception as e:
    #     print(f"Error in replica main loop: {e}")

async def main():
    """
    Main function to start the server, parse arguments, load RDB file, and start monitoring the directory.
    """
    global master_socket , master_host, master_port
    print("Starting server...")

    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, help='Directory to store the data')
    parser.add_argument('--dbfilename', type=str, help='Name of the file to store the data')
    parser.add_argument('--port', type=int, help='Port number to listen on', default=6379)
    parser.add_argument('--replicaof', type=str, help='Replicate data to another server', default='master')
    args = parser.parse_args()  # Parse arguments

    set_globals_variables(args)

    # If application is started as a replica, connect to the master server
    if args.replicaof != 'master':
        print("Starting as replica server")
        master_host, master_port = args.replicaof.split()
        master_socket = await perform_handshake(master_host, master_port, args.port)
        print("Master socket is ", master_socket)
        # the connection is already closed.

        # now my replica server is connected to master server,and wait command from him ,to execute,like how a client is connected to a server master.
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
    if Globals.global_role == "master":
        await master_main_loop(server_set)  # Execution will be blocked here until the main_loop is finished
    else:
        await replica_main_loop(server_set,
                                master_socket)  # Execution will be blocked here until the main_loop is finished

    # Stop the observer
    try:
        while True:
            await asyncio.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    asyncio.run(main())

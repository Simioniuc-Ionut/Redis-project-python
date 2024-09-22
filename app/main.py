import asyncio
import argparse
import socket
import threading

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
    print("Handshake completed, ", msg)
    msg = str(msg)
    if "REDIS" not in msg:
        msg = await loop.sock_recv(s, 1024)
        print("Handshake completed, ", msg)
        msg = str(msg)
    # recevice ack concatenaed with the message
    if "REPLCONF" in msg:
        print("IS ACK REPLCONF concatenated with the message")
        Globals.global_first_ack = True
        await loop.sock_sendall(s, "*3\r\n$8\r\nREPLCONF\r\n$3\r\nACK\r\n$1\r\n0\r\n".encode())

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


async def handle_master_connection(master_socket, keys):
    """
        Handle the connection with the master server.

        This function establishes a connection with the master server, starts an event loop to process
        messages from the master server, and handles any exceptions that occur during the connection.

        Parameters:
        master_socket (socket): The socket connected to the master server.
        keys (dict): A dictionary to store key-value pairs.

        Returns:
        None
        """
    try:
        print("Master connection established with master socket: ", master_socket)
        loop = EventLoop(master_socket, keys)
        await loop.start(True)  # Handle master connection asynchronously
        print("Master connection closed")
    except Exception as e:
        print(f"Error handling master connection: {e}")


async def handle_client_connections(server_set, keys):
    """
    Accept and handle client connections.

    This function runs an infinite loop to accept client connections, starts an event loop to process
    messages from each client, and handles any exceptions that occur during the connection.

    Parameters:
    server_set (ConnectionRedis): The server socket manager for accepting client connections.
    keys (dict): A dictionary to store key-value pairs.

    Returns:
    None
    """
    while True:
        try:
            client_socket = await server_set.accept_client()
            print("Globals keys ", keys, " client socket ", client_socket)
            loop = EventLoop(client_socket, keys)
            asyncio.create_task(loop.start())  # Handle client asynchronously
        except Exception as e:
            print(f"Error accepting client connection: {e}")


def start_thread(loop, coro):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coro)


async def replica_main_loop(server_set, master_socket_con):
    """
    Main loop to handle the connection with the master server and accept client connections for the replica server.

    Parameters:
    server_set (ConnectionRedis): The server socket manager for accepting client connections.
    master_socket (socket): The socket connected to the master server.
    """
    try:
        keys = Globals.global_keys

        # Create event loops for each thread
        master_loop = asyncio.new_event_loop()
        client_loop = asyncio.new_event_loop()

        # Create threads for each loop
        master_thread = threading.Thread(target=start_thread,
                                         args=(master_loop, handle_master_connection(master_socket_con, keys)))
        client_thread = threading.Thread(target=start_thread,
                                         args=(client_loop, handle_client_connections(server_set, keys)))

        # Start threads
        master_thread.start()
        client_thread.start()

        # Join threads
        master_thread.join()
        client_thread.join()

    except Exception as e:
        print(f"Error in replica main loop: {e}")


def _parser_arguments(parser):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, help='Directory to store the data')
    parser.add_argument('--dbfilename', type=str, help='Name of the file to store the data')
    parser.add_argument('--port', type=int, help='Port number to listen on', default=6379)
    parser.add_argument('--replicaof', type=str, help='Replicate data to another server', default='master')
    return parser.parse_args()  # Parse arguments


async def main():
    """
    Main function to start the server, parse arguments, load RDB file, and start monitoring the directory.
    """
    global master_socket, master_host, master_port
    print("Starting server...")

    # Parse the arguments
    args = _parser_arguments(argparse.ArgumentParser())

    set_globals_variables(args)

    # If application is started as a replica, connect to the master server
    if args.replicaof != 'master':
        print("Starting as replica server")
        master_host, master_port = args.replicaof.split()
        master_socket = await perform_handshake(master_host, master_port, args.port)
        print("Master socket is ", master_socket)  # obtain connection between replica and master
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

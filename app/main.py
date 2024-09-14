import asyncio
import argparse
from app.observer_pattern.RDBFileHandler import load_rdb_file, start_monitoring_directory
from app.connection.ConnectionRedis import ConnectionRedis
from app.EventLoop import EventLoop
from app import Globals

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
    args = parser.parse_args()  # Parse arguments

    Globals.global_dir = args.dir
    Globals.global_dbfilename = args.dbfilename

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
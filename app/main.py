import asyncio
import argparse
import time
from app.observer_pattern.RDBFileHandler import load_rdb_file, start_monitoring_directory
from app.connection.ConnectionRedis import ConnectionRedis
from app.EventLoop import EventLoop
from app import Globals


async def main_loop(server_set):
    while True:
        client_socket = await server_set.accept_client()
        loop = EventLoop(client_socket)
        asyncio.create_task(loop.start())  # Handle client asynchronously
        # print("Client handled asynchronously")


def main():
    print("Starting server...")

    # we parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, help='Directory to store the data')
    parser.add_argument('--dbfilename', type=str, help='Name of the file to store the data')

    args = parser.parse_args()  # we parse to args

    Globals.global_dir = args.dir
    Globals.global_dbfilename = args.dbfilename

    # Load the RDB file initially (if it exists)
    load_rdb_file(Globals.global_dir, Globals.global_dbfilename)

    # Start monitoring the directory for changes
    observer = start_monitoring_directory(Globals.global_dir, Globals.global_dbfilename,
                                          lambda: load_rdb_file(Globals.global_dir, Globals.global_dbfilename))

    # Start the main loop
    server_set = ConnectionRedis()
    asyncio.run(main_loop(server_set))
    # execution will be blocked here until the main_loop is finished

    # Stop the observer
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:  # Stop the observer when the script is interrupted by user with CTR+C
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()

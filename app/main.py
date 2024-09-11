import asyncio
import argparse
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, help='Directory to store the data')
    parser.add_argument('--dbfilename', type=str, help='Name of the file to store the data')

    args = parser.parse_args()  # we parse to args

    Globals.global_dir = args.dir
    Globals.global_dbfilename = args.dbfilename

    server_set = ConnectionRedis()
    asyncio.run(main_loop(server_set))
    # execution will be blocked here until the main_loop is finished


if __name__ == "__main__":
    main()

import asyncio
from app.connection.ConnectionRedis import ConnectionRedis
from app.EventLoop import EventLoop


async def main_loop(server_set):
    while True:
        client_socket = await server_set.accept_client()
        loop = EventLoop(client_socket)
        asyncio.create_task(loop.start())  # Handle client asynchronously
        # print("Client handled asynchronously")


def main():
    print("Starting server...")
    server_set = ConnectionRedis()
    asyncio.run(main_loop(server_set))
    # execution will be blocked here until the main_loop is finished


if __name__ == "__main__":
    main()

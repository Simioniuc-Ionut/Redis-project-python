import asyncio

from app.EventLoop import EventLoop
from app.connection.ConnectionRedis import ConnectionRedis
from app.mediator.Mediator import Mediator
from app.command_pattern.commands.CommandPing.CommandPing import CommandPing
from app.command_pattern.invoker.InvokerCommands import InvokerCommands
from app.reciver.Receiver import Receiver
import socket  # noqa: F401


async def main_loop(server_set):
    while True:  # manage all connections in concurrent way
        client_socket = await server_set.accept_client()  # wait for client
        loop = EventLoop(client_socket)
        asyncio.create_task(loop.start_task())

        # daca clientu lse deconcteaza apelez opresc loop ul si inchid clientul
        # to do
        # client.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")


# singleton instance
server_set = ConnectionRedis()

# Event Loop
asyncio.run(main_loop(server_set))

if __name__ == "__main__":
    main()

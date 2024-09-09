"""
Receiver Class:
The Receiver class reads messages from the client,
 processes them,
  and notifies the Mediator with the parsed arguments.
"""
import asyncio

from app.command_pattern.commands.CommandPing.CommandPing import CommandPing


class Receiver:
    def __init__(self, client_socket, invoker):
        self.__client_socket = client_socket
        self.__invoker = invoker

    async def ping(self):
        await self.__client_socket.send(b"+PONG\r\n")

    def send_message(self, message):
        self.__process_messages(message)

    async def receive_message(self):
        return asyncio.get_event_loop().sock_recv(self.__client_socket, 1024)

    async def __process_messages(self, message):
        # ex : *3\r\n$3\r\nSET\r\n$4\r\nPING\r\n$7\r\nmyvalue\r\n
        if message:
            # debug
            # print(f"Received message: {message.decode()}")
            lines = message.decode().split("\r\n")

            if lines[0][:1] == "*":  # array
                await self.__process_array_message(lines)

        else:
            print("Error: No message received.")

    async def __process_array_message(self, lines):
        num_args = int(lines[0][1:])
        arguments = []
        index = 1
        for _ in range(num_args):
            index += 1  # move to the message line
            argument = lines[index]  # get the argument
            arguments.append(argument)
            index += 1  # move to the next complet line

        # debug
        print("Arguments:", arguments)
        await self.__process_commands("*", arguments)

    async def __process_commands(self, sender, event):
        if sender == "*":  # an array with responses
            for response in event:
                if response == "PING":
                    self.__invoker.set_commands([CommandPing(self.__client_socket)])
                    await  self.__invoker.execute_commands()

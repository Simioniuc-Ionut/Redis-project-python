import asyncio

from app.command_pattern.commands.CommandECHO import CommandECHO
from app.command_pattern.commands.CommandPing import CommandPing


class Receiver:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    async def receive_message(self):
        loop = asyncio.get_running_loop()
        return await loop.sock_recv(self.client_socket, 1024)

    async def send_message(self, message):
        loop = asyncio.get_running_loop()
        await loop.sock_sendall(self.client_socket, message)
        # is non blocking. recv is blocking
        # and will interrupt execution

    async def process_message(self, message, invoker):
        if message:
            lines = message.decode().split("\r\n")
            if lines[0][:1] == "*":
                await self._process_array_message(lines, invoker)
            else:
                print("Invalid message format")
        else:
            print("No message received")

    async def _process_array_message(self, lines, invoker):
        num_args = int(lines[0][1:])
        arguments = []
        index = 1
        for _ in range(num_args):
            index += 1
            argument = lines[index]
            arguments.append(argument)
            index += 1

        print("Arguments:", arguments)
        await self._process_commands(arguments, invoker)

    async def _process_commands(self, arguments, invoker):
        if "PING" in arguments:
            invoker.add_command(CommandPing(self))
            await invoker.execute_commands()
        elif "ECHO" in arguments:
            # BUlk string : EX : $5\r\nhello\r\n
            message = ""
            for msg in arguments:
                if msg != "ECHO":
                    message = "$" + str(len(msg)) + "\r\n" + msg + "\r\n"
            invoker.add_command(CommandECHO(self, message))
            await invoker.execute_commands()
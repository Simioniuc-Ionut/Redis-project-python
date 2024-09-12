import asyncio

from app.command_pattern.ProcessCommands import process_ping, process_echo, process_set, process_get, process_config_get, process_keys


class Receiver:
    def __init__(self, client_socket, keys):
        self.client_socket = client_socket
        self.own_map = keys

    async def receive_message(self):
        loop = asyncio.get_running_loop()
        return await loop.sock_recv(self.client_socket, 1024)

    async def send_message(self, message):
        loop = asyncio.get_running_loop()
        await loop.sock_sendall(self.client_socket, message)
        # is non-blocking. recv is blocking
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
        await self._handle_commands(arguments, invoker)

    async def _handle_commands(self, arguments, invoker):
        command = arguments[0].upper()
        if command == "PING":
            await process_ping(self, invoker)
        elif command == "ECHO":
            await process_echo(self, arguments, invoker)
        elif command == "SET":
            await process_set(self, arguments, invoker)
        elif command == "GET":
            await process_get(self, arguments, invoker)
        elif command == "CONFIG" and arguments[1].upper() == "GET":
            await process_config_get(self, arguments[2], invoker)
        elif command == "KEYS":
            await process_keys(self, arguments, invoker)


import asyncio


class Receiver:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    async def receive_message(self):
        loop = asyncio.get_running_loop()
        return await loop.sock_recv(self.client_socket, 1024)

    async def send_message(self, message):
        loop = asyncio.get_running_loop()
        await loop.sock_sendall(self.client_socket, message)

    async def process_message(self, message):
        if message:
            lines = message.decode().split("\r\n")
            if lines[0][:1] == "*":
                await self._process_array_message(lines)
            else:
                print("Invalid message format")
        else:
            print("No message received")

    async def _process_array_message(self, lines):
        num_args = int(lines[0][1:])
        arguments = []
        index = 1
        for _ in range(num_args):
            index += 1  # Move to the message line
            argument = lines[index]
            arguments.append(argument)
            index += 1

        print("Arguments:", arguments)
        await self._process_commands(arguments)

    async def _process_commands(self, arguments):
        if "PING" in arguments:
            await self.send_message(b"+PONG\r\n")

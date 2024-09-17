# Commands
from app.command_pattern.commands.Command import Command


class CommandPing(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    async def execute(self):
        await self.receiver.send_message(b"+PONG\r\n")


class CommandPingReplication(CommandPing):

    def __init__(self, reader, writer):
        super().__init__(receiver=None)
        self.reader = reader
        self.writer = writer

    async def execute(self):
        # Business logic for server-replication communication
        ping_message = "*1\r\n$4\r\nPING\r\n"
        self.writer.write(ping_message.encode())
        await self.writer.drain()

        print("PING sent to master.")

        # Wait response from master
        self.response = await self.reader.read(100)
        print(f"Received: {self.response.decode()}")
        return self.response


from app.command_pattern.commands.Command import Command


class CommandGET(Command):
    def __init__(self, receiver, receiver_own_map, key):
        self.receiver = receiver
        self.key = key
        self.map = receiver_own_map

    async def execute(self):
        if self.key not in self.map:
            await self.receiver.send_message(b"$-1\r\n")
        else:
            value = self.map[self.key]
            message = "$" + str(len(value)) + "\r\n" + value + "\r\n"
            # debug
            print("CommandGET execute , msg is " + message)
            await self.receiver.send_message(message.encode())

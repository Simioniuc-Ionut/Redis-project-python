from app.command_pattern.commands.Command import Command


class CommandKEYS(Command):
    def __init__(self, receiver, pattern):
        self.receiver = receiver
        self.keys = receiver.own_map
        self.pattern = pattern

    async def execute(self):
        import fnmatch
        filtered_keys = fnmatch.filter(self.keys.keys(), self.pattern)
        # print("Filtered keys:", filtered_keys)  # debug
        message = "*" + str(len(filtered_keys)) + "\r\n"
        for key in filtered_keys:
            message += "$" + str(len(key)) + "\r\n" + key + "\r\n"
        await self.receiver.send_message(message.encode())

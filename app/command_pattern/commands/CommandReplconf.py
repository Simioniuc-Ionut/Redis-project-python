from app.command_pattern.commands.Command import Command

"""
This command is recevied from the replica to the server
"""
class CommandReplconf(Command):

    def __init__(self, receiver, option, value):
        self.receiver = receiver
        self.option = option
        self.value = value

    async def execute(self):
        response = f"+OK\r\n"
        #debug
        print("Replconf option:", self.option, " value:", self.value)
        await self.receiver.send_message(response.encode())

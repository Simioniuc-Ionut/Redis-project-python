from app.command_pattern.commands.Command import Command
from app import Globals


class CommandInfo(Command):

    def __init__(self, receiver):
        self.receiver = receiver
        self.role = Globals.global_role
        self.port = Globals.global_port
        self.master_replied = "8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb"  # provizorii
        self.master_repl_offset = 0  # provizorii

    async def execute(self):
        if self.role != "master":
            self.role = "slave"
        message = f"role:{self.role}\r\nmaster_repl_offset:{self.master_repl_offset}\r\nmaster_replid:{self.master_replied}"
        message = "$" + str(len(message)) + "\r\n" + message + "\r\n"
        print("Message:", message)
        await self.receiver.send_message(message.encode())
from app.command_pattern.commands.Command import Command

class CommandPsync(Command):

    def __init__(self, receiver, replid , offset):
        self.receiver = receiver
        self.offset = offset
        self.replid_from_master = replid

    async def execute(self):
        """
         The master needs to respond with +FULLRESYNC <REPL_ID> 0\r\n ("FULLRESYNC 0" encoded as a RESP Simple String). Here's what the response means:
         FULLRESYNC means that the master cannot perform incremental replication with the replica, and will thus start a "full" resynchronization.
         <REPL_ID> is the replication ID of the master. You've already set this in the "Replication ID & Offset" stage.
         As an example, you can hardcode 8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb as the replication ID.
         0 is the replication offset of the master. You've already set this in the "Replication ID & Offset" stage.
         """
        # debug
        print("PSYNC arguments ,send ok")
        the_offset_response = 0
        if self.offset > -1:
            the_offset_response = self.offset

        print("replication_id:", self.replid_from_master, " replication_offset:", the_offset_response)

        response = f"+FULLRESYNC {self.replid_from_master} {the_offset_response}\r\n"
        await self.receiver.send_message(response.encode())
        print("Psync response sent.")
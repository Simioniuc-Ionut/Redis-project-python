from app.command_pattern.commands.Command import Command


class CommandSendRdbFile(Command):
    def __init__(self, receiver, file_path):
        self.receiver = receiver
        self.file_path = file_path

    async def execute(self):
        """
        return:  $<length_of_file>\r\n<contents_of_file>
        """
        # we will send an hex file
        rdb_hex = "524544495330303131fa0972656469732d76657205372e322e30fa0a72656469732d62697473c040fa056374696d65c26d08bc65fa08757365642d6d656dc2b0c41000fa08616f662d62617365c000fff06e3bfec0ff5aa2"
        rdb_content = bytes.fromhex(rdb_hex)  # Convert the hex string to binary data
        rdb_length_of_data = f"${len(rdb_content)}\r\n".encode()  # Construct the length of the data
        response = rdb_length_of_data + rdb_content  # Construct the response with raw binary
        # data
        print("RDB file sent.")
        print("RDB file , the response is:", response)
        await self.receiver.send_message(response)




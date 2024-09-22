from app.command_pattern.commands.Command import Command


class CommandWait(Command):
    """
    The WAIT command.
    """

    def __init__(self, receiver, numreplicas, timeout):
        """
        Initialize the command.

        Parameters:
        receiver (object): The receiver object that will handle the response.
        numreplicas (int): The number of replicas to wait for.
        timeout (int): The timeout in milliseconds.
        """
        super().__init__(receiver)
        self.numreplicas = numreplicas
        self.timeout = timeout

    async def execute(self):
        """
        Execute the command.
        """
        # response = f":{self.numreplicas}\r\n"
        response = self.numreplicas
        await self.receiver.send_message(response.encode())

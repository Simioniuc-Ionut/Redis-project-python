from app.command_pattern.commands.Command import Command


class CommandWait(Command):
    """
    The WAIT command.
    """

    def __init__(self, receiver, nr_replicas, timeout):
        """
        Initialize the command.

        Parameters:
        receiver (object): The receiver object that will handle the response.
        numreplicas (int): The number of replicas to wait for.
        timeout (int): The timeout in milliseconds.
        """
        super().__init__(receiver)
        self.nr_replicas = nr_replicas
        self.timeout = timeout

    async def execute(self):
        """
        Execute the command.
        """
        response = f":{self.nr_replicas}\r\n"
        # response = self.nr_replicas
        await self.receiver.send_message(response.encode())

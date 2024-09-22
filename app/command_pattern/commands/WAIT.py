from app.command_pattern.ProcessCommandsToReplicas import propagate_wait_command_to_replicas
from app.command_pattern.commands.Command import Command
from app import Globals

class CommandWait(Command):
    """
    The WAIT command.
    """

    def __init__(self, receiver, nr_replicas, milliseconds, replicas_connections):
        """
        Initialize the command.

        Parameters:
        receiver (object): The receiver object that will handle the response.
        numreplicas (int): The number of replicas to wait for.
        timeout (int): The timeout in milliseconds.
        """
        super().__init__(receiver)
        self.nr_replicas = nr_replicas
        self.replicas_connections = replicas_connections
        self.milliseconds = milliseconds

    async def execute(self):
        """
        Execute the command.
        """
        replicas_connections = self.replicas_connections

        # Propagate the WAIT command to all replicas and wait for acknowledgments
        acknowledged_replicas = await propagate_wait_command_to_replicas(replicas_connections,
                                                                         self.milliseconds)
        if acknowledged_replicas >= self.nr_replicas:
            print("All replicas acknowledged the command ,", acknowledged_replicas, " replicas", self.nr_replicas)
        else:
            print("Not all replicas acknowledged the command ,", acknowledged_replicas, " replicas", self.nr_replicas)

            # Return the number of replicas that acknowledged the command
        response = ""
        if not Globals.global_no_commads:
            response = f":{acknowledged_replicas}\r\n"
        else:
            response = f":{len(self.replicas_connections)}\r\n"
            print("No commands to execute")

        await self.receiver.send_message(response.encode())  # receiver will be the client connection that send
        # the command

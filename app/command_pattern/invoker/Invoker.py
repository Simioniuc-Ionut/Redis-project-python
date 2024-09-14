"""
InvokerCommands Class: Executes commands based
on the notifications received from the Mediator.

Attributes:
    _commands (list): A list to store the commands to be executed.
"""


class Invoker:
    def __init__(self):
        """
        Initialize the Invoker with an empty list of commands.
        """
        self._commands = []

    def add_command(self, command):
        """
        Add a command to the list of commands.

        Parameters:
        command (object): The command to be added.
        """
        self._commands.append(command)

    async def execute_commands(self):
        """
        Execute all the commands in the list asynchronously and clear the list.
        """
        for command in self._commands:
            await command.execute()
        self._commands.clear()

"""
InvokerCommands Class: Executes commands based
on the notifications received from the Mediator.
"""


class InvokerCommands:
    def __init__(self):
        self._commands = []

    def set_commands(self, commands):
        self._commands = commands

    def execute_commands(self):
        for command in self._commands:
            command.execute()
        self._commands.clear()

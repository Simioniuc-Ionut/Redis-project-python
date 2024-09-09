"""
InvokerCommands Class: Executes commands based
on the notifications received from the Mediator.
"""


class Invoker:
    def __init__(self):
        self._commands = []

    def add_command(self, command):
        self._commands.append(command)

    async def execute_commands(self):
        for command in self._commands:
            await command.execute()
        self._commands.clear()

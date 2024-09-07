from app.command_pattern.commands.CommandPing.CommandPing import CommandPing

"""
Mediator Class: Manages communication between the 
Receiver and the InvokerCommands.
"""
class Mediator:
    def __init__(self):
        self._receiver = None
        self._invoker = None

    def set_receiver(self, receiver):
        self._receiver = receiver

    def set_invoker(self, invoker):
        self._invoker = invoker

    def notify(self, sender, event):
        if sender == "*": # an array with responses
            for response in event:
                if response == "PING":
                    self._invoker.set_commands([CommandPing(self._receiver)])
                    self._invoker.execute_commands()
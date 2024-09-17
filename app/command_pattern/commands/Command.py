from abc import ABC, abstractmethod


# Command Interface
class Command(ABC):
    """
    Abstract base class for Command interface in the command pattern.

    Methods:
    execute(): Abstract method to be implemented by concrete command classes.
    """

    @abstractmethod
    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        """
        Abstract method to execute the command.

        This method should be overridden by subclasses to provide the specific command execution logic.
        """
        pass

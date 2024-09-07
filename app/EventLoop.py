import asyncio

from app.command_pattern.invoker.InvokerCommands import InvokerCommands
from app.mediator.Mediator import Mediator
from app.reciver.Receiver import Receiver


class EventLoop:
    def __init__(self, client_socket):
        self._is_running = True
        self.events = {}  # handle different types of events
        self.client_socket = client_socket
        self._mediator = None

    def start_task(self):
        self.__initiate()

        while self._is_running:  # here manage communication between server - client
            message = self.wait_message_from_receiver()
            if not message:  # connection is closed
                print("Client disconnected")
                self.client_socket.close()
                self._is_running = False
            else:
                # debug
                print(f"Message received: {message}")
                self.send_message_to_receiver(message)

    def __initiate(self):
        self._mediator = Mediator()
        client_receiver = Receiver(self.client_socket, self._mediator)
        server_invoker = InvokerCommands()

        self._mediator.set_receiver(client_receiver)
        self._mediator.set_invoker(server_invoker)
        # debug
        print("Event Loop initiated")

    def wait_message_from_receiver(self):
        message = self._mediator.notify_invoker()
        return message

    def send_message_to_receiver(self, message):
        self._mediator.notify_receiver(message)

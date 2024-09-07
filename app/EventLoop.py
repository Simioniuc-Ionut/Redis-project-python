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

    async def wait_message_from_receiver(self):
        # Trebuie să fie asincronă
        try:
            message = await asyncio.get_event_loop().sock_recv(self.client_socket, 1024)
            return message
        except ConnectionResetError:
            return None

    # def send_message_to_receiver(self, message):
    #     self._mediator.notify_receiver(message)
    async def send_message_to_receiver(self, message):
        try:
            await asyncio.get_event_loop().sock_sendall(self.client_socket, message)
        except BrokenPipeError:
            self._is_running = False

    # async def start_task(self):
    #     self.__initiate()
    #     print("Event Loop started")
    #     while self._is_running:  # here manage communication between server - client
    #         message = await self.wait_message_from_receiver()  # wait message from client
    #         if message:  # connection is closed
    #             if message == b"":
    #                 print("Client disconnected")
    #                 self.client_socket.close()
    #                 self._is_running = False
    #             else:
    #                 # debug
    #                 # print(f"Message received: {message}")
    #                 self.send_message_to_receiver(message)
    async def start_task(self):
        print("Event Loop started")
        while self._is_running:
            message = await self.wait_message_from_receiver()
            if not message:
                print("Client disconnected")
                self.client_socket.close()
                self._is_running = False
            else:
                print(f"Message received: {message}")
                if message == b"*1\r\n$4\r\nPING\r\n":
                    response = b"+PONG\r\n"
                    await self.send_message_to_receiver(response)

    def __initiate(self):
        self._mediator = Mediator()
        client_receiver = Receiver(self.client_socket, self._mediator)
        server_invoker = InvokerCommands()

        self._mediator.set_receiver(client_receiver)
        self._mediator.set_invoker(server_invoker)
        # debug
        print("Event Loop initiated")

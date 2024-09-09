import asyncio

from app.command_pattern.invoker.InvokerCommands import InvokerCommands
from app.mediator.Mediator import Mediator
from app.reciver.Receiver import Receiver


class EventLoop:
    def __init__(self, client_socket):
        self._is_running = True
        self.client_socket = client_socket
        self.client_recevier = None
        self.server_invoker = None
    async def wait_message_from_receiver(self):
        # Trebuie să fie asincronă
        return await asyncio.get_event_loop().sock_recv(self.client_socket, 1024)

    async def send_message_to_receiver(self, message):
        await self.client_receiver.send_message(message)

    async def start_task(self):
        self.__initiate()
        print("Event Loop started")
        while self._is_running:  # here manage communication between server - client
            message = await self.wait_message_from_receiver()  # wait message from client
            if message:  # connection is closed
                if message == b"":
                    print("Client disconnected")
                    self.client_socket.close()
                    self._is_running = False
                else:
                    # debug
                    # print(f"Message received: {message}")
                    await self.send_message_to_receiver(message)

    def __initiate(self):
        self.server_invoker = InvokerCommands()
        self.client_receiver = Receiver(self.client_socket, self.server_invoker)
        # debug
        print("Event Loop initiated")

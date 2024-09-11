import asyncio
from app.reciver.Receiver import Receiver
from app.command_pattern.invoker.Invoker import Invoker


class EventLoop:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.receiver = Receiver(client_socket)
        self.invoker = Invoker()
        self._is_running = True

    async def start(self):
        print("Event Loop started")
        while self._is_running:
            message = await self.receiver.receive_message()
            if message == b"":
                print("Client disconnected")
                self.client_socket.close()
                self._is_running = False
            else:
                await self.receiver.process_message(message, self.invoker)

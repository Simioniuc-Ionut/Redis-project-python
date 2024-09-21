import asyncio
from app.reciver.Receiver import Receiver
from app.command_pattern.invoker.Invoker import Invoker

class EventLoop:
    """
    EventLoop class manages the asynchronous event loop for handling client connections and processing messages.

    Attributes:
    client_socket (socket.socket): The client socket for communication.
    receiver (Receiver): The receiver object for handling incoming messages.
    invoker (Invoker): The invoker object for managing command execution.
    _is_running (bool): A flag indicating whether the event loop is running.
    """

    def __init__(self, client_socket, keys):
        """
        Initialize the EventLoop with a client socket and a key-value store.

        Parameters:
        client_socket (socket.socket): The client socket for communication.
        keys (dict): The dictionary representing the key-value store.
        """
        self.client_socket = client_socket
        self.receiver = Receiver(client_socket, keys)
        self.invoker = Invoker()
        self._is_running = True

    async def start(self, is_master=False):
        """
        Start the event loop to receive and process messages from the client or master.

        This method runs an infinite loop to receive messages from the client socket(or master socket),
        process them using the receiver, and execute the corresponding commands.
        The loop terminates when the client disconnects.
        """
        print("Event Loop started")
        count = 0
        while self._is_running:
            if count == 2:
                break
            try:
                if self.client_socket.fileno() == -1:  # check if the socket is closed by using descriptor
                    print("Socket is closed before reading message", self.client_socket)
                    self._is_running = False
                    # self.client_socket.close()
                    break
                # verify if the socket is still connected
                try:
                    message = await self.receiver.receive_message()
                except ConnectionResetError as e:
                    print(f"ConnectionResetError: {e}")
                    self._is_running = False
                    # self.client_socket.close()
                    break

                if is_master:
                    print("Message received from master ", message)
                    # count += 1
                else:
                    print("Message received from client ", message)
                if message == b"":
                    print("Client disconnected ", self.client_socket)
                    # self.client_socket.close()
                    self._is_running = False
                    break
                else:
                    await self.receiver.process_message(message, self.invoker)
            except OSError as e:
                print(f"OSError: {e} and error ", self.client_socket)
                self._is_running = False
                # self.client_socket.close()
            except asyncio.CancelledError:
                print("Event loop was cancelled")
                self._is_running = False
                # self.client_socket.close()
            except Exception as e:
                print(f"Unexpected error: {e}")
                self._is_running = False
                # self.client_socket.close()
            finally:
                if not self._is_running:
                    print("Cleaning up resources ", self.client_socket)
                    self.client_socket.close()

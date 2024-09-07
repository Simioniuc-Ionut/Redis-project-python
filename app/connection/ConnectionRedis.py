import asyncio
import socket  # noqa: F401


class ConnectionRedis:
    _instance = None  # used for singleton implementation

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionRedis, cls).__new__(cls)
            cls._instance._server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
            cls._instance._client_socket = None
        return cls._instance

    def accept_client(self):
        # Trebuie să fie asincronă
        # self._instance._client_socket, _address = await asyncio.get_event_loop().sock_accept(self._instance._server_socket)

        # return self._instance._client_socket  # returnează socketul clientului
        self._instance._client_socket,_addr = self._instance._server_socket.accept()  # wait for client
        return self._instance._client_socket,_addr
    def close(self):
        """
        Closes the connection to the Redis server.
        """
        if self._instance._client_socket:
            self._instance._client_socket.close()
        self._instance._server_socket.close()

    def send(self, message):
        """
        Sends a message to the client.
        Args:
        message (bytes): The message to send.
        """
        if self._instance._client_socket:
            self._instance._client_socket.sendall(message)
        else:
            print("Error: No client connected.")

    def receive(self, bufsize):
        """
        Receives a message from the client.
        Args:
           bufsize (int): The maximum amount of data to be received at once.
        Returns:
           bytes: The message received.
        """
        if self._instance._client_socket:
            return self._instance._client_socket.recv(bufsize)
        else:
            print("Error: No client connected.")
            return b""

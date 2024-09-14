import asyncio
import socket

class ConnectionRedis:
    """
    ConnectionRedis is a singleton class that manages the server socket for a Redis-like server.

    Attributes:
    _instance (ConnectionRedis): The singleton instance of the class.
    _server_socket (socket.socket): The server socket for accepting client connections.
    """

    _instance = None  # Singleton implementation

    def __new__(cls, port):
        """
        Create a new instance of ConnectionRedis if it doesn't already exist.

        Returns:
        ConnectionRedis: The singleton instance of the class.
        """
        if cls._instance is None:
            cls._instance = super(ConnectionRedis, cls).__new__(cls)
            cls._instance._server_socket = socket.create_server(("localhost", port), reuse_port=True)
            cls._instance._server_socket.setblocking(False)  # Non-blocking socket
        return cls._instance

    async def accept_client(self):
        """
        Accept a new client connection asynchronously.

        Returns:
        socket.socket: The client socket for the accepted connection.
        """
        loop = asyncio.get_running_loop()
        client_socket, address = await loop.sock_accept(self._instance._server_socket)
        print("Client connected", address)
        return client_socket

    def close(self):
        """
        Close the server socket.
        """
        self._instance._server_socket.close()
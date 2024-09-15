import asyncio
import socket


class ConnectionRedis:
    """
    ConnectionRedis is a singleton class that manages the server socket for a Redis-like server.

    Attributes:
    _instance (ConnectionRedis): The singleton instance of the class.
    _server_socket (socket.socket): The server socket for accepting client connections.
    _master_socket (socket.socket): The socket for connecting to the master server (for replication).
    """

    _instance = None  # Singleton implementation

    def __new__(cls, port=None, master_host=None, master_port=None):
        """
        Create a new instance of ConnectionRedis if it doesn't already exist.

        Returns:
        ConnectionRedis: The singleton instance of the class.
        """
        if cls._instance is None:
            cls._instance = super(ConnectionRedis, cls).__new__(cls)
            if port:
                cls._instance._server_socket = socket.create_server(("localhost", port), reuse_port=True)
                cls._instance._server_socket.setblocking(False)  # Non-blocking socket
            if master_host and master_port:
                cls._instance._master_socket = None
                cls._instance.master_host = master_host
                cls._instance.master_port = master_port
        return cls._instance

    async def accept_client(self):
        """
        Accept a new client connection asynchronously.

        Returns:
        socket.socket: The client socket for the accepted connection.
        """
        """
        client_socket in ConnectionRedis
        Purpose: Used to accept incoming client connections to the server.
        Implementation: Utilizes the socket module to create a server socket that listens for incoming connections.
        Usage: Typically used in server-side code to handle multiple client connections.
        """
        loop = asyncio.get_running_loop()
        client_socket, address = await loop.sock_accept(self._instance._server_socket)
        print("Client connected", address)
        return client_socket

    async def connect_master(self):
        """
        Connect to the master server asynchronously.

        Returns:
        tuple: The reader and writer streams for the master connection.
        """
        """
        open_connection
        Purpose: Used to establish a connection to a remote server.
        Implementation: Utilizes the asyncio module to create a connection to a specified host and port.
        Usage: Typically used in client-side code to connect to a server.
        Example:
        """
        reader, writer = await asyncio.open_connection(self.master_host, self.master_port)
        print(f"Connected to master at {self.master_host}:{self.master_port}")
        return reader, writer

    def close(self):
        """
        Close the server socket.
        """
        if self._server_socket:
            self._server_socket.close()
        if self._master_socket:
            self._master_socket.close()

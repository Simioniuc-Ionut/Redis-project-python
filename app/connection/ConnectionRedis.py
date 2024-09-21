import asyncio
import socket
from app import Globals

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
            # if master_host and master_port:
            #     cls._instance._master_socket = socket.create_connection((master_host, master_port))
            #     cls._instance.master_host = master_host
            #     cls._instance.master_port = master_port
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
        print("Client connected", address, " to a ", Globals.global_role, " server ")
        return client_socket

    def close(self):
        """
        Close the server socket.
        """
        print("Closing server socket from ConnectionRedis")
        if self._instance._server_socket:
            self._instance._server_socket.close()
            self._instance._server_socket = None
        # if self._instance._master_socket:
        #     self._instance._master_socket.close()
        #     self._instance._master_socket = None
        # ConnectionRedis._instance = None


 # def close(self, close_server=True, close_master=True):
 #        """
 #        Close the server and/or master socket.
 #
 #        Parameters:
 #        close_server (bool): Whether to close the server socket.
 #        close_master (bool): Whether to close the master socket.
 #        """
 #        if close_server and self._instance._server_socket:
 #            self._instance._server_socket.close()
 #            self._instance._server_socket = None
 #        if close_master and self._instance._master_socket:
 #            self._instance._master_socket.close()
 #            self._instance._master_socket = None
 #        if not self._instance._server_socket and not self._instance._master_socket:
 #            ConnectionRedis._instance = None
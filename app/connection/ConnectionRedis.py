import socket  # noqa: F401


class ConnectionRedis:
    _instance = None # used for singleton implementation

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionRedis, cls).__new__(cls)
            cls._instance._server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
            cls._instance._client_socket = None
        return cls._instance

    def accept_client(self):
        self._instance._client_socket, _address = self._instance._server_socket.accept()  # wait for client

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
        try:
            if self._instance._client_socket:
                self._instance._client_socket.sendall(message)
            else:
                print("Error: No client connected.")
        except BrokenPipeError:
            print("Error: Broken pipe. The client may have disconnected.")
            self._instance._client_socket.close()
            self._instance._client_socket = None

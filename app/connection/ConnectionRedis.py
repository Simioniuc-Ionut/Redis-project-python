import socket  # noqa: F401


class ConnectionRedis:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionRedis, cls).__new__(cls)
            cls._instance._client = socket.create_server(("localhost", 6379), reuse_port=True)
        return cls._instance

    def accept_client(self):
        return self._client.accept()  # wait for client
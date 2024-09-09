import asyncio
import socket


class ConnectionRedis:
    _instance = None  # Singleton implementation

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionRedis, cls).__new__(cls)
            cls._instance._server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
            cls._instance._server_socket.setblocking(False)  # Non-blocking socket
        return cls._instance

    async def accept_client(self):
        loop = asyncio.get_running_loop()
        client_socket, address = await loop.sock_accept(self._instance._server_socket)
        print("Client connected", address)
        return client_socket

    def close(self):
        self._instance._server_socket.close()

class Receiver:
    def __init__(self, client):
        self.__client = client

    def ping(self):
        self.__client.send("+PONG\r\n")

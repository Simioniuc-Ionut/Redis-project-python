class Receiver:
    def __init__(self, client):
        self.__client = client

    def ping(self):
        self.__client.send(b"+PONG\r\n")

    def process_messages(self):
        while True:
            message = self.__client.recv(1024) # read up to 1024 bytes
            if message:
                result = None
                # debug
                print(f"Received message: {message.decode()}")
                arguments = message.decode().split()[:1]
                arguments = arguments[1:]
                print(arguments + " arguments length ") # debug
                for args_length in range(0,arguments):
                    arg = message.decode().split()[args_length]
                    print(arg + "each arg") # debug
                    result +=arg + "\r\n"

                return result
            else:
                break
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
                lines = message.decode().split("\r\n")
                if(lines[0][:1] == "*"): # array
                    num_args = int(lines[0][1:])
                    print(" arguments length ")
                    arguments = []
                    index = 1
                    for _ in range(num_args):
                        length = int(lines[index][1:])  # get the length of the argument
                        arguments.append(argument)
                        index += 1

                    print("Arguments:", arguments)  # debug
                    return arguments
            else:
                break
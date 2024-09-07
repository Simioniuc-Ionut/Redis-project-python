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
                arguments = []
                lines = message.decode().split("\r\n")

                if(lines[0][:1] == "*"): # array
                    arguments = ["*"]  # array
                    num_args = int(lines[0][1:])
                    # ex : *3\r\n$3\r\nSET\r\n$4\r\nPING\r\n$7\r\nmyvalue\r\n

                    index = 1
                    for _ in range(num_args):
                        index += 1 # move to the message line
                        argument = lines[index]  # get the argument
                        arguments.append(argument)
                        index += 1 # move to the next complet line

                    print("Arguments:", arguments)  # debug
                    return arguments
            else:
                break
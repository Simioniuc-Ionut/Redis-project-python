from app.utils.Decorators import debug

"""
Receiver Class:
The Receiver class reads messages from the client,
 processes them,
  and notifies the Mediator with the parsed arguments.
"""
class Receiver:
    def __init__(self, client,mediator):
        self.__client = client
        self.__mediator = mediator

    @debug
    def ping(self):
        self.__client.send(b"+PONG\r\n")

    @debug
    def process_messages(self):
        while True:
            message = self.__client.recv(1024) # read up to 1024 bytes
            if message:
               arguments = []
               lines = message.decode().split("\r\n")

               if(lines[0][:1] == "*"): # array
                    num_args = int(lines[0][1:])
                    # ex : *3\r\n$3\r\nSET\r\n$4\r\nPING\r\n$7\r\nmyvalue\r\n

                    index = 1
                    for _ in range(num_args):
                        index += 1 # move to the message line
                        argument = lines[index]  # get the argument
                        arguments.append(argument)
                        index += 1 # move to the next complet line

                    self.__mediator.notify("*", arguments)
            else:
                break
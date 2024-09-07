"""
Receiver Class:
The Receiver class reads messages from the client,
 processes them,
  and notifies the Mediator with the parsed arguments.
"""


class Receiver:
    def __init__(self, client, mediator):
        self.__client = client
        self.__mediator = mediator

    def send_message(self, message):
        self.__process_messages(message)

    def __process_messages(self, message):
        # ex : *3\r\n$3\r\nSET\r\n$4\r\nPING\r\n$7\r\nmyvalue\r\n
        if message:
            # debug
            # print(f"Received message: {message.decode()}")
            lines = message.decode().split("\r\n")

            if lines[0][:1] == "*":  # array
                self.__process_array_message(lines)

        else:
            print("Error: No message received.")

    def __process_array_message(self, lines):
        num_args = int(lines[0][1:])
        arguments = []
        index = 1
        for _ in range(num_args):
            index += 1  # move to the message line
            argument = lines[index]  # get the argument
            arguments.append(argument)
            index += 1  # move to the next complet line

        # debug
        # print("Arguments:", arguments)
        self.__mediator.process_commands("*", arguments)

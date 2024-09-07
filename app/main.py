from app.connection.ConnectionRedis import ConnectionRedis
from app.command_pattern.commands.CommandPing.CommandPing import CommandPing
from app.command_pattern.invoker.InvokerCommands import InvokerCommands
from app.reciver.Receiver import Receiver
import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    #server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    #server_socket.accept()  # wait for client

    client = ConnectionRedis()
    client.accept_client()  # wait for client

    receiver = Receiver(client)
    invoker = InvokerCommands()

    # Set the command
    is_command_set = False
    command = None
    while True:
        responde = receiver.process_messages()
        print("in main command loop " + responde) # debug
        if responde.contains("PING"):
                is_command_set = True
                command = CommandPing(receiver)
        if is_command_set:
            invoker.set_commands([command])
            invoker.execute_commands()



    client.close()


if __name__ == "__main__":
    main()

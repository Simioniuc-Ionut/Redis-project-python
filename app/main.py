import connection.ConnectionRedis as Connection
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

    #client = Connection.ConnectionRedis()
    #client.accept_client()  # wait for client

    receiver = Receiver()

    #setez comanda
    command_ping = CommandPing(receiver)

    invoker = InvokerCommands()
    invoker.set_commands([command_ping])
    response = invoker.execute_commands()
    print(response) # This will print the response "+PONG\r\n"

if __name__ == "__main__":
    main()

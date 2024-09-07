from app.connection.ConnectionRedis import ConnectionRedis
from app.mediator.Mediator import Mediator
from app.command_pattern.commands.CommandPing.CommandPing import CommandPing
from app.command_pattern.invoker.InvokerCommands import InvokerCommands
from app.reciver.Receiver import Receiver
import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")


# Debug dictionary
debug_dict = {}

client = ConnectionRedis()
client.accept_client()  # wait for client

mediator = Mediator()
receiver = Receiver(client, mediator)
invoker = InvokerCommands()

mediator.set_receiver(receiver)
mediator.set_invoker(invoker)

while True:
    receiver.process_messages(debug_dict)

client.close()

if __name__ == "__main__":
    main()

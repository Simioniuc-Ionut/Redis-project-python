from app.command_pattern.commands.CommandConfigGET import CommandConfigGet
from app.command_pattern.commands.CommandECHO import CommandECHO
from app.command_pattern.commands.CommandGET import CommandGET
from app.command_pattern.commands.CommandInfo import CommandInfo
from app.command_pattern.commands.CommandKEYS import CommandKEYS
from app.command_pattern.commands.CommandEXPIRE import CommandExpire
from app.command_pattern.commands.CommandPing import CommandPing
from app.command_pattern.commands.CommandPsync import CommandPsync
from app.command_pattern.commands.CommandReplconf import CommandReplconf
from app.command_pattern.commands.CommandSET import CommandSET
from app import Globals

async def process_ping(receiver, invoker):
    """
    Process the PING command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    invoker (object): The invoker object that manages command execution.
    """
    invoker.add_command(CommandPing(receiver))
    await invoker.execute_commands()


async def process_echo(receiver, arguments, invoker):
    """
    Process the ECHO command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the ECHO command.
    invoker (object): The invoker object that manages command execution.
    """
    message = ""
    for msg in arguments:
        if msg != "ECHO":
            message = f"${len(msg)}\r\n{msg}\r\n"
    invoker.add_command(CommandECHO(receiver, message))
    await invoker.execute_commands()


async def process_set(receiver, arguments, invoker):
    """
    Process the SET command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the SET command.
    invoker (object): The invoker object that manages command execution.
    """
    key = arguments[1]
    value = arguments[2]
    invoker.add_command(CommandSET(receiver, key, value, receiver.own_map))

    # Handle options for the SET command
    if len(arguments) > 3:
        for i in range(3, len(arguments)):
            option = arguments[i].upper()
            if option == "PX":
                # Set the key with a timeout in milliseconds
                milliseconds = int(arguments[i + 1])
                print("Milliseconds:", milliseconds)
                invoker.add_command(CommandExpire(receiver, key, milliseconds, receiver.own_map, False))
            elif option == "EX":
                # Set the key with a timeout in seconds
                seconds = int(arguments[i + 1])
                invoker.add_command(CommandExpire(receiver, key, seconds, receiver.own_map, True))
    await invoker.execute_commands()


async def process_get(receiver, arguments, invoker):
    """
    Process the GET command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the GET command.
    invoker (object): The invoker object that manages command execution.
    """
    key = arguments[1]
    invoker.add_command(CommandGET(receiver, receiver.own_map, key))
    await invoker.execute_commands()


async def process_config_get(receiver, get_name, invoker):
    """
    Process the CONFIG GET command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    get_name (str): The name of the configuration parameter to get.
    invoker (object): The invoker object that manages command execution.
    """
    invoker.add_command(CommandConfigGet(receiver, get_name))
    await invoker.execute_commands()


async def process_keys(receiver, arguments, invoker):
    """
    Process the KEYS command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the KEYS command.
    invoker (object): The invoker object that manages command execution.
    """
    pattern = arguments[1]
    invoker.add_command(CommandKEYS(receiver, pattern))
    await invoker.execute_commands()


async def process_info(receiver, arguments, invoker):
    """
    Process the INFO command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the INFO command.
    invoker (object): The invoker object that manages command execution.
    """
    if arguments[1] == "replication":
        invoker.add_command(CommandInfo(receiver))
    await invoker.execute_commands()


async def process_replication_config(receiver, arguments, invoker):
    """
    Process the REPLCONF command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the REPLCONF command.
    invoker (object): The invoker object that manages command execution.
    """
    option = arguments[1]
    value = arguments[2]
    print("REPLCONF arguments ,send ok")
    invoker.add_command(CommandReplconf(receiver, option, value))
    await invoker.execute_commands()


async def process_psync(receiver, arguments, invoker):
    """
    Process the PSYNC command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the PSYNC command.
    invoker (object): The invoker object that manages command execution.
    """

    replication_id = arguments[1]  # if is ? because this is the first time the replica is connecting to the master.
    replication_offset = arguments[2]  # if is -1. is because this is the first time the replica is connecting to the master.

    invoker.add_command(CommandPsync(receiver, Globals.global_master_replica_id, replication_offset))
    await invoker.execute_commands()
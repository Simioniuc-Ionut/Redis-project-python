from app.command_pattern.ProcessCommandsToReplicas import process_propagation_send_SET_command_to_replicas
from app.command_pattern.commands.ConfigGET import CommandConfigGet
from app.command_pattern.commands.ECHO import CommandECHO
from app.command_pattern.commands.GET import CommandGET
from app.command_pattern.commands.Info import CommandInfo
from app.command_pattern.commands.KEYS import CommandKEYS
from app.command_pattern.commands.EXPIRE import CommandExpire
from app.command_pattern.commands.Ping import CommandPing
from app.command_pattern.commands.Psync import CommandPsync
from app.command_pattern.commands.Replconf import CommandReplconf
from app.command_pattern.commands.SET import CommandSET
from app import Globals
from app.command_pattern.commands.SendRdbFile import CommandSendRdbFile


async def add_and_execute_command(invoker, command):
    """
    Helper function to add a command to the invoker and execute it.

    Parameters:
    invoker (object): The invoker object that manages command execution.
    command (Command): The command to be added and executed.
    """
    invoker.add_command(command)
    await invoker.execute_commands()



async def process_ping(receiver, invoker):
    """
    Process the PING command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    invoker (object): The invoker object that manages command execution.
    """
    await add_and_execute_command(invoker, CommandPing(receiver))


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
    await add_and_execute_command(invoker, CommandECHO(receiver, message))


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
    await add_and_execute_command(invoker, CommandSET(receiver, key, value, receiver.own_map))
    # Handle options for the SET command
    if len(arguments) > 3:
        for i in range(3, len(arguments)):
            option = arguments[i].upper()
            if option == "PX":
                # Set the key with a timeout in milliseconds
                milliseconds = int(arguments[i + 1])
                print("Milliseconds:", milliseconds)
                await add_and_execute_command(invoker,
                                              CommandExpire(receiver, key, milliseconds, receiver.own_map, False))
                # Set the key with a timeout in seconds
                seconds = int(arguments[i + 1])
                await add_and_execute_command(invoker, CommandExpire(receiver, key, seconds, receiver.own_map, True))

    # if there are replica connections, propagate the SET command to them
    if Globals.global_replica_connections and Globals.global_role == "master":
        await process_propagation_send_SET_command_to_replicas(key, value)


async def process_get(receiver, arguments, invoker):
    """
    Process the GET command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the GET command.
    invoker (object): The invoker object that manages command execution.
    """
    key = arguments[1]
    await add_and_execute_command(invoker, CommandGET(receiver, receiver.own_map, key))


async def process_config_get(receiver, get_name, invoker):
    """
    Process the CONFIG GET command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    get_name (str): The name of the configuration parameter to get.
    invoker (object): The invoker object that manages command execution.
    """
    await add_and_execute_command(invoker, CommandConfigGet(receiver, get_name))


async def process_keys(receiver, arguments, invoker):
    """
    Process the KEYS command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the KEYS command.
    invoker (object): The invoker object that manages command execution.
    """
    pattern = arguments[1]
    await add_and_execute_command(invoker, CommandKEYS(receiver, pattern))


async def process_info(receiver, arguments, invoker):
    """
    Process the INFO command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the INFO command.
    invoker (object): The invoker object that manages command execution.
    """
    if arguments[1] == "replication":
        await add_and_execute_command(invoker, CommandInfo(receiver))


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
    await add_and_execute_command(invoker, CommandReplconf(receiver, option, value))


async def process_psync(receiver, arguments, invoker):
    """
    Process the PSYNC command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    arguments (list): The list of arguments for the PSYNC command.
    invoker (object): The invoker object that manages command execution.
    """

    replication_id = arguments[1]  # if is ? because this is the first time the replica is connecting to the master.
    replication_offset = arguments[
        2]  # if is -1. is because this is the first time the replica is connecting to the master.

    await add_and_execute_command(invoker, CommandPsync(receiver, Globals.global_master_replica_id, replication_offset))


async def process_send_rdb_file(receiver, invoker):
    """
    Process the PSYNC command.

    Parameters:
    receiver (object): The receiver object that will handle the response.
    invoker (object): The invoker object that manages command execution.
    """
    file_path = "app/empty.rdb"  # an empty rdb fle
    await add_and_execute_command(invoker, CommandSendRdbFile(receiver, file_path))




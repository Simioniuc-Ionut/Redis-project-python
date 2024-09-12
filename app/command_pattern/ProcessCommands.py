from app.command_pattern.commands.CommandConfigGET import CommandConfigGet
from app.command_pattern.commands.CommandECHO import CommandECHO
from app.command_pattern.commands.CommandGET import CommandGET
from app.command_pattern.commands.CommandKEYS import CommandKEYS
from app.command_pattern.commands.CommandPX import CommandPX
from app.command_pattern.commands.CommandPing import CommandPing
from app.command_pattern.commands.CommandSET import CommandSET


async def process_ping(receiver, invoker):
    invoker.add_command(CommandPing(receiver))
    await invoker.execute_commands()


async def process_echo(receiver, arguments, invoker):
    # BUlk string : EX : $5\r\nhello\r\n
    message = ""
    for msg in arguments:
        if msg != "ECHO":
            message = f"${len(msg)}\r\n{msg}\r\n"
    invoker.add_command(CommandECHO(receiver, message))
    await invoker.execute_commands()


async def process_set(receiver, arguments, invoker):
    key = arguments[1]
    value = arguments[2]
    invoker.add_command(CommandSET(receiver, key, value, receiver.own_map))

    # options
    if len(arguments) > 3:
        for i in range(3, len(arguments)):
            option = arguments[i].upper()
            if option == "PX":
                # set the key with a timeout in milliseconds
                milliseconds = arguments[i + 1]
                invoker.add_command(CommandPX(receiver, key, milliseconds, receiver.own_map))

    await invoker.execute_commands()


async def process_get(receiver, arguments, invoker):
    key = arguments[1]
    invoker.add_command(CommandGET(receiver, receiver.own_map, key))
    await invoker.execute_commands()


async def process_config_get(receiver, get_name, invoker):
    invoker.add_command(CommandConfigGet(receiver, get_name))
    await invoker.execute_commands()


async def process_keys(receiver, arguments, invoker):
    pattern = arguments[1]
    invoker.add_command(CommandKEYS(receiver, pattern))
    await invoker.execute_commands()

from app import Globals


async def process_propagation_send_SET_command_to_replicas(key, value):
    if Globals.global_replica_connections:
        for replica in Globals.global_replica_connections:
            message = f"*3\r\n$3\r\nSET\r\n${len(key)}\r\n{key}\r\n${len(value)}\r\n{value}\r\n"
            print("Sending SET command to replica")
            await replica.send_message(message.encode())





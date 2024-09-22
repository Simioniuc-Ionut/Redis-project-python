import asyncio
import asyncio.tasks
import concurrent.futures

from app import Globals


async def process_propagation_send_SET_command_to_replicas(key, value):
    Globals.global_no_commads = False
    if Globals.global_replica_connections:
        for replica in Globals.global_replica_connections:
            message = f"*3\r\n$3\r\nSET\r\n${len(key)}\r\n{key}\r\n${len(value)}\r\n{value}\r\n"
            print("Sending SET command to replica")
            await replica.send_message(message.encode())


def send_and_wait_for_ack(replica, milliseconds):
    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = f"*3\r\n$8\r\nREPLCONF\r\n$6\r\nGETACK\r\n$1\r\n*\r\n"
            loop.run_until_complete(replica.send_message(response.encode()))
            print(f"Sent MasterGetAck command to replica")

            data = loop.run_until_complete(asyncio.wait_for(replica.receive_message(), timeout=milliseconds / 1000))  # wait for the response from the replica
            if data:
                return 1
        except asyncio.TimeoutError:
            print("Timeout error: Did not receive response from replica in time")
        except Exception as e:
            print(f"Error sending MasterGetAck command to replica: {e}")
        finally:
            loop.close()
        return 0

    return run_in_thread()

async def propagate_wait_command_to_replicas(replicas_connections, milliseconds):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_and_wait_for_ack, replica, milliseconds) for replica in replicas_connections]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    print("Results: ", results)
    return sum(results)  # Count the number of successful responses

# async def propagate_wait_command_to_replicas(replicas_connections, milliseconds):
#     async def send_and_wait_for_ack(replica,milliseconds):
#         try:
#             response = f"*3\r\n$8\r\nREPLCONF\r\n$6\r\nGETACK\r\n$1\r\n*\r\n"
#             await replica.send_message(response.encode())
#             print(f"Sent MasterGetAck command to replica")
#             if milliseconds < 1000:
#                 milliseconds += 3500
#             data = await asyncio.wait_for(replica.receive_message(), timeout=milliseconds / 1000)  # wait for the response from the replica
#             # print(f"Received response from replica: {data}")
#             if data:
#                 return 1
#         except asyncio.TimeoutError:
#             print("Timeout error: Did not receive response from replica in time")
#         except Exception as e:
#             print(f"Error sending MasterGetAck command to replica: {e}")
#         return 0
#
#     tasks = [asyncio.create_task(send_and_wait_for_ack(replica,milliseconds)) for replica in replicas_connections]
#     results = await asyncio.gather(*tasks, return_exceptions=True)
#
#
#     print("Results: ", results)
#     return sum(results)  # Count the number of successful responses


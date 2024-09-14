import time
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app import Globals
from app.command_pattern.commands.CommandEXPIRE import CommandExpire


class RDBFileHandler(FileSystemEventHandler):
    """
    A class to handle file system events for RDB files.

    Attributes:
    filename (str): The name of the file to monitor.
    callback (function): The callback function to execute on file events.
    """

    def __init__(self, filename, callback):
        """
        Initialize the RDBFileHandler with a filename and a callback function.

        Parameters:
        filename (str): The name of the file to monitor.
        callback (function): The callback function to execute on file events.
        """
        self.filename = filename
        self.callback = callback

    def on_modified(self, event):
        """
        Handle the event when the monitored file is modified.

        Parameters:
        event (FileSystemEvent): The file system event.
        """
        if event.src_path.endswith(self.filename):  # src_path is the path of the file that was modified
            print(f"Detected modification in {self.filename}")
            self.callback()  # Trigger the callback to reload the RDB file

    def on_created(self, event):
        """
        Handle the event when the monitored file is created.

        Parameters:
        event (FileSystemEvent): The file system event.
        """
        if event.src_path.endswith(self.filename):
            print(f"Detected creation of {self.filename}")
            self.callback()  # Trigger the callback to load the RDB file


def start_monitoring_directory(directory, filename, callback):
    """
    Start monitoring a directory for changes to a specified file and trigger a callback when the file is created or modified.

    Parameters:
    directory (str): The path of the directory to be monitored.
    filename (str): The name of the file to be monitored.
    callback (function): The function to be called when the file is created or modified.

    Returns:
    Observer: The Observer object that monitors the specified directory.
    """
    event_handler = RDBFileHandler(filename, callback)  # Create an event handler for the RDB file
    observer = Observer()  # Create an observer object
    observer.schedule(event_handler, path=directory, recursive=False)
    observer.start()  # start thread to monitor the directory
    return observer  # return the observer object to allow stopping it later


async def load_rdb_file(directory, filename):
    """
    Load and process an RDB file from the specified directory.

    Parameters:
    directory (str): The path of the directory containing the RDB file.
    filename (str): The name of the RDB file to be loaded.
    """
    rdb_file_path = os.path.join(directory, filename)
    if os.path.exists(rdb_file_path):
        print(f"Loading RDB file from {rdb_file_path}")
        # Open and process file RDB
        with open(rdb_file_path, "rb") as file:  # open file in rb (read in binary mode)
            content = file.read()  # read the content of the file
            print("content is ", content)
            await _process_rdb_file(content)

    else:
        print(f"RDB file {rdb_file_path} not found.")


async def _process_rdb_file(content):
    """
       Process the content of an RDB file.

       Parameters:
       content (bytes): The content of the RDB file.
       """
    __process_header(content)  # header section of the RDB file
    offset = 9  # cursor to keep track of the current position in the content
    # keys = {}  # dictionary to store the keys and their values

    while offset < len(content):
        byte = content[offset]

        if byte == 0xFA:  # metadata section , have am string encoded
            offset += 1  # skip the metadata byte
            name_of_metadata_str, offset = __decode_string(content, offset)
            value_of_metadata_str, offset = __decode_string(content, offset)
            # print(" -- ", offset, " -- ", len(content), " name ", name_of_metadata_str, " value ",
            #       value_of_metadata_str)  # Debug info
        # special flags

        elif byte == 0xFE:  # database section
            offset += 1  # skip the database byte
            database_index, offset = __decode_size(content, offset)
            print("Database number is:", database_index, " offset is ", offset)
        elif byte == 0xFB:  # Hash db table
            """
            Indicates that hash table size information follows.
            - The size of the hash table that stores the keys and values (size encoded).
            - The size of the hash table that stores the expires of the keys (size encoded).
            """
            offset += 1  # Move past the FB byte

            # Decode the size of the hash table for keys and values
            hash_table_size, offset = __decode_size(content, offset)
            print("Hash table size is:", hash_table_size)

            # Decode the size of the hash table for expires
            expires_size, offset = __decode_size(content, offset)
            print("Expires size is:", expires_size)

            remained_hash_table = hash_table_size
            remained_expire_table = expires_size
            expire_time = 0
            is_seconds = False
            # Loop through the whole hash table
            while remained_hash_table > 0 or remained_expire_table > 0:
                # print("In while", hex(byte))
                print("Remained hash table is ", remained_hash_table, " remained expire table is ",
                      remained_expire_table)
                flag_byte = content[offset]  # flag byte indicating the value type
                if flag_byte == 0x00:  # string value
                    offset += 1  # Move past the flag byte
                    key, offset = __decode_string(content, offset)  # Decode the key
                    value, offset = __decode_string(content, offset)  # Decode the value

                    print(f"Key: {key}, Value: {value}")
                    Globals.global_keys[key] = value  # Store key-value in the dictionary
                    remained_hash_table -= 1  # Decrement the remaining hash table size
                    if expire_time != 0:  # we have expired UNIX timestamp
                        # print("Expire UNIX timestamp is ", expire_time, " is seconds ", is_seconds)
                        await wait_expire_time(expire_time, key, Globals.global_keys, is_seconds)
                        # print("After waiting for expire time")
                        expire_time = 0
                # Add additional handling for other types if needed, like:
                # elif flag_byte == 0x01:  # list value
                #    .
                elif flag_byte == 0xFC or flag_byte == 0xFD:  # timestamp expiry in milliseconds / seconds
                    if flag_byte == 0xFC:  # 8 bytes long
                        is_seconds = False
                    else:
                        is_seconds = True  # 4 bytes int
                    offset += 1
                    expire_time_remaining, offset = __decode_little_endian(content, offset, is_seconds)
                    expire_time = expire_time_remaining
                    remained_expire_table -= 1
            # print("Out of while")
        elif byte == 0xFF:  # END OF FILE section
            offset += 1
            remaining_content = content[offset:]
            checksum = sum(remaining_content)
            print("Checksum is:", checksum)
            break


def __process_header(content):
    """
        Process the header of the RDB file.

        Parameters:
        content (bytes): The content of the RDB file.
        """
    header = content[:9]  # first 9 bytes are the header
    magic_string = header[:5].decode('ascii')  # first 5 bytes are the magic string
    version = int(header[5:].decode('ascii'))  # next 4 bytes are the version
    print("header : magic string is ", magic_string, " version is ", version)
    # check if the magic string is correct
    if magic_string != "REDIS":
        raise ValueError("Invalid RDB file format")


def __decode_size(content, offset):
    """
    Decode the size using the Redis size encoding scheme.

    Parameters:
    content (bytes): The content of the RDB file.
    offset (int): The current offset in the content.

    Returns:
    tuple: The decoded size and the new offset after reading the value.
    """
    first_byte = content[offset]
    print(f"Decoding size, first_byte: {first_byte:02x}, offset: {offset}")  # Debug info

    if first_byte >> 6 == 0b00:
        # The value is encoded in the remaining 6 bits of the first byte
        value = first_byte & 0b00111111
        offset += 1
        print(f"Decoded size (6-bit): {value}, new offset: {offset}")  # Debug info
    elif first_byte >> 6 == 0b01:
        # The value is encoded in the remaining 6 bits of the first byte + 8 bits of the second byte
        value = ((first_byte & 0b00111111) << 8) | content[offset + 1]
        offset += 2
        print(f"Decoded size (14-bit): {value}, new offset: {offset}")  # Debug info
    elif first_byte >> 6 == 0b10:
        # The value is encoded in the next 4 bytes
        value = int.from_bytes(content[offset + 1:offset + 5], 'big')
        offset += 5
        print(f"Decoded size (32-bit): {value}, new offset: {offset}")  # Debug info
    elif first_byte == 0x0A:  # Length of previous entry case
        print(f"Previous entry length marker found at offset {offset}, byte: {first_byte:02x}")
        prev_length = first_byte  # Length is indicated by byte 0x0A
        offset += prev_length  # Move offset forward by the indicated length (10 in this case)
        print(f"Skipping {prev_length} bytes, new offset: {offset}")  # Debug info
        value = 0
    elif first_byte == 0xC0:  # Special case for redis-bits
        offset += 1  # Move past the C0 byte
        redis_bits = content[offset]  # The next byte represents redis-bits
        offset += 1
        print(f"Redis-bits: {redis_bits}")
        value = -1  # to represent the redis-bits
    else:
        print(f"Unknown size encoding at offset {offset}, first_byte: {first_byte:02x}")  # Debug info
        raise ValueError("Unknown size encoding")

    return value, offset


def __decode_string(content, offset):
    """
    Decode a string value from the content.

    Parameters:
    content (bytes): The content of the RDB file.
    offset (int): The current offset in the content.

    Returns:
    tuple: The decoded string value and the new offset after reading the value.
    """
    string_length, offset = __decode_size(content, offset)  # Decode the length of the string
    if string_length == -1:  # special case for redis-bits
        string_value = content[offset - 1]  # Extract the redis-bits
    else:
        string_value = content[offset:offset + string_length].decode('utf-8')  # Extract the string
        offset += string_length  # Move the offset forward
    return string_value, offset


# time stamp is decode in little endian
def __decode_little_endian(content, offset, is_seconds):
    """
        Decode a timestamp value in little-endian format.

        Parameters:
        content (bytes): The content of the RDB file.
        offset (int): The current offset in the content.
        is_seconds (bool): Whether the timestamp is in seconds or milliseconds.

        Returns:
        tuple: The decoded timestamp value and the new offset after reading the value.
        """
    if is_seconds:
        # seconds , unsigned int 32 bits
        str_length_of_time = 4
        value = int.from_bytes(content[offset: offset + str_length_of_time], 'little', signed=False)
    else:
        # milliseconds long
        str_length_of_time = 8
        value = int.from_bytes(content[offset: offset + str_length_of_time], 'little', signed=False)
    # value is in UNIX timestamp format

    offset += str_length_of_time
    return value, offset


async def wait_expire_time(expire_time_unix, key, keys, is_seconds):
    """
        Calculate the remaining time until a key expires and schedule its expiration.

        Parameters:
        expire_time_unix (int): The expiration time in UNIX timestamp format.
        key (str): The key to be expired.
        keys (dict): The dictionary of keys and their values.
        is_seconds (bool): Whether the expiration time is in seconds or milliseconds.
        """
    current_time = time.time()  # Obtain current time in seconds
    if not is_seconds:
        current_time *= 1000  # Convert to milliseconds if needed

    time_remaining = expire_time_unix - current_time  # Compute time remaining until expiry

    # debug
    # import datetime
    #
    # # Dacă value reprezintă milisecunde
    # timestamp = datetime.datetime.utcfromtimestamp(expire_time_unix / 1000)
    # print(f"Timestamp in human-readable format: {timestamp}")
    # print("REAL time remainging ", time_remaining, " curent time ", current_time, " expire unix time", expire_time_unix,
    #       " is seconds ", is_seconds)
    if time_remaining > 0:
        remaining_time = CommandExpire(None, key, time_remaining, keys, is_seconds)
        await remaining_time.execute()
    else:
        keys.pop(key, None)  # remove the key from the dictionary if the time is already expired

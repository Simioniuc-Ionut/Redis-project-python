import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class RDBFileHandler(FileSystemEventHandler):
    def __init__(self, filename, callback):
        self.filename = filename
        self.callback = callback

    def on_modified(self, event):
        if event.src_path.endswith(self.filename):  # src_path is the path of the file that was modified
            print(f"Detected modification in {self.filename}")
            self.callback()  # Trigger the callback to reload the RDB file

    def on_created(self, event):
        if event.src_path.endswith(self.filename):
            print(f"Detected creation of {self.filename}")
            self.callback()  # Trigger the callback to load the RDB file


"""
Starts monitoring a directory for changes to a specified file and triggers a callback when the file is created or modified.

Parameters:
- `directory` (str): The path of the directory to be monitored.
- `filename` (str): The name of the file to be monitored.
- `callback` (function): The function to be called when the file is created or modified.

Returns:
- `Observer`: The `Observer` object that monitors the specified directory.

This allows the application to automatically react to changes in the specified file within the monitored directory.
"""


def start_monitoring_directory(directory, filename, callback):
    event_handler = RDBFileHandler(filename, callback)  # Create an event handler for the RDB file
    observer = Observer()  # Create an observer object
    observer.schedule(event_handler, path=directory, recursive=False)
    observer.start()  # start thread to monitor the directory
    return observer  # return the observer object to allow stopping it later


def load_rdb_file(directory, filename):
    rdb_file_path = os.path.join(directory, filename)
    if os.path.exists(rdb_file_path):
        print(f"Loading RDB file from {rdb_file_path}")
        # Deschide și parcurge fișierul RDB
        # Aici trebuie să implementezi logica ta de încărcare a datelor
        # și actualizarea cheilor și valorilor în memorie.
        # De exemplu:
        with open(rdb_file_path, "rb") as file:  # open file in rb (read in binary mode)
            content = file.read()  # read the content of the file
            print("content is ", content)
            _process_rdb_file(content)

    else:
        print(f"RDB file {rdb_file_path} not found.")


def _process_rdb_file(content):
    __process_rdb_header(content) # header section of the RDB file


def __process_rdb_header(content):
    header = content[:9]  # first 9 bytes are the header
    magic_string = header[:5].decode('ascii')  # first 5 bytes are the magic string
    version = int(header[5:].decode('ascii'))  # next 4 bytes are the version
    print(" magic string is ", magic_string, " version is ", version)
    # check if the magic string is correct
    if magic_string != "REDIS":
        raise ValueError("Invalid RDB file format")

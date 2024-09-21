import asyncio

from app.ThreadSafeDict import ThreadSafeDict

global_dir = None
"""
global_dir (str): A global variable to store the directory path.
"""

global_dbfilename = None
"""
global_dbfilename (str): A global variable to store the database filename.
"""

global_keys = ThreadSafeDict()
"""
global_keys (dict): A global dictionary to store key-value pairs.
"""
global_role = "master"
global_master_replica_id = "8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb"
global_port = None
global_replica_connections = []


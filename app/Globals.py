from app.ThreadSafeDict import ThreadSafeDict

# Global variables for both master and replica servers
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

global_port = None

# Global variables specific to master server
global_role = "master"
global_master_replica_id = "8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb"
global_replica_connections = []

# Global variables specific to replica server
global_first_ack = False
global_offset = 0

# Project Documentation

## Overview

This project is a toy Redis clone built as part of the ["Build Your Own Redis" Challenge](https://codecrafters.io/challenges/redis). The implementation handles basic Redis commands like `PING`, `SET`, and `GET`, and includes features such as reading RDB files, decoding binary data, and more.

## Implementation Details

### Concepts Used

1. **Command Pattern**: The project uses the command pattern to handle different Redis commands. Each command is implemented as a class inheriting from an abstract `Command` class.
2. **Asynchronous Programming**: The project uses Python's `asyncio` library to handle asynchronous operations, ensuring non-blocking I/O.
3. **RESP Protocol**: The project implements the Redis Serialization Protocol (RESP) to communicate with clients.
4. **Observer Pattern**: Allows an object to notify other objects about changes in its state.
5. **Singleton Pattern**: Ensures ConnectionRedis class has only one instance and provides a global point of access to it.

### Key Components

- **Command Classes**: Each Redis command is implemented as a separate class (e.g., `CommandECHO`, `CommandConfigGet`).
- **Receiver**: The receiver class handles the actual communication with the client.
- **Globals**: A module to store global configuration parameters.

### Problems Solved

1. **Reading RDB Files**: Implemented functionality to read and parse Redis Database (RDB) files.
2. **Decoding Binary Data**: Added methods to decode binary data into readable formats.
3. **Handling Configuration Parameters**: Implemented commands to get configuration parameters like `dir` and `dbfilename`.
4. **Asynchronous Execution**: Ensured that commands execute asynchronously to avoid blocking operations.
## Testing and Output

### Screenshots

Include screenshots of your tests and their outputs here.

![Test Output 1](Test_Images/Redis2(1).png)
![Test Output 2](Test_Images/Redis2(2).png)
![Test Output 3](Test_Images/Redis2(3).png)
![Test Output 4](Test_Images/Redis2(4).png)
![Test Output 5](Test_Images/Redis2(5).png)
![Test Output 6](Test_Images/Redis2(6).png)
![Test Output 7](Test_Images/Redis2(7).png)
![Test Output 8](Test_Images/Redis2(8).png)
![Test Output 9](Test_Images/Redis2(9).png)
![Test Output 10](Test_Images/Redis2(10).png)
![Test Output 11](Test_Images/Redis2(11).png)
![Test Output 12](Test_Images/Redis2(12).png)
![Test Output 13](Test_Images/Redis2(13).png)
## References

- [Redis Protocol Specification](https://redis.io/topics/protocol)
- [Python `asyncio` Documentation](https://docs.python.org/3/library/asyncio.html)
- [Command Pattern](https://refactoring.guru/design-patterns/command)
- [Codecrafters Redis Challenge](https://codecrafters.io/challenges/redis)
- [Redis RDB File Format](https://rdb.fnordig.de/file_format.html#value-encoding)
## Troubleshooting

### Common Issues

#### `module 'socket' has no attribute 'create_server'`

This error occurs if you are using a Python version older than 3.8. Upgrade to Python 3.8 or later to resolve this issue.

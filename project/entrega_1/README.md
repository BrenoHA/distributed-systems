# Distributed File System BigFS

A simple distributed file system implementation using Python sockets.

## Overview

This project implements a client/server architecture that simulates a distributed file system. The system supports four basic file operations:

- **list (ls)**: View files and directories
- **remove (rm)**: Delete files or directories
- **copy (cp)**: Copy files or directories
- **get**: Download files or directories to the client

## Requirements

- Python 3.6+

## Setup

1. Clone this repository
2. Ensure the `server.py` and `client.py` files are executable

## Running the Server

```bash
python server.py
```

The server will:

- Start listening on 127.0.0.1:9999 (default)
- Create a `data` directory that acts as the root of the file system
- Wait for client connections

## Running the Client

```bash
python client.py
```

The client will:

- Connect to the server at 127.0.0.1:9999
- Present an interactive command prompt
- Create a `downloads` directory where files retrieved using `get` will be stored

## Client Commands

| Command                     | Description                                  | Example                         |
| --------------------------- | -------------------------------------------- | ------------------------------- |
| `ls` [path]                 | List contents of a directory or file details | `ls documents`                  |
| `rm <path>`                 | Remove a file or directory                   | `rm documents/report.txt`       |
| `cp <source> <destination>` | Copy a file or directory                     | `cp file1.txt backup/file1.txt` |
| `get <path>`                | Download a file or directory to client       | `get documents/data.csv`        |
| `help`                      | Display help information                     | `help`                          |
| `exit` or `quit`            | Exit the client                              | `exit`                          |

## Notes

- All paths are relative to the server's `data` directory
- When using `get` with a directory, the entire directory structure will be downloaded
- The client will create necessary subdirectories when downloading files

## Example Usage

server.py

```
$ python3 server.py
Server started on 127.0.0.1:9999
Root directory: /Users/user/documents/project/data
```

client.py

```
$ python client.py
Connected to server at 127.0.0.1:9999
Connected to the distributed file system.
Type 'help' for available commands or 'exit' to quit.

Enter command (ls, rm, cp, get, help, exit): ls
Contents of root directory:
documents/
test.txt (124 bytes)

Enter command (ls, rm, cp, get, help, exit): cp test.txt documents/test_copy.txt
File copied from test.txt to documents/test_copy.txt

Enter command (ls, rm, cp, get, help, exit): get documents
Downloaded 1 files from directory to downloads

Enter command (ls, rm, cp, get, help, exit): exit
Disconnected from server
```

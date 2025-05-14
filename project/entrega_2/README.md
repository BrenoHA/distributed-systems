# NFS (Network File System) Implementation

This is a simple implementation of a Network File System (NFS) using Python and TCP sockets. The system allows clients to perform basic file operations (list, copy, and delete) on both local and remote files.

## Features

- Server exports a local directory for remote access
- Client can perform operations on both local and remote files
- Supports multiple concurrent clients
- Thread-safe operations with proper locking
- Detailed logging of all operations
- Simple command-line interface

## Requirements

- Python 3.6+

## Project Structure

```
.
├── server.py      # NFS server implementation
├── client.py      # NFS client implementation
```

## Usage

### Starting the Server

1. Open a terminal and navigate to the project directory
2. Run the server:
   ```bash
   python server.py
   ```
   The server will start on localhost:5000 by default and export the `/tmp/nfs_export` directory.

### Using the Client

1. Open another terminal and navigate to the project directory
2. Run the client:
   ```bash
   python client.py
   ```
   By default, it connects to localhost:5000. You can specify a different host and port:
   ```bash
   python client.py --host <host> --port <port>
   ```

### Available Commands

The client supports the following commands:

1. **List files (ls)**

   - List files in a local directory:
     ```
     ls /path/to/local/directory
     ```
   - List files in a remote directory:
     ```
     ls remoto:/path/to/remote/directory
     ```

2. **Copy files (copy)**

   - Copy from local to remote:
     ```
     copy /path/to/local/file remoto:/path/to/remote/directory
     ```
   - Copy from remote to local:
     ```
     copy remoto:/path/to/remote/file /path/to/local/directory
     ```

3. **Delete files (delete)**

   - Delete a local file:
     ```
     delete /path/to/local/file
     ```
   - Delete a remote file:
     ```
     delete remoto:/path/to/remote/file
     ```

4. **Quit (quit)**
   - Exit the client:
     ```
     quit
     ```

## Protocol

The client and server communicate using a simple JSON-based protocol:

### Request Format

```json
{
    "command": "ls|copy|delete",
    "args": ["arg1", "arg2", ...]
}
```

### Response Format

```json
{
  "status": "success|error",
  "message": "Optional message",
  "files": [] // Only for ls command
}
```

## Logging

The server logs all operations to both the console and a file named `nfs_server.log`. Each log entry includes:

- Timestamp
- Client identifier
- Operation type
- Affected file/directory

Example log entry:

```
[2024-03-13 10:00:00] CLIENTE_127.0.0.1:12345 realizou operação 'ls' no diretório '/tmp/nfs_export'
```

## Security Considerations

This is a basic implementation and does not include:

- Authentication
- Encryption
- Access control
- File permissions

For production use, these security features should be implemented.

## Limitations

1. No support for large file transfers (limited by socket buffer size)
2. No automatic reconnection on connection loss
3. No caching mechanism
4. No support for file permissions
5. No support for symbolic links

## Future Improvements

1. Implement authentication and authorization
2. Add support for file permissions
3. Implement file transfer in chunks for large files
4. Add caching mechanism
5. Implement automatic reconnection
6. Add support for symbolic links
7. Implement file locking for concurrent access

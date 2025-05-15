import socket
import json
import os
import sys
import argparse

class NFSClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        
    def connect(self):
        """Connect to the NFS server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to NFS server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Error connecting to server: {str(e)}")
            return False
            
    def disconnect(self):
        """Disconnect from the NFS server"""
        if self.socket:
            self.socket.close()
            self.socket = None
            
    def send_request(self, command, args):
        """Send a request to the server"""
        if not self.socket:
            print("Not connected to server")
            return None
            
        request = {
            'command': command,
            'args': args
        }
        
        try:
            self.socket.send(json.dumps(request).encode())
            response = self.socket.recv(4096)
            return json.loads(response.decode())
        except Exception as e:
            print(f"Error sending request: {str(e)}")
            return None
            
    def ls(self, path):
        """List files in a directory"""
        response = self.send_request('ls', [path])
        if response and response['status'] == 'success':
            files = response['files']
            print(f"\nContents of {path}:")
            print("-" * 50)
            for file in files:
                type_str = "DIR" if file['is_dir'] else "FILE"
                size_str = f"{file['size']} bytes" if not file['is_dir'] else ""
                print(f"{type_str:<6} {file['name']} {size_str}")
            print("-" * 50)
        else:
            print(f"Error: {response['message'] if response else 'Unknown error'}")
            
    def copy(self, src, dst):
        """Copy a file"""
        response = self.send_request('copy', [src, dst])
        if response and response['status'] == 'success':
            print(f"Successfully copied {src} to {dst}")
        else:
            print(f"Error: {response['message'] if response else 'Unknown error'}")
            
    def delete(self, path):
        """Delete a file"""
        response = self.send_request('delete', [path])
        if response and response['status'] == 'success':
            print(f"Successfully deleted {path}")
        else:
            print(f"Error: {response['message'] if response else 'Unknown error'}")
            
    def show_help(self):
        """Display help information for all available commands"""
        help_text = """
Available Commands:
------------------
1. ls <path>
   List contents of a directory
   Example: ls /home/user/documents

2. copy <source_path> <destination_path>
   Copy a file from source to destination
   Example: copy /home/user/file.txt /home/user/backup/file.txt

3. delete <path>
   Delete a file
   Example: delete /home/user/old_file.txt

4. help
   Show this help message

5. quit
   Exit the client

Note: For remote paths, prefix them with 'remoto:'
Example: ls remoto:/documents
"""
        print(help_text)

def main():
    parser = argparse.ArgumentParser(description='NFS Client')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=5000, help='Server port')
    args = parser.parse_args()
    
    client = NFSClient(args.host, args.port)
    if not client.connect():
        sys.exit(1)
        
    try:
        while True:
            try:
                command_line = input("\nEnter command (ls/copy/delete/help/quit): ").strip()
                
                if command_line == 'quit':
                    break
                    
                # Split the command line into command and arguments
                parts = command_line.split()
                if not parts:
                    print("Invalid command. Type 'help' for available commands.")
                    continue
                    
                command = parts[0]
                args = parts[1:]
                
                if command == 'help':
                    client.show_help()
                elif command == 'ls':
                    if len(args) != 1:
                        print("Usage: ls <path>")
                        continue
                    client.ls(args[0])
                elif command == 'copy':
                    if len(args) != 2:
                        print("Usage: copy <source_path> <destination_path>")
                        continue
                    client.copy(args[0], args[1])
                elif command == 'delete':
                    if len(args) != 1:
                        print("Usage: delete <path>")
                        continue
                    client.delete(args[0])
                else:
                    print("Invalid command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                
    finally:
        client.disconnect()
        print("\nDisconnected from server")

if __name__ == '__main__':
    main() 
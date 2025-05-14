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
                command = input("\nEnter command (ls/copy/delete/quit): ").strip()
                
                if command == 'quit':
                    break
                    
                if command == 'ls':
                    path = input("Enter path: ").strip()
                    client.ls(path)
                    
                elif command == 'copy':
                    src = input("Enter source path: ").strip()
                    dst = input("Enter destination path: ").strip()
                    client.copy(src, dst)
                    
                elif command == 'delete':
                    path = input("Enter path: ").strip()
                    client.delete(path)
                    
                else:
                    print("Invalid command. Available commands: ls, copy, delete, quit")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                
    finally:
        client.disconnect()
        print("\nDisconnected from server")

if __name__ == '__main__':
    main() 
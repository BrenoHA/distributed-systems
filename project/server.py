import os
import socket
import json
import shutil
from pathlib import Path

class FileServer:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_dir = Path('data')
        
        # Create data directory if it doesn't exist
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True)
    
    def start(self):
        """Start the file server"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        print(f"Data directory: {self.data_dir.absolute()}")
        
        try:
            while True:
                client, address = self.socket.accept()
                print(f"Connection from {address}")
                self.handle_client(client)
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.socket.close()
    
    def handle_client(self, client_socket):
        """Handle client requests"""
        try:
            # Receive data from client
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                return
            
            # Parse the request
            request = json.loads(data)
            operation = request.get('operation')
            filename = request.get('filename')
            
            response = {'status': 'error', 'message': 'Invalid operation'}
            
            # Handle different operations
            if operation == 'create':
                content = request.get('content', '')
                response = self.create_file(filename, content)
            elif operation == 'read':
                response = self.read_file(filename)
            elif operation == 'update':
                content = request.get('content', '')
                response = self.update_file(filename, content)
            elif operation == 'delete':
                response = self.delete_file(filename)
            
            # Send response back to client
            client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            error_response = {'status': 'error', 'message': str(e)}
            client_socket.send(json.dumps(error_response).encode('utf-8'))
        finally:
            client_socket.close()
    
    def create_file(self, filename, content):
        """Create a new file with the given content"""
        try:
            file_path = self.data_dir / filename
            
            # Check if file already exists
            if file_path.exists():
                return {'status': 'error', 'message': f'File {filename} already exists'}
            
            # Create the file and write content
            with open(file_path, 'w') as f:
                f.write(content)
            
            return {'status': 'success', 'message': f'File {filename} created successfully'}
        except Exception as e:
            return {'status': 'error', 'message': f'Error creating file: {str(e)}'}
    
    def read_file(self, filename):
        """Read and return the content of a file"""
        try:
            file_path = self.data_dir / filename
            
            # Check if file exists
            if not file_path.exists():
                return {'status': 'error', 'message': f'File {filename} does not exist'}
            
            # Check if it's a directory
            if file_path.is_dir():
                # Return a list of files in the directory
                files = [f.name for f in file_path.iterdir()]
                return {'status': 'success', 'message': f'Directory contents retrieved', 'content': files, 'is_directory': True}
            
            # Read the file content
            with open(file_path, 'r') as f:
                content = f.read()
            
            return {'status': 'success', 'message': f'File {filename} read successfully', 'content': content, 'is_directory': False}
        except Exception as e:
            return {'status': 'error', 'message': f'Error reading file: {str(e)}'}
    
    def update_file(self, filename, content):
        """Update the content of an existing file"""
        try:
            file_path = self.data_dir / filename
            
            # Check if file exists
            if not file_path.exists():
                return {'status': 'error', 'message': f'File {filename} does not exist'}
            
            # Check if it's a directory
            if file_path.is_dir():
                return {'status': 'error', 'message': f'{filename} is a directory, cannot update'}
            
            # Update the file content
            with open(file_path, 'w') as f:
                f.write(content)
            
            return {'status': 'success', 'message': f'File {filename} updated successfully'}
        except Exception as e:
            return {'status': 'error', 'message': f'Error updating file: {str(e)}'}
    
    def delete_file(self, filename):
        """Delete the specified file"""
        try:
            file_path = self.data_dir / filename
            
            # Check if file exists
            if not file_path.exists():
                return {'status': 'error', 'message': f'File {filename} does not exist'}
            
            # Delete the file or directory
            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()
            
            return {'status': 'success', 'message': f'{filename} deleted successfully'}
        except Exception as e:
            return {'status': 'error', 'message': f'Error deleting file: {str(e)}'}

if __name__ == "__main__":
    server = FileServer()
    server.start() 
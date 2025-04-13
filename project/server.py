import socket
import os
import shutil
import json
import threading

class FileServer:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.root_dir = "data"
        
        # Create the root directory if it doesn't exist
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
    
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"BigFS Server started on {self.host}:{self.port}")
        print(f"Root directory: {os.path.abspath(self.root_dir)}")
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Client connected from {address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()
    
    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                try:
                    command_data = json.loads(data)
                    command = command_data.get('command')
                    
                    if command == 'ls':
                        response = self.list_files(command_data.get('path', ''))
                    elif command == 'rm':
                        response = self.remove_file(command_data.get('path', ''))
                    elif command == 'cp':
                        response = self.copy_file(
                            command_data.get('source', ''),
                            command_data.get('destination', '')
                        )
                    elif command == 'get':
                        response = self.get_file(command_data.get('path', ''))
                    else:
                        response = {"status": "error", "message": f"Unknown command: {command}"}
                    
                    client_socket.send(json.dumps(response).encode('utf-8'))
                except json.JSONDecodeError:
                    client_socket.send(json.dumps({
                        "status": "error", 
                        "message": "Invalid command format"
                    }).encode('utf-8'))
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
            print("Client disconnected")
    
    def list_files(self, path):
        full_path = os.path.join(self.root_dir, path)
        
        if not os.path.exists(full_path):
            return {"status": "error", "message": f"Path does not exist: {path}"}
        
        if os.path.isfile(full_path):
            file_stat = os.stat(full_path)
            return {
                "status": "success",
                "type": "file",
                "name": os.path.basename(full_path),
                "size": file_stat.st_size,
                "message": f"File: {os.path.basename(full_path)}, Size: {file_stat.st_size} bytes"
            }
        
        try:
            files = os.listdir(full_path)
            file_details = []
            
            for file in files:
                file_path = os.path.join(full_path, file)
                if os.path.isfile(file_path):
                    file_stat = os.stat(file_path)
                    file_details.append({
                        "name": file,
                        "type": "file",
                        "size": file_stat.st_size
                    })
                else:
                    file_details.append({
                        "name": file,
                        "type": "directory"
                    })
            
            return {
                "status": "success",
                "type": "directory",
                "files": file_details,
                "message": f"Contents of {path if path else 'root directory'}:"
            }
        except Exception as e:
            return {"status": "error", "message": f"Error listing files: {str(e)}"}
    
    def remove_file(self, path):
        if not path:
            return {"status": "error", "message": "No file path provided"}
        
        full_path = os.path.join(self.root_dir, path)
        
        if not os.path.exists(full_path):
            return {"status": "error", "message": f"File not found: {path}"}
        
        try:
            if os.path.isfile(full_path):
                os.remove(full_path)
                return {"status": "success", "message": f"File removed successfully: {path}"}
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
                return {"status": "success", "message": f"Directory and all contents removed: {path}"}
        except Exception as e:
            return {"status": "error", "message": f"Error removing file: {str(e)}"}
    
    def copy_file(self, source, destination):
        if not source or not destination:
            return {"status": "error", "message": "Source and destination paths are required"}
        
        source_path = os.path.join(self.root_dir, source)
        dest_path = os.path.join(self.root_dir, destination)
        
        if not os.path.exists(source_path):
            return {"status": "error", "message": f"Source not found: {source}"}
        
        # Create destination directory if it doesn't exist
        dest_dir = os.path.dirname(dest_path)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        try:
            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)
                return {"status": "success", "message": f"File copied from {source} to {destination}"}
            elif os.path.isdir(source_path):
                if os.path.exists(dest_path):
                    return {"status": "error", "message": f"Destination directory already exists: {destination}"}
                shutil.copytree(source_path, dest_path)
                return {"status": "success", "message": f"Directory copied from {source} to {destination}"}
        except Exception as e:
            return {"status": "error", "message": f"Error copying file: {str(e)}"}
    
    def get_file(self, path):
        if not path:
            return {"status": "error", "message": "No file path provided"}
        
        full_path = os.path.join(self.root_dir, path)
        
        if not os.path.exists(full_path):
            return {"status": "error", "message": f"File not found: {path}"}
        
        try:
            if os.path.isfile(full_path):
                with open(full_path, 'rb') as file:
                    file_content = file.read()
                
                return {
                    "status": "success",
                    "type": "file",
                    "name": os.path.basename(full_path),
                    "content": file_content.hex(),  # Send binary data as hex string
                    "message": f"File retrieved: {path}"
                }
            elif os.path.isdir(full_path):
                # For directories, we'll create a dictionary of files and their contents
                files_dict = {}
                for root, _, files in os.walk(full_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.root_dir)
                        with open(file_path, 'rb') as f:
                            files_dict[rel_path] = f.read().hex()
                
                return {
                    "status": "success",
                    "type": "directory",
                    "name": os.path.basename(full_path),
                    "files": files_dict,
                    "message": f"Directory contents retrieved: {path}"
                }
        except Exception as e:
            return {"status": "error", "message": f"Error retrieving file: {str(e)}"}

if __name__ == "__main__":
    server = FileServer()
    server.start() 
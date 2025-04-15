import socket
import json
import os
import binascii

class FileClient:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.client_socket = None
        self.download_dir = "downloads"
        
        # Create download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False
    
    def close(self):
        if self.client_socket:
            self.client_socket.close()
            print("Disconnected from server")
    
    def send_command(self, command_data):
        try:
            self.client_socket.send(json.dumps(command_data).encode('utf-8'))
            response = self.client_socket.recv(1024 * 1024).decode('utf-8')  # Allow for larger responses
            return json.loads(response)
        except Exception as e:
            print(f"Error communicating with server: {e}")
            return {"status": "error", "message": "Communication error with server"}
    
    def handle_command(self, command_line):
        if not command_line.strip():
            return "Please enter a command"
        
        parts = command_line.strip().split()
        command = parts[0].lower()
        
        if command == "exit":
            return None  # Signal to exit
        
        if command == "ls":
            path = parts[1] if len(parts) > 1 else ""
            return self.handle_list(path)
        
        elif command == "rm":
            if len(parts) < 2:
                return "Usage: rm <file/directory path>"
            path = parts[1]
            return self.handle_remove(path)
        
        elif command == "cp":
            if len(parts) < 3:
                return "Usage: cp <source> <destination>"
            source = parts[1]
            destination = parts[2]
            return self.handle_copy(source, destination)
        
        elif command == "get":
            if len(parts) < 2:
                return "Usage: get <file/directory path>"
            path = parts[1]
            return self.handle_get(path)
        
        elif command == "help":
            return self.show_help()
        
        else:
            return f"Unknown command: {command}\nType 'help' to see available commands"
    
    def handle_list(self, path):
        response = self.send_command({"command": "ls", "path": path})
        
        if response["status"] == "success":
            if response["type"] == "file":
                return response["message"]
            
            result = response["message"] + "\n"
            for file in response["files"]:
                if file["type"] == "file":
                    result += f"{file['name']} ({file['size']} bytes)\n"
                else:
                    result += f"{file['name']}/\n"
            return result
        else:
            return f"Error: {response['message']}"
    
    def handle_remove(self, path):
        response = self.send_command({"command": "rm", "path": path})
        return response["message"]
    
    def handle_copy(self, source, destination):
        response = self.send_command({
            "command": "cp", 
            "source": source, 
            "destination": destination
        })
        return response["message"]
    
    def handle_get(self, path):
        response = self.send_command({"command": "get", "path": path})
        
        if response["status"] == "success":
            if response["type"] == "file":
                file_name = response["name"]
                local_path = os.path.join(self.download_dir, file_name)
                
                # Create directory structure if needed
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                # Write the file content
                content = binascii.unhexlify(response["content"])
                with open(local_path, 'wb') as f:
                    f.write(content)
                
                return f"Downloaded file to {local_path}"
            
            elif response["type"] == "directory":
                files = response["files"]
                for rel_path, content_hex in files.items():
                    local_path = os.path.join(self.download_dir, rel_path)
                    
                    # Create directory structure if needed
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    
                    # Write the file content
                    content = binascii.unhexlify(content_hex)
                    with open(local_path, 'wb') as f:
                        f.write(content)
                
                return f"Downloaded {len(files)} files from directory to {self.download_dir}"
        
        return f"Error: {response['message']}"
    
    def show_help(self):
        return """
Available commands:
  ls [path]               - List contents of a directory or file details
  rm <path>               - Remove a file or directory
  cp <source> <dest>      - Copy a file or directory
  get <path>              - Download a file or directory to 'downloads' folder
  exit                    - Exit the client
        """
    
    def run(self):
        if not self.connect():
            return
        
        print("Connected to the distributed file system.")
        print("Type 'help' for available commands or 'exit' to quit.")
        
        try:
            while True:
                command = input("\nEnter command (ls, rm, cp, get, help, exit): ")
                result = self.handle_command(command)
                
                if result is None:  # Exit command
                    break
                
                print(result)
        except KeyboardInterrupt:
            print("\nClient shutting down...")
        finally:
            self.close()

if __name__ == "__main__":
    client = FileClient()
    client.run() 
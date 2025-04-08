import socket
import json
import sys
import os

class FileClient:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
    
    def connect(self):
        """Create a new socket connection to the server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            return True
        except ConnectionRefusedError:
            print(f"Could not connect to server at {self.host}:{self.port}")
            return False
    
    def send_request(self, request):
        """Send a request to the server and return the response"""
        if not self.connect():
            return {'status': 'error', 'message': 'Connection failed'}
        
        try:
            # Send the request
            self.socket.send(json.dumps(request).encode('utf-8'))
            
            # Get the response
            response = self.socket.recv(4096).decode('utf-8')
            return json.loads(response)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        finally:
            self.socket.close()
    
    def create_file(self, filename, content=''):
        """Create a new file on the server"""
        request = {
            'operation': 'create',
            'filename': filename,
            'content': content
        }
        response = self.send_request(request)
        return response
    
    def read_file(self, filename):
        """Read a file from the server"""
        request = {
            'operation': 'read',
            'filename': filename
        }
        response = self.send_request(request)
        return response
    
    def update_file(self, filename, content):
        """Update a file on the server"""
        request = {
            'operation': 'update',
            'filename': filename,
            'content': content
        }
        response = self.send_request(request)
        return response
    
    def delete_file(self, filename):
        """Delete a file from the server"""
        request = {
            'operation': 'delete',
            'filename': filename
        }
        response = self.send_request(request)
        return response

def display_menu():
    """Display the menu options"""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    print("===== FILE MANAGEMENT SYSTEM =====")
    print("1. Create File")
    print("2. Read File")
    print("3. Update File")
    print("4. Delete File")
    print("5. Exit")
    print("=================================")

def get_menu_choice():
    """Get user menu choice"""
    while True:
        try:
            choice = int(input("Enter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_file_content(response):
    """Display file content or directory listing"""
    if response['status'] != 'success':
        print(f"Error: {response['message']}")
        return
    
    if response.get('is_directory', False):
        print("\nDirectory contents:")
        for item in response['content']:
            print(f"  - {item}")
    else:
        print("\nFile content:")
        print("=" * 40)
        print(response['content'])
        print("=" * 40)

def main():
    client = FileClient()
    
    while True:
        display_menu()
        choice = get_menu_choice()
        
        if choice == 1:  # Create
            filename = input("Enter filename to create: ")
            content = input("Enter file content: ")
            response = client.create_file(filename, content)
            print(f"\nServer response: {response['message']}")
            
        elif choice == 2:  # Read
            filename = input("Enter filename to read: ")
            response = client.read_file(filename)
            if response['status'] == 'success':
                display_file_content(response)
            else:
                print(f"\nServer response: {response['message']}")
            
        elif choice == 3:  # Update
            filename = input("Enter filename to update: ")
            
            # First, read the current content
            read_response = client.read_file(filename)
            if read_response['status'] != 'success':
                print(f"\nServer response: {read_response['message']}")
                input("\nPress Enter to continue...")
                continue
                
            if read_response.get('is_directory', False):
                print("\nCannot update a directory")
                input("\nPress Enter to continue...")
                continue
                
            # Show current content
            print("\nCurrent content:")
            print("=" * 40)
            print(read_response['content'])
            print("=" * 40)
            
            # Get new content
            new_content = input("\nEnter new content (or press Enter to keep current content): ")
            
            # If no new content provided, use existing content
            if not new_content:
                new_content = read_response['content']
                
            # Update the file
            response = client.update_file(filename, new_content)
            print(f"\nServer response: {response['message']}")
            
        elif choice == 4:  # Delete
            filename = input("Enter filename to delete: ")
            response = client.delete_file(filename)
            print(f"\nServer response: {response['message']}")
            
        elif choice == 5:  # Exit
            print("\nExiting the program. Goodbye!")
            break
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 
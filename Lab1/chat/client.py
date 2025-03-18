import socket
import threading

def receive_messages(client_socket):
    """Listen for incoming messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024)
            print(f"New message: {message.decode('utf-8')}")
        except:
            print("Error receiving message.")
            break

def send_messages(client_socket):
    """Send messages to the server."""
    while True:
        message = input("Enter message (type 'exit' to quit): ")
        if message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))

def start_client(host='127.0.0.1', port=65432):
    """Start the chat client."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Connected to server!")

        # Create separate threads for sending and receiving messages
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
        send_messages(client_socket)

if __name__ == "__main__":
    start_client()

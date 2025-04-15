import socket
import threading

clients = []

def broadcast(message, client_socket):
    """Send a message to all clients except the sender."""
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove client if sending message fails
                clients.remove(client)

def handle_client(client_socket, client_address):
    """Handle the client's communication."""
    print(f"New connection from {client_address}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break  # If the client disconnects, stop handling it
            print(f"Message from {client_address}: {message.decode('utf-8')}")
            broadcast(message, client_socket)  # Broadcast the message to all clients
    except:
        print(f"Error handling client {client_address}")
    finally:
        # Clean up
        clients.remove(client_socket)
        client_socket.close()

def start_server(host='127.0.0.1', port=65432):
    """Start the chat server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    start_server()

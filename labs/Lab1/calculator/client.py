import socket

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            expression = input("Enter a mathematical expression (e.g., 2 + 3) or 'q' to quit: ")
            if expression.lower() == 'q':
                print("Exiting...")
                break
            s.sendall(expression.encode('utf-8'))
            data = s.recv(1024)
            print(f"Result: {data.decode('utf-8')}")

if __name__ == "__main__":
    start_client()

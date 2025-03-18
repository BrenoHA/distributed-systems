import socket
import threading

def calculate(expression):
    try:
        return eval(expression)
    except Exception as e:
        return str(e)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        expression = data.decode("utf-8")
        result = calculate(expression)
        conn.sendall(str(result).encode('utf-8'))
    conn.close()

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()

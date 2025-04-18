import socket

def calculate(expression):
    try:
        return eval(expression)  # This will evaluate simple math expressions like "2 + 3"
    except Exception as e:
        return str(e)

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                expression = data.decode("utf-8")
                result = calculate(expression)
                conn.sendall(str(result).encode('utf-8'))

if __name__ == "__main__":
    start_server()

import socket
import threading
import os
import json
import logging
import datetime
import shutil
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('nfs_server.log'),
        logging.StreamHandler()
    ]
)

class NFSServer:
    def __init__(self, host='localhost', port=5000, export_dir='/tmp/nfs_export'):
        self.host = host
        self.port = port
        self.export_dir = export_dir
        self.server_socket = None
        self.clients = {}
        self.lock = threading.Lock()
        
        # Create export directory if it doesn't exist
        os.makedirs(export_dir, exist_ok=True)
        
    def start(self):
        """Start the NFS server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        logging.info(f"NFS Server started on {self.host}:{self.port}")
        logging.info(f"Exporting directory: {self.export_dir}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, address)
            )
            client_thread.start()
            
    def handle_client(self, client_socket, address):
        """Handle client connections"""
        client_id = f"{address[0]}:{address[1]}"
        self.clients[client_id] = client_socket
        
        logging.info(f"New client connected: {client_id}")
        
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                    
                request = json.loads(data.decode())
                response = self.process_request(request, client_id)
                client_socket.send(json.dumps(response).encode())
                
        except Exception as e:
            logging.error(f"Error handling client {client_id}: {str(e)}")
        finally:
            client_socket.close()
            del self.clients[client_id]
            logging.info(f"Client disconnected: {client_id}")
            
    def process_request(self, request, client_id):
        """Process client requests"""
        command = request.get('command')
        args = request.get('args', [])
        
        try:
            if command == 'ls':
                return self.handle_ls(args[0], client_id)
            elif command == 'copy':
                return self.handle_copy(args[0], args[1], client_id)
            elif command == 'delete':
                return self.handle_delete(args[0], client_id)
            else:
                return {'status': 'error', 'message': 'Invalid command'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def handle_ls(self, path, client_id):
        """Handle ls command"""
        with self.lock:
            try:
                if path.startswith('remoto:'):
                    path = os.path.join(self.export_dir, path[7:])
                else:
                    path = os.path.abspath(path)
                    
                if not os.path.exists(path):
                    return {'status': 'error', 'message': 'Path does not exist'}
                    
                files = []
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    files.append({
                        'name': item,
                        'is_dir': os.path.isdir(full_path),
                        'size': os.path.getsize(full_path) if os.path.isfile(full_path) else 0
                    })
                    
                logging.info(f"CLIENTE_{client_id} realizou operação 'ls' no diretório '{path}'")
                return {'status': 'success', 'files': files}
                
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
                
    def handle_copy(self, src, dst, client_id):
        """Handle copy command"""
        with self.lock:
            try:
                # Handle source path
                if src.startswith('remoto:'):
                    src = os.path.join(self.export_dir, src[7:])
                else:
                    src = os.path.abspath(src)
                    
                # Handle destination path
                if dst.startswith('remoto:'):
                    dst = os.path.join(self.export_dir, dst[7:])
                else:
                    dst = os.path.abspath(dst)
                    
                if not os.path.exists(src):
                    return {'status': 'error', 'message': 'Source file does not exist'}
                    
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                
                shutil.copy2(src, dst)
                logging.info(f"CLIENTE_{client_id} copiou o arquivo '{src}' para '{dst}'")
                return {'status': 'success', 'message': 'File copied successfully'}
                
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
                
    def handle_delete(self, path, client_id):
        """Handle delete command"""
        with self.lock:
            try:
                if path.startswith('remoto:'):
                    path = os.path.join(self.export_dir, path[7:])
                else:
                    path = os.path.abspath(path)
                    
                if not os.path.exists(path):
                    return {'status': 'error', 'message': 'File does not exist'}
                    
                os.remove(path)
                logging.info(f"CLIENTE_{client_id} deletou o arquivo '{path}'")
                return {'status': 'success', 'message': 'File deleted successfully'}
                
            except Exception as e:
                return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    server = NFSServer()
    server.start() 
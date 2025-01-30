
import socket
import json

def handle_client(connection_socket: socket.socket) -> None:
    """
    Handle a client connection.
    
    args:
        connection_socket (socket.socket): The socket to the client.
    """
    # Receive the data from the client
    _data = json.loads(connection_socket.recv(1024).decode())
    print(f"Received data from client: {_data}")
    connection_socket.close()
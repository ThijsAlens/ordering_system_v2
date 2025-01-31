

import logging
import socket
import config
import threading
import os
import re

import back_end.handle_client


def _serve_html(filename: str) -> str:
    """
    Serve the requested HTML file.
    """
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            content = file.read()
        return f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{content}"
    else:
        return "HTTP/1.1 404 Not Found\n\n<h1>404 Not Found</h1>"
    

def _serve_static(filename: str) -> str:
    """
    Serve static files like CSS or JS.
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return f"HTTP/1.1 200 OK\nContent-Type: text/css\n\n{content}"
    except FileNotFoundError:
        return "HTTP/1.1 404 Not Found\n\n<h1>404 Not Found</h1>"
    
def _handle_request(connection: socket.socket) -> None:
    """
    Handle the incoming request.
    """
    request = connection.recv(1024).decode('utf-8')
    logging.info(f"Request received: {request}")

    method_match = re.match(r"(GET|POST) /(.*) HTTP/1.1", request)
    
    if method_match:
        method = method_match.group(1)  # GET or POST
        path = method_match.group(2)  # Path (e.g., 'client', 'master', 'static/styles.css', etc.)
        print(f"Method: {method}, Path: {path}")
    else:
        method = None
        path = None

    match method, path:
        case "GET", "client":
            # Serve the client.html file
            response = _serve_html("front_end/templates/client.html")
        case "GET", "master":
            # Serve the master.html file
            response = _serve_html("front_end/templates/master.html")
        case "GET", "static/styles.css":
            # Serve the styles.css file
            response = _serve_static("front_end/static/styles.css")
        case "POST", "client/send":
            # Handle the client's order
            back_end.handle_client.handle_client(request=request)
            response = _serve_html("front_end/templates/client.html")
        case _, _:
            # Serve the error.html file
            response = _serve_html("front_end/templates/error.html")
    
    connection.sendall(response.encode())
    connection.close()

def _setup_server() -> socket.socket:
    """
    Set up the server socket.
    """
    try:
        config.SERVER_PORT = _find_open_port()
        logging.info(f"Found open port: {config.SERVER_PORT}")
    except RuntimeError as e:
        logging.error(str(e))
        return
    # set up a server socket
    _server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _server_socket.bind((config.SERVER_HOST, config.SERVER_PORT))
    _server_socket.listen(config.SERVER_NUMBER_OF_CONNECTIONS)
    logging.info(f"Server started at {config.SERVER_HOST}:{config.SERVER_PORT}")
    print(f"Server started at {config.SERVER_HOST}:{config.SERVER_PORT}")
    return _server_socket

def _find_open_port(start_port=config.SERVER_PORT_RANGE[0], end_port=config.SERVER_PORT_RANGE[1]) -> int:
    """
    Find an open port on the local machine from where the server can run.
    
    args:
        start_port (int): The port number to start the search from. Default is 3000.
        end_port (int): The port number to end the search at. Default is 5000.
    
    returns:
        int: The port number that is open and therefore will be used for the server.
    """

    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    raise RuntimeError("No available ports found in the specified range.")

def run_server() -> None:
    _socket = _setup_server()
    while (config.GLOBAL_RUNNING):
        try:
            # Accept a connection and give it its own thread to handle it
            _connection_socket, _address = _socket.accept()
            logging.info(f"Accepted a connection from {_address}, handeling it...")
            config.GLOBAL_THREADS["CLIENT_THREADS"].append(threading.Thread(target=_handle_request, args=(_connection_socket,)))
            config.GLOBAL_THREADS["CLIENT_THREADS"][-1].start()
        except Exception as e:
            logging.error(f"Could not accept a connection from the server socket: {e}")
    
    _socket.close()
    return
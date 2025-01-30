

import logging
import socket
import config
import threading

import back_end.client

def _setup_server() -> socket.socket:
    """
    main code for the server
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
            config.GLOBAL_THREADS.append(threading.Thread(target=back_end.client.handle_client, args=(_connection_socket,)))
            config.GLOBAL_THREADS[-1].start()
        except Exception as e:
            logging.error(f"Could not accept a connection from the server socket: {e}")
    
    _socket.close()
    return
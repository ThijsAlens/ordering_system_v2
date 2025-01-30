
import socket
import json

import config
import logging

def send_to_server(data: dict) -> bool:
    """
    Send a request to the server and return the response.

    args:
        data (dict): The data to send to the server.

    returns:
        bool: True if the request was successful, False otherwise.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((config.SERVER_IP, config.SERVER_PORT))
            s.sendall(json.dumps(data).encode())
            return True
    except Exception as e:
        logging.error(f"Could not send data to the server: {e}")

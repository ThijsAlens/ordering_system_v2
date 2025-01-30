
import logging
import threading

import back_end.server
import front_end.web_app
import config

def setup_logger():
    logging.basicConfig(
        filename=config.FILE_PATH_LOGGER,
        encoding="utf-8",
        filemode="a",  # Append to the log file
        format="{asctime} - {levelname}\t {filename}\t| {message}",
        style="{",
        datefmt="%d-%m-%Y %H:%M",
        level=logging.INFO  # Set default logging level
    )


if __name__ == "__main__":
    setup_logger()
    logging.info(f"Initializing the system")

    # Start the server
    config.GLOBAL_THREADS.append(threading.Thread(target=back_end.server.run_server))
    config.GLOBAL_THREADS[-1].start()

    # Start the web-app application
    config.GLOBAL_THREADS.append(threading.Thread(target=front_end.web_app.run_web_app))
    config.GLOBAL_THREADS[-1].start()
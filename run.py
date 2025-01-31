
import logging
import threading
import csv

import back_end.server
import back_end.model.item
import front_end.create_html
import config

def setup_logger() -> None:
    logging.basicConfig(
        filename=config.FILE_PATH_LOGGER,
        encoding="utf-8",
        filemode="a",  # Append to the log file
        format="{asctime} - {levelname}\t {filename}\t| {message}",
        style="{",
        datefmt="%d-%m-%Y %H:%M",
        level=logging.INFO  # Set default logging level
    )

def reset_logger() -> None:
    with open(config.FILE_PATH_LOGGER, "w") as file:
        file.write("")

def read_menu() -> list[back_end.model.item.Item]:
    menu: list[back_end.model.item.Item] = []
    with open("menu.csv", "r", newline="") as file:
        reader = csv.reader(file)
        # Skip the header
        next(reader)
        id: int = 0
        for row in reader:
            menu.append(back_end.model.item.Item(id=id, name=row[0], destination=row[2], price=float(row[1])))
            id += 1
    return menu


if __name__ == "__main__":
    setup_logger()
    reset_logger()
    logging.info(f"Initializing the system")

    # Read the menu from the menu.csv file
    config.GLOBAL_MENU = read_menu()

    # Create the html files
    front_end.create_html.create_html()

    # Set up the state files
    with open(config.FILE_NAME_ORDERS, "w") as file:
        file.write("[]")

    # Start the server
    config.GLOBAL_THREADS["MAIN_THREADS"].append(threading.Thread(target=back_end.server.run_server))
    config.GLOBAL_THREADS["MAIN_THREADS"][-1].start()

import json
import config
import logging
import time

import back_end.model.order

def _formalize_request(request:str) -> dict:
    """
    Formalize the incoming request.
    """
    body_start = request.find("\r\n\r\n") + 4  # Find where the body starts
    body = request[body_start:]  # Extract body

    print(f"POST request body: {body}")
    parsed_data = {}
    # Split the data by '&' to get key-value pairs
    pairs = body.split("&")
    for pair in pairs:
        key, value = pair.split("=")
        parsed_data[key] = value
    
    processed_data: dict = \
        {"id":-1,
         "items":[]}
    for key, value in parsed_data.items():
        if key == "client_id":
            processed_data["id"] = int(value)
        else:
            if value == "0":
                continue
            for item in config.GLOBAL_MENU:
                if item.id == int(key):
                    processed_data["items"].append((value, item.serialize()))
                    break
    return processed_data

def _update_order(new_order: back_end.model.order.Order) -> None:
    attempt:int = 0
    while attempt < config.SEMAPHORE_TIMEOUT:
        aquired = config.SEMAPHORE_ORDER_FILE.acquire(blocking=False)
        if not aquired:
            attempt += 1
            time.sleep(config.SEMAPHORE_RETRY_INTERVAL)
            continue
        try:
            with open(config.FILE_NAME_ORDERS, "r+") as file:
                # Load the existing data
                file.seek(0)
                existing_data: list[dict] = json.load(file)
                
                # Check if the order already exists, replace it if it does or append the new one if it doesn't
                for order_dict in existing_data:
                    order: back_end.model.order.Order = back_end.model.order.Order.deserialize(order_dict)
                    if order.id == new_order.id:
                        existing_data.remove(order_dict)
                        break
                existing_data.append(new_order.serialize())

                # Write the updated data to the file
                file.seek(0)
                file.write(json.dumps(existing_data))
        except Exception as e:
            logging.error(f"Error updating order with order_ID {new_order.id}: {e}")
        finally:
            config.SEMAPHORE_ORDER_FILE.release()

        logging.info(f"Updated order with order_ID {new_order.id}")
        return
    logging.error(f"Failed to update order with order_ID {new_order.id} (timeout of the semaphore)")
        

def handle_client(request:str) -> None:
    """
    Handle the incoming request.
    """
    # Formalize the incoming request
    formalized_request: dict = _formalize_request(request)
    print(f"\nReceived order: {formalized_request}\n")
    
    new_order: back_end.model.order.Order = back_end.model.order.Order.deserialize(formalized_request)
    print(f"order.id: {new_order.id}\norder.items: {new_order.items}\n")
    _update_order(new_order)


    
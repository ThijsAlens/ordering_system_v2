
import config

def _write_html_file(path:str, data:str) -> None:
    with open(path, "w") as file:
        file.write(data)

def _create_client_html() -> str:
    html = \
    """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
    <form action="/client/send" method="post">
        <label for="client_id">Selecteer je ID:</label>
        <select id="client_id" name="client_id">
    """
    for i in range(1, config.NUMBER_OF_CLIENTS + 1):
        html += f"<option value={i}>{i}</option>"
    html += \
    """
        </select>

        <label for="oder_id">Selecteer je het ordernummer:</label>
        <select id="oder_id" name="oder_id">
    """
    for id in config.GLOBAL_ACTIVE_ORDERS:
        html += f"<option value={id}>{id}</option>"
    html += \
    """
        </select>
        
        <table>
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Aantal</th>
                </tr>
    """
    for item in config.GLOBAL_MENU:
        html += \
        f"""
            <tr>
                <td>{item.name}</td>
                <td><input type="number" name="{item.id}" value="0" min="0" max="9999"></td>
            </tr>
        """
    html += \
    """
        </table>
        <input type="submit" value="Bevestig bestelling">
    </form>
    </body>
    </html>
    """
    return html

def create_html() -> None:
    _write_html_file("front_end/templates/client.html", _create_client_html())
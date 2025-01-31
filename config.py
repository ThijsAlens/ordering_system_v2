###############################################################################
#-- This is the configuration file for, set up the variables to your system --#
###############################################################################

###############################################################################
#--------------------------- SERVER CONFIGURATION ----------------------------#
###############################################################################

# The server IP address (the IP-adress of the pc that run.py is executed on)
SERVER_IP = "192.168.0.143"

# Only change these values if you know what you are doing
SERVER_HOST = '0.0.0.0'             # The host to use for the server
SERVER_PORT_RANGE = (3000, 5000)    # The range of ports to search for an open port
SERVER_PORT = 3000                  # The port to use for the server
SERVER_NUMBER_OF_CONNECTIONS = 20   # The number of connections the server can handle

###############################################################################
#--------------------------- WEB-APP CONFIGURATION ---------------------------#
###############################################################################
WEB_APP_PORT = 7000                 # The port to use for the web-app

###############################################################################
#--------------------------- LOGGER CONFIGURATION ----------------------------#
###############################################################################
# The path to the log file
FILE_PATH_LOGGER = "log.log"

###############################################################################
#---------------------------- THREAD MANAGEMENT ------------------------------#
###############################################################################
import threading
GLOBAL_THREADS: dict[str, list[threading.Thread]] = \
    {"MAIN_THREADS": [],
     "CLIENT_THREADS": [],
     "MODEL_MODIFICATION_THREADS": []} 

###############################################################################
#--------------------------- MAIN LOOP MANAGEMENT ----------------------------#
###############################################################################
GLOBAL_RUNNING: bool = True           # The main loop of the server

###############################################################################
#-------------------------- OTHER GLOBAL VARIABLES ---------------------------#
###############################################################################
import back_end.model.item
GLOBAL_MENU: list[back_end.model.item.Item] = []  # The menu of the restaurant

###############################################################################
#-------------------------- CLIENT CONFIGURATION -----------------------------#
###############################################################################
NUMBER_OF_CLIENTS = 6                # The number of clients that can connect to the server
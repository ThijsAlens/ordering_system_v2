###############################################################################
#-- This is the configuration file for, set up the variables to your system --#
###############################################################################

###############################################################################
#--------------------------- SERVER CONFIGURATION ----------------------------#
###############################################################################

# The server IP address (the IP-adress of the pc that run.py is executed on)
SERVER_IP = "192.168.4.118"

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
# List of all threads
GLOBAL_THREADS = []

###############################################################################
#--------------------------- MAIN LOOP MANAGEMENT ----------------------------#
###############################################################################
GLOBAL_RUNNING = True           # The main loop of the server
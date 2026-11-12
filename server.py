#Server Design:
#*
#   Get a status code from client(s) -- saying what theyre about to send
#   Point server to case of which variable to update
#   Update variable, send data back -- either echo or appropiate response 
# *#

import json
from dataclasses import asdict, dataclass
import time as t
import threading
from socket import *

BUFFER_SIZE = 2048

@dataclass 
class Ride:
    """dataclass for Ride"""
    rideID:int
    customer:str
    driver:str
    pick_zone:str
    dropoff_zone:str
    distance:int
    cost:float
    req_time:t
    dropoff_time:t
    status:int

##still missing a way to store users??

def handle_request(user, pickup_zone, dropoff_zone) -> str:
    myStr = f"[HANDLER_REQ] Received: {user=}, {pickup_zone=}, {dropoff_zone=}"
    return myStr

## HANDLE CLIENT RESPONSES
def handle_client(data, client_address, server_socket):
    handlers = {
        "request": handle_request
    }
    """worker function to handle incoming data"""
    try:
        thread_name = threading.current_thread().name
        message = data.decode()
        print(f'[{thread_name}] Received: [{message}] From: [{client_address}]')
        
        ## Read action, call next function
        jsonData = json.loads(message)
        clientAction = jsonData["action"]
        ##clean json before passing it:
        payload = {key: value for key, value in jsonData.items() if key != "action"}
        handler = handlers.get(
            clientAction, 
            lambda **kwargs: "Invalid"
            )(**payload) #lambda is also rlly cool, gets rid of the need for a conditional check
        ## so the **jsonData is rlly cool here, it unpacks the keys from the dict in the parsed JSON and correlates them by NAME!! to the function args


        ## reply back
        response = handler
        server_socket.sendto(response.encode(), client_address)
        print(f'[{thread_name}] Sent: [{response}] To [{client_address}]')
    except Exception as e:
        print(f"Error handling data from {client_address}: {e}")

##START SERVER
def start_server():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))

    print(f'[SERVER STARTED] Listening on localhost:{serverPort}')

    try:
        while True: #will change conditional -- maybe while driver/client == None
            #block execution until data arrives
            data, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)

            #start worker thread to handle data
            client_thread = threading.Thread(
                target=handle_client,
                daemon=True, #daemon to exit when prog stops
                args=(data, clientAddress, serverSocket)
            )
            client_thread.start()
    except KeyboardInterrupt:
        print('\n[SERVER] Closing socket...')
    finally:
        serverSocket.close()

start_server()
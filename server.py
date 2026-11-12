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


## HANDLE CLIENT RESPONSES
def handle_client(data, client_address, server_socket):
    """worker function to handle incoming data"""
    try:
        thread_name = threading.current_thread().name
        message = data.decode()
        print(f'[{thread_name}] Received: [{message}] From: [{client_address}]')
        ## Read action, call next function
        
        response = f'{message}'
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
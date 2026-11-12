#Server Design:
#*
#   Get a status code from client(s) -- saying what theyre about to send
#   Point server to case of which variable to update
#   Update variable, send data back -- either echo or appropiate response 
# *#

import json
from dataclasses import field, dataclass
import datetime
import threading
from socket import *
from queue import Queue

BUFFER_SIZE = 2048

shutdown_event = threading.Event() ##init shutdown event flag
STOP = object() ## create stop obj for sessions to recognize

@dataclass
class ClientSession:
    address: tuple[str, int] # client's address + port
    messages: Queue = field(default_factory=Queue) # Accepts a zero-argument callable (like list or dict) to generate a fresh default value for each new instance.
    worker: threading.Thread | None = None
    user: str | None = None
    authenticaed: bool = False


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
    req_time:datetime.time
    dropoff_time:datetime.time
    status:int

#SESSION STORE: (so we dont keep making threads)
sessionsList: dict[tuple[str, int], ClientSession] = {}

def handle_login(user):
    return f"[HANDLER_LOGIN] {user} successfully logged in!"

def handle_request(user, pickup_zone, dropoff_zone) -> str:
    myStr = f"[HANDLER_REQ] Received: {user=}, {pickup_zone=}, {dropoff_zone=}"
    return myStr


## HANDLE CLIENT RESPONSES
def handle_client(data, client_address, server_socket, session):
    ##TODO: update session login/user/auth status
    handlers = {
        "request": handle_request,
        "login": handle_login
    }
    """worker function to handle incoming data"""
    try:
        thread_name = threading.current_thread().name
        message = data

        print(f'[{thread_name}] Received: [{message}] From: [{client_address}]')
        
        ## Read action, call next function
        jsonData = json.loads(message.decode())
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

'''END HANDLING, BEGIN SERVER IMPLEMENTATION'''

def client_worker(session, server_socket):
    while True:
        data = session.messages.get()

        try:
            if data is STOP:
                return
            handle_client(data, session.address, server_socket, session)
        finally:
            session.messages.task_done()

#takes address (tuple of IP:PORT), finds session based on address, if not found creates new session
def get_or_create_session(address, server_socket):
    if address not in sessionsList:
        #creates new clientSession
        session = ClientSession(address=address)
    
        #starts new thread
        session.worker = threading.Thread(
            target = client_worker,
            args=(session, server_socket)
        )
        sessionsList[address] = session #binds session to item in sessionList 
        session.worker.start() #starts worker in session

    return sessionsList[address]



##START SERVER
def start_server():
    
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))

    print(f'[SERVER STARTED] Listening on localhost:{serverPort}')
    

    try:
        while True: 
            #block execution until data arrives
            data, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
            session = get_or_create_session(clientAddress, serverSocket)
            session.messages.put(data) #put raw byte data into ClientSession: messages Queue
            #start worker thread to handle data
    except KeyboardInterrupt:
        print('\n[SERVER] Closing socket...')
    finally:
        """BEGIN SHUTDOWN"""
        shutdown_event.set()

        for session in sessionsList.values():
            session.messages.put(STOP)

        for session in sessionsList.values():
            if session.worker is not None:
                session.worker.join() #join back with main thread

        serverSocket.close()

start_server()
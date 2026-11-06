#PROGRAM FLOW AS OF NOW:
#*
#               
# *#

import time as t
from socket import *

#user details, maybe implement as class?
users = ["A", "B", "C"]    
#driver details
drivers = ["D","E","F"]

#req id is starting 1, increment after every ride req
reqID = 0
def generateReqID():
    reqID += 1
    return reqID


#vars: request time, pickup time, dropoff time
def getTime():
    currTime = t.localtime()
    time_struct = currTime.tm_hour, currTime.tm_min, currTime.tm_sec
    return time_struct #should return (hh, mm, ss)

#status 1-requested, no driver yet
#       2-accepted by driver, driver otw
#       3-picked up, otw to dropoff
#       4-dropped off customer

##START SERVER
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('Server listening...')

def getClientResponse[T](response:T) -> T:
    clientResponse, clientAddress = serverSocket.recvfrom(2048)
    response = clientResponse.decode()
    return response


#get customer
print('Server waiting for selectedUser input...')
selectedUser = None
while (selectedUser == None):
    clientSelUser, clientAddress = serverSocket.recvfrom(2048)
    selectedUser = clientSelUser.decode()
print(f"{selectedUser=}")
#TODO: AUTHENTICATE LOGIC
#maybe have client wait until driver is selected?
#do busy wait while driver == unselected


#get driver -- how to make this async?? or rather make it so we dont HAVE to get user first before driver
print('Server waiting for selectedDriver input...')
selectedDriver = None
while (selectedDriver == None):
    clientSelDriver, clientAddress = serverSocket.recvfrom(2048)
    selectedDriver = clientSelDriver.decode()
print(f'{selectedDriver=}')
#TODO: AUTHENTI LOGIC

#get pickup
print('Server waiting for pickupZone input...')
pickupZone = None
while (pickupZone == None):
    clientPickUpZone, clientAddress = serverSocket.recvfrom(2048)
    pickupZone = clientPickUpZone.decode()
print(f'{pickupZone=}')
#TODO: assign distances

#get dropoff
print('Server waiting for pickupZone input...')
dropZone = None
while (dropZone == None):
    clientDropZone, clientAddress = serverSocket.recvfrom(2048)
    dropZoneZone = clientDropZone.decode()
print(f'{dropZone=}')

##ASSUMING NOW CLIENT(CUSTOMER) IS WAITING FOR COST AND DISTANCE
#calc dist

#calc cost

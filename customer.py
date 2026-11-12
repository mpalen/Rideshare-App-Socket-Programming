import json
from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
#client
# list of 3 customers 'a' 'b' 'c'
# username and pw for each are the same --should be stored in serv


# get input from user for username/password
user = input("Enter user(A/B/C): ")
action = input("Enter action (request): ")
pickup_zone = input("Enter pickup zone: ")
dropoff_zone = input("Enter drop off zone: ")

request = {
    "user": user,
    "action": action,
    "pickup_zone": pickup_zone,
    "dropoff_zone": dropoff_zone
}

message = json.dumps(request).encode()
clientSocket.sendto(message, (serverName, serverPort))
data = clientSocket.recvfrom(2048)[0].decode()

print(f"{data}")
# authenticate/authorize

# prompt for profile pic
# get profile pic, send

# prompt for ride history
# show ride history

#prompt if want to ride

#prompt for pickup loc
#save answer as current customer loc
#send status 0-not reading yet
#prompt for dropoff

#server handles data store, calc dis+cost

#prompt user to accept ride
#back to server, inputs ride into ride history
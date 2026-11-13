import json
from math import dist
from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
_SERVER = (serverName, serverPort)

# Setting up the zone map... using weighted graphs ;c (DSA was 4evur ago)
nodes = {
    1: (0,0),
    2: (1,0),
    3: (2,0),
    4: (0,1), #technically graph on project PDF shows 4 down but who cares
    5: (1,1),
    6: (2,1),
    7: (2,0),
    8: (2,1),
    9: (2,2)
}

def calculate_weight(node1, node2):
    return round(dist(nodes[node1], nodes[node2]), 1) ##euclidean distance form

graph = {node: {} for node in nodes}

for node1 in nodes:
    for node2 in nodes:
        if node1 != node2:
            weight = calculate_weight(node1, node2)
            graph[node1][node2] = weight

## ZONE MAP DONE

#client
# list of 3 customers 'a' 'b' 'c'
# username and pw for each are the same --should be stored in serv
user = input("Enter user(A/B/C): ")

requestLogin = {
    "user": user,
    "action": "login"
}

message = json.dumps(requestLogin).encode()
clientSocket.sendto(message, _SERVER)
data = clientSocket.recvfrom(2048)[0].decode()
print(f"{data}")

# get input from user for username/password
action = input("Enter action (request): ")
while True:
    try:
        pickup_zone = int(input("Enter pickup zone (1-9): "))
        dropoff_zone = int(input("Enter drop off zone (1-9): "))

        if pickup_zone not in nodes or dropoff_zone not in nodes:
            print("Zones must be between 1 and 9.")
            continue

        if pickup_zone == dropoff_zone:
            print("Pickup and drop-off zones must be different.")
            continue

        break
    except ValueError:
        print("Please enter whole-number zones.")

distance = graph[pickup_zone][dropoff_zone]
cost = round(distance * 5, 2)

requestRide = {
    "action": action,
    "pickup_zone": pickup_zone,
    "dropoff_zone": dropoff_zone,
    "distance": distance,
    "cost": cost
}

message = json.dumps(requestRide).encode()
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

clientSocket.close()
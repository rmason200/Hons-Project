# for the Adafruit IO API
from Adafruit_IO import Client

aio = Client("<USERNAME>", "<API-KEY>")

# sets test result 
sts_B = "init"

# takes input for test
sts_B = input("Enter Signal B Status: ")

# sends the variable 'sts_B' to the API feed 'status-b'
aio.send('status-b', sts_B)

# retrieves updated parameter from API
sts_B = aio.receive('status-b').value

# prints result
print("Signal B Status: " + str(sts_B))

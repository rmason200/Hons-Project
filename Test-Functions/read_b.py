# for the Adafruit IO API
from Adafruit_IO import Client

aio = Client("<USERNAME>", "<API-KEY>")

# receives status of signal from API, prints to terminal
UnitB_status = aio.receive('status-b').value
print("Unit B Signal State: " + str(UnitB_status))

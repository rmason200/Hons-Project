# for the Adafruit IO API
from Adafruit_IO import Client

aio = Client("rmason200", "d5b8d9b68d654dfb965acfb8dc1e7ffd")

# receives status of signal from API, prints to terminal
UnitB_status = aio.receive('status-b').value
print("Unit B Signal State: " + str(UnitB_status))

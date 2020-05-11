# for the Adafruit IO API
from Adafruit_IO import Client

aio = Client("<USERNAME>", "<API-KEY>")

# sets test values
eCO2_data = # enter test value here
tvoc_data = # enter test value here
redu_data = # enter test value here
oxi_data = # enter test value here

# prints values to terminal
print("eCO2:\t" + str(eCO2_data))
print("TVOC:\t" + str(tvoc_data))
print("CO:\t" + str(redu_data))
print("NO2:\t" + str(oxi_data))

# sends values to API
aio.send('eco2-b', eCO2_data)
aio.send('tvoc-b', tvoc_data)
aio.send('redu-b', redu_data)
aio.send('oxi-b', oxi_data)

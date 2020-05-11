# for the Adafruit IO API
from Adafruit_IO import Client
# for the SGP30 functions, including I2C 
import board
import busio
# imports the SGP30-specific library
import adafruit_sgp30
# importing gas module of enviroplus library
from enviroplus import gas

# neccessary definitions for sensors and API
# defines the username and key for the API
aio = Client("rmason200", "d5b8d9b68d654dfb965acfb8dc1e7ffd")
# enables the I2C for the SGP30, defining pin inputs etc
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
#initialises the SGP30 sensor, defines properties according to adafruit documentation
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)



# begins by assigning the information for A and B to variables

print("Reading data from sensors...")
# for A, read data from sensors
# for SGP30 a simple read
eco2_A = sgp30.eCO2
tvoc_A = (sgp30.TVOC) + 1
# enviroplus, gas readings taken to intermediary variable
enviro_readings = gas.read_all()
# specific reading taken from intermediary variable and assigned to specific variable
redu_A = enviro_readings.reducing
oxi_A = enviro_readings.oxidising

print("Reading data from API...")
# for B, information taken from API
eco2_B = float(aio.receive('eco2-b').value)
tvoc_B = (float(aio.receive('tvoc-b').value)) + 1
redu_B = float(aio.receive('redu-b').value)
oxi_B = float(aio.receive('oxi-b').value)

print("eCO2 at A: " + str(eco2_A))
print("TVOC at A: " + str(tvoc_A))
print("CO at A: " + str(redu_A))
print("NO2 at A: " + str(oxi_A))
print("eCO2 at B: " + str(eco2_B))
print("TVOC at B: " + str(tvoc_B))
print("CO at B: " + str(redu_B))
print("NO2 at B: " + str(oxi_B))

# code to run the loop for unit B
# at each second, Unit B checks the API for the status that for the signal
# every 10 seconds, it sends the sensor data to the API


# import relevant libraries

# system libraries
import time
import threading

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


# loop counter
count = 0


def data_send():
	# reads data from sensors, assigns value to relevant variable
	# for SGP30 a simple read
	eCO2_data = sgp30.eCO2
	tvoc_data = sgp30.TVOC
	# for enviroplus, gas readings taken to intermediary variable
	enviro_readings = gas.read_all()
	# specific reading taken from intermediary variable and assigned to specific variable        
	redu_data = enviro_readings.reducing
	oxi_data =  enviro_readings.oxidising

	# prints values to terminal
	print("eCO2:\t" + str(eCO2_data))
	print("TVOC:\t" + str(tvoc_data))
	print("CO:\t" + str(redu_data))
	print("NO2:\t" + str(oxi_data))

	# sends values to API
	aio.send('eco2-av', eCO2_data)
	aio.send('tvoc-av', tvoc_data)
	aio.send('redu-av', redu_data)
	aio.send('oxi-av', oxi_data)


while True:
	# sets up time variable needed to ensure loop happens once a second
	# rather than <code runtime> + 1 second
	starttime = time.time()
	
	# prints counter to display progress of loop
	print("\nCount: " + str(count))
	print("Time: " + str(time.time()))
	
	# receives status of signal from API, prints to terminal
	UnitB_status = aio.receive('unit-b-status').value
	print("Unit B Signal State: " + str(UnitB_status))
	
	if count == 10:		
		# creates a thread to allow the data send process to run in parallel
		data_send_thread = threading.Thread(target = data_send)
		# starts the thread
		data_send_thread.start()
		
		# resets count to start loop again
		count = 0
     
	# increments loop
	count = count + 1
	# sleeps process for the rest of the second
	# takes process time and removes it from the second, then sleeps for remaining time
	time.sleep(1.0 - ((time.time() - starttime) % 60))

# code to gather sensor data over a 12-hour period
# every 10 seconds, the sensor data will be read
# after a 10-minute warm-up period, sensor data will begin writing to files
# this writing period will continue every 10 seconds for the remainder of the 12-hour period
# once writing period is complete, pi is shut down


# import libraries for system functions
import time
import sys
from subprocess import call

# importing gas module of enviroplus library
from enviroplus import gas

# imports libraries nor SGP30 functions, including I2C
import board
import busio

#imports the SGP30-specific library
import adafruit_sgp30

#series of definitions used throughout code
#defines loop delay as 10 seconds
LOOP_DELAY = 10

# enables the I2C for the SGP30, defining pin inputs etc
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

#initialises the SGP30 sensor, defines properties according to adafruit documentation
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)

# initialises the loop counter
count = 0



# main loop function, all processes contained herein
while True:
    # first period of count defines warm up period
    while count < 60: # 60 * 10 seconds = 10 minutes
        # increments counter
        count = count + 1
        # if running through terminal, prints progress for easier supervision
        print("Warming up... Progress: " + str(count) + "/60")
        print('Reading sensors...\n')
        
        # reads data from sensors, assigns value to relevant variable
        # for SGP30 a simple read
        eCO2_data = sgp30.eCO2
        tvoc_data = sgp30.TVOC
        # enviroplus, gas readings taken to intermediary variable
        enviro_readings = gas.read_all()
        # specific reading taken from intermediary variable and assigned to specific variable        
        nh3_data = enviro_readings.nh3
        redu_data = enviro_readings.reducing
        oxi_data =  enviro_readings.oxidising

        # prints read data to terminal
        print('--- Enviro+ Data ---')
        print("NH3: ", str(nh3_data),)
        print("Oxidising: ", str(oxi_data))
        print("Reducing: ", str(redu_data), '\n')
        
        print('--- SGP30 Data ---')
        print('eCO2:', eCO2_data)
        print('tvoc:', tvoc_data,'\n')
        
        print("----------------------\n")
        
        # sleeps board for the defined delay (10s)
        time.sleep(LOOP_DELAY)


    # next while loop covers writing phase
    while count > 59 and count < 4320: # 4320 * 10s = 12 hours
        #increments the counter
        count = count + 1
        # if running through terminal, prints progress for supervison
        # -60 accounts for warm up period
        print("Collecting data... Progress: " + str(count-60) + "/4260")
        print("Reading sensors...\n")
     
        # reads data from sensors, assigns value to relevant variable
        # for SGP30 a simple read
        eCO2_data = sgp30.eCO2
        tvoc_data = sgp30.TVOC
        # enviroplus, gas readings taken to intermediary variable
        enviro_readings = gas.read_all()
        # specific reading taken from intermediary variable and assigned to specific variable        
        nh3_data = enviro_readings.nh3
        redu_data = enviro_readings.reducing
        oxi_data =  enviro_readings.oxidising

        # print read data to terminal
        print('--- Enviro+ Data ---')
        print("NH3: ", str(nh3_data),)
        print("Reducing: ", str(redu_data))
        print("Oxidising: ", str(oxi_data), '\n')
        
        print('--- SGP30 Data ---')
        print('eCO2:', eCO2_data)
        print('TVOC:', tvoc_data,'\n')

        #prints to terminal current status
        print("Writing data to files...\n")


        # series of file handling sequences to write data for each type
        # first line opens file, defines file path and destination file, which is then created/appended to
        # second line writes the data as a string to the file
        # third line closes file, ends file handling operation
        
        # nh3 value file handling
        nh3_file = open("/home/pi/Project/Test-Data/data_nh3.txt", "a")
        nh3_file.write(str(nh3_data) + "\n")
        nh3_file.close()

        # reducing value file handling
        redu_file = open("/home/pi/Project/Test-Data/data_reducing.txt", "a")
        redu_file.write(str(redu_data) + "\n")
        redu_file.close()
        
        # oxidising value file handling
        oxi_file = open("/home/pi/Project/Test-Data/data_oxidising.txt", "a")
        oxi_file.write(str(oxi_data) + "\n")
        oxi_file.close()

        # eCO2 value file handling
        eCO2_file = open("/home/pi/Project/Test-Data/data_eCO2.txt", "a")
        eCO2_file.write(str(eCO2_data) + "\n")
        eCO2_file.close()

        # TVOC value file handling
        tvoc_file = open("/home/pi/Project/Test-Data/data_tvoc.txt", "a")
        tvoc_file.write(str(tvoc_data) + "\n")
        tvoc_file.close()
        
        print("-------------------------------\n")
        
        # sleeps code for defined delay (10s)
        time.sleep(LOOP_DELAY)


    # final while loop, responsible for shutting down pi and ending the code
    # occurs at end ofthe 12-hour period
    while count > 4319:
        # updates user on progress
        print("Data gathering complete.\n")
        # sends command to command line shutting down pi in 1 minute
        # this also prints shutdown message to terminal
        call("sudo shutdown --poweroff", shell = True)
        # exits program
        sys.exit()

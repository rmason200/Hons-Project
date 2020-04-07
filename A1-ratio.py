# code to ratio the different sensor values from Units A and B


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



# gathering cycle parameters, then making sure they are integers
cyc_time = 90 # input("Enter CYCLE TIME in seconds: ")
cyc_time = int(cyc_time)
intergreen = 10 # input("Enter INTERGREEN TIME in seconds: ")
intergreen = int(intergreen)
ped = 0 # input("Enter PEDESTRIAN TIME in seconds: ")
ped = int(ped)
phase_count = 2     # would be an input in dynamic system
phase_count = int(phase_count)  # unnecessary here, but would be needed if taking input

# calculate total available green split
green_split = cyc_time - (intergreen * phase_count) - ped

# present current info to user
print("\n\tCYCLE TIME\tINTERGREEN\tPEDESTRIAN\tGREEN SPLIT\n\t" + str(cyc_time) + "\t\t" + str(intergreen) + "\t\t" + str(ped) + "\t\t" + str(green_split)+ "\n")


# gather ratio values by gettiing sensor values

# unit A values read from sensors on board
# for SGP30 a simple read
eCO2_data_A = sgp30.eCO2
tvoc_data_A = sgp30.TVOC
# for enviroplus, gas readings taken to intermediary variable
enviro_readings = gas.read_all()
# specific reading taken from intermediary variable and assigned to specific variable        
redu_data_A = enviro_readings.reducing
oxi_data_A =  enviro_readings.oxidising

# prints values to terminal
print("eCO2 at A:\t" + str(eCO2_data_A))
print("TVOC at A:\t" + str(tvoc_data_A))
print("CO at A:\t" + str(redu_data_A))
print("NO2 at A:\t" + str(oxi_data_A))

# unit B values read from API, converted to float so it can be manipulated
eCO2_data_B = aio.receive('eco2-b').value
eCO2_data_B = float(eCO2_data_B)
tvoc_data_B = aio.receive('tvoc-b').value
tvoc_data_B = float(tvoc_data_B)
redu_data_B = aio.receive('redu-b').value
redu_data_B = float(redu_data_B)
oxi_data_B = aio.receive('oxi-b').value
oxi_data_B = float(oxi_data_B)

# prints values to terminal
print("\neCO2 at B:\t" + str(eCO2_data_B))
print("TVOC at B:\t" + str(tvoc_data_B))
print("CO at B:\t" + str(redu_data_B))
print("NO2 at B:\t" + str(oxi_data_B))

# before calculating ratio, ensuring a sensor value =! 0, as this causes an error
# TVOC data is potentially 0 at some points
tvoc_data_A = float(tvoc_data_A) + 1
tvoc_data_B = float(tvoc_data_B) + 1

# put readings at each unit into lists
readings_A = [eCO2_data_A, tvoc_data_A, redu_data_A, oxi_data_A]
readings_B = [eCO2_data_B, tvoc_data_B, redu_data_B, oxi_data_B]
# find ratio of each reading by dividing each reading for entire list
ratios = [a/b for a, b in zip(readings_A, readings_B)]
print("Ratios: " + str(ratios))
ratios.sort()
ratios_0toz = [float(n) - min(ratios) for n in ratios]
print("Ratios 0 to Z: " + str(ratios_0toz))
ratios_0to1 = [float(n) / max(ratios_0toz) for n in ratios_0toz]
print("Ratios 0 to 1: " + str(ratios_0to1))
ratios_1to2 = [float(n) + 1 for n in ratios_0to1]
print("Ratios 1 to 2: " + str(ratios_1to2))

# readings_A = [eCO2_data_A, tvoc_data_A, redu_data_A, oxi_data_A]
# readings_A.sort()
# readings_A_range_0toz = [float(a) - min(readings_A) for a in readings_A]
# print(readings_A_range_0toz)
# readings_A_range_0to1 = [float(a) / max(readings_A) for a in readings_A_range_0toz]
# print(readings_A_range_0to1)

# readings_B = [eCO2_data_B, tvoc_data_B, redu_data_B, oxi_data_B]
# readings_B.sort()
# readings_B_range_0toz = [float(b) - min(readings_B) for b in readings_B]
# print(readings_B_range_0toz)
# readings_B_range_0to1 = [float(b) / max(readings_B) for b in readings_B_range_0toz]
# print(readings_B_range_0to1)



# # calulates ratio for each sensor reading
# eCO2_ratio = float(eCO2_data_A) / float(eCO2_data_B)
# tvoc_ratio = float(tvoc_data_A) / float(tvoc_data_B)
# redu_ratio = float(redu_data_A) / float(redu_data_B)
# oxi_ratio = float(oxi_data_A) / float(oxi_data_B)

# # print each ratio
# print("\neCO2 Ratio:\t" + str(eCO2_ratio))
# print("TVOC Ratio:\t" + str(tvoc_ratio))
# print("CO Ratio:\t" + str(redu_ratio))
# print("NO2 Ratio:\t" + str(oxi_ratio))

# # sorting ratios for normalisation
# ratios = [eCO2_ratio, tvoc_ratio, redu_ratio, oxi_ratio]
# ratios.sort()
# print(ratios)

# # !!!!! NORMALISE !!!!!

# norm = [float(i)/max(ratios) for i in ratios]
# print(norm)

# cyc_ratio = (norm[0] + norm[1] + norm[2] + norm[3]) / 4
# print("\nCycle Ratio: " + str(cyc_ratio))

# # # calculate and print cycle ratio
# # cyc_ratio = (eCO2_ratio + tvoc_ratio + redu_ratio + oxi_ratio) / 4

# periodA = (green_split / phase_count) * cyc_ratio
# periodA = int(periodA)
# periodB = green_split - periodA
# periodB = int(periodB)

# print("\n\tPeriod A\tPeriod B\n\t" + str(periodA) + "\t\t" + str(periodB))

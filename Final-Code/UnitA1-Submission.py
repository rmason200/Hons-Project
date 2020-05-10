# code to run the loop for unit A
# on first run, starts up un-adjusted cycle
# every second, it will send the unit B status to the API
# every 10 seconds, it will take sensor data from A and B
# sensor data at A is read from on-board sensor
# sensor data at B is read from API
# at end of cycle, new period times are calculated and the section times are adjusted for next cycle


# import relevant libraries
# system libraries
import time
import threading
from subprocess import call
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
aio = Client("<USERNAME>", "<API KEY>")
# enables the I2C for the SGP30, defining pin inputs etc
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
#initialises the SGP30 sensor, defines properties according to adafruit documentation
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)


def data_send(): # function to send data to API for Unit B
	print("Sending data to API...")	
	# sends the variable 'sts_B' to the API feed 'status-b'
	aio.send('status-b', sts_B)
	

def data_read(): # function to take sensor inputs and store in list
	print("Reading data from sensors...")
	
	# begins by assigning the information for A and B to variables
	
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
	
	# once data retrieved, values added to lists for use at end of function
	eco2_data_A.append(eco2_A)
	tvoc_data_A.append(tvoc_A)
	redu_data_A.append(redu_A)
	oxi_data_A.append(oxi_A)
	eco2_data_B.append(eco2_B)
	tvoc_data_B.append(tvoc_B)
	redu_data_B.append(redu_B)
	oxi_data_B.append(oxi_B)


def cycle_end(): # function to calculate and reassign new period duration values
	
	#declaring variables as global to avoid errors
	global eco2_data_A
	global tvoc_data_A
	global redu_data_A
	global oxi_data_A
	global eco2_data_B
	global tvoc_data_B
	global redu_data_B
	global oxi_data_B
		
	# start by finding average reading of each list
	# list average = sum of list / number of terms in list
	eco2_av_A = sum(eco2_data_A) / len(eco2_data_A)
	tvoc_av_A = sum(tvoc_data_A) / len(tvoc_data_A)
	redu_av_A = sum(redu_data_A) / len(redu_data_A)
	oxi_av_A = sum(oxi_data_A) / len(oxi_data_A)
	eco2_av_B = sum(eco2_data_B) / len(eco2_data_B)
	tvoc_av_B = sum(tvoc_data_B) / len(tvoc_data_B)
	redu_av_B = sum(redu_data_B) / len(redu_data_B)
	oxi_av_B = sum(oxi_data_B) / len(oxi_data_B)

	# put each average into list of averages
	averages_A = [eco2_av_A, tvoc_av_A, redu_av_A, oxi_av_A]
	averages_B = [eco2_av_B, tvoc_av_B, redu_av_B, oxi_av_B]

	# find ratios for each emission type
	# divides each index of the lists
	ratios = [a/b for a, b in zip(averages_A, averages_B)]
	
	# series of if functions to ensure each index of list is never over 2
	if ratios[0] > 2:
		ratios[0] = 2
	if ratios[1] > 2:
		ratios[1] = 2
	if ratios[2] > 2:
		ratios[2] = 2
	if ratios[3] > 2:
		ratios[3] = 2
	
	# find mean value of ratios to find final ratio
	final_ratio = sum(ratios) / 4

	# calculate each period druation using the new ratio
	# for equal phase times, each phase duration would be half the available green split
	# to allow a decent time available for both phases, the entire phase time is not adjustable
	# in this instance, half of the available time will be the minimum available, plus the adjusted ratio
	periodA_dur = (green_split / 4) + ((green_split / 4) * final_ratio)
	# ensures that period A never exceeds value designed
	if periodA_dur > (green_split * 0.75):
		periodA_dur = green_split * 0.75
	periodB_dur = green_split - periodA_dur
	# set each value as an integer to ensure cycle time stays in whole seconds
	periodA_dur = int(periodA_dur)
	periodB_dur = int(periodB_dur)
	
	print("\n\tPERIOD A\tPERIOD B\n\t" + str(periodA_dur) + ("\t\t") + str(periodB_dur))


	# redefine the start/end times of each stage
	# naming convention
	# Xs = section start
	# Xe = section end
	# Sx = Start section
	# Ax = period A section
	# Tx = transition section
	# Bx = period B section
	# Ex = end section
	
	# global assignment of variables so the new values can be accessed by main and other functions
	global Ss
	global Se
	global As
	global Ae
	global Ts
	global Te
	global Bs
	global Be
	global Es
	global Ee
	
	Ss = 0
	Se = 3
	As = Se
	Ae = As + periodA_dur
	Ts = Ae
	Te = Ts + 7 + intergreen
	Bs = Te
	Be = Bs + periodB_dur
	Es = Be
	Ee = Es + 4
	# print values to terminal
	print("\tSs\tSe\tAs\tAe\tTs\tTe\tBs\tBe\tEs\tEe\n\t" + str(Ss) + "\t" + str(Se) + "\t" + str(As) + "\t" + str(Ae) + "\t" + str(Ts) + "\t" + str(Te) + "\t" + str(Bs) + "\t" + str(Be) + "\t" + str(Es) + "\t" + str(Ee) + "\n")

	# clear lists for reuse later
	eco2_data_A = []
	tvoc_data_A = []
	redu_data_A = []
	oxi_data_A = []
	eco2_data_B = []
	tvoc_data_B = []
	redu_data_B = []
	oxi_data_B = []
	averages_A = []
	averages_B = []
	ratios = []
	

def start_sec(): # function to control signal status at each second of the cycle start section
	# print status to terminal
	# prints counter to display progress of loop
	print("\n+ - - - - - - - - +\n")
	print("Time: " + str(count) + " second(s)")
	print ("CYCLE START")
	
	# call global version of variable so the value is changed outside the function
	global sts_A
	global sts_B
	
	# series of if functions to set and print the status of each signal for each second
	# first part of section
	if count == Ss:
		# sets the status of each light to the relevant value, prints to terminal
		sts_A = 'RED'
		sts_B = 'RED'
		print("A: " + sts_A)
		print("B: " + sts_B)

	# second part of section
	if count >= Ss + 1 and count <= Ss + 2:
		# sets the status of each light to the relevant value, prints to terminal
		sts_A = 'RED/AMBER'
		sts_B = 'RED'
		print("A: " + sts_A)
		print("B: " + sts_B)
	
	
def period_a_sec(): # function to control signal status at each second of the cycle start section
	# print status to terminal
	# prints counter to display progress of loop
	print("\n+ - - - - - - - - +\n")
	print("Time: " + str(count) + " second(s)")
	print ("PERIOD A")
	
	# call global variables to function
	global sts_A
	global sts_B
	
	if count >= As and count <= Ae:
		sts_A = 'GREEN'
		sts_B = 'RED'
		print("A: " + sts_A)
		print("B: " + sts_B)

	
def transition_sec(): # function to control signal status at each second of the cycle start section
	# print status to terminal
	# prints counter to display progress of loop
	print("\n+ - - - - - - - - +\n")
	print("Time: " + str(count) + " second(s)")
	print ("TRANSITION")
	
	# call global variables for use in function
	global sts_A
	global sts_B

	if count >= Ts and count <= (Ts + 2):
		sts_A = 'AMBER'
		sts_B = 'RED'
		print("A: " + sts_A)
		print("B: " + sts_B)
		
	if count >= (Ts + 3) and count <= (Te - 3):
		sts_A = 'RED'
		sts_B = 'RED'
		print("A: " + sts_A)
		print("B: " + sts_B)
		
	if count >= (Te - 2) and count <= Te:
		sts_A = 'RED'
		sts_B = 'RED/AMBER'
		print("A: " + sts_A)
		print("B: " + sts_B)
	

def period_b_sec(): # function to control signal status at each second of the cycle start section
	# print status to terminal
	# prints counter to display progress of loop
	print("\n+ - - - - - - - - +\n")
	print("Time: " + str(count) + " second(s)")
	print ("PERIOD B")
	
	# call global variables for use in function
	global sts_A
	global sts_B
	
	if count >= Bs and count <= Be:
		sts_A = 'RED'
		sts_B = 'GREEN'
		print("A: " + sts_A)
		print("B: " + sts_B)


def end_sec(): # function to control signal status at each second of the cycle start section
	# print status to terminal
	# prints counter to display progress of loop
	print("\n+ - - - - - - - - +\n")
	print("Time: " + str(count) + " second(s)")
	print ("CYCLE END")
	
	# call global variables for use in function
	global sts_A
	global sts_B
	
	if count >= Es and count < Ee:
		sts_A = 'RED'
		sts_B = 'AMBER'
		print("A: " + sts_A)
		print("B: " + sts_B)
		
	if count == Ee:
		sts_A = 'RED'
		sts_B = 'RED'
		print("A: " + sts_A)
		print("B: " + sts_B)
		
		
def warmup(): # function to allow the sensors to warm up before being used adjust cycle
	# variable to allow warm-up repetitions of cycle
	reps = 0
	# global count variable is used to access the global timer
	global count
	
	while reps <= 7: # 7 was selected since 600 (10 minutes) / 90 (minimum allowable cycle time) = 6.7
		# version of main loop of program for warm-up, with some changes as necessary
		while count <= cycle_dur: # main loop
			# sets time variable to ensure loop happens every second
			# rather than <loop run time> + 1 second
			start_time = time.time()
			
			# run data_send function as a daemon thread
			data_send_thread = threading.Thread(target = data_send)
			data_send_thread.start()
			
			# if function to run the data_read function when neccesary
			# the range here works every 10 values of count between the start and end of the cycle
			if count == count in range(Ss, Ee, 10):
				# start a thread to run the data_read function as a daemon thread, thread is defined then started
				data_read_thread = threading.Thread(target = data_read)
				data_read_thread.start()
			# data read function is kept to allow sensors to work and warm up
			
			# series of if functions to run the relevant function for section of cycle at correct time
			# convention is when the count value is between the start and end times of the relevant function, the function runs
			
			# for cycle start function
			if count >= Ss and count <= Se:
				start_sec()

			# for period A function
			if count >= As and count <= Ae:
				period_a_sec()

			# for transition function
			if count >= Ts and count <= Te:
				transition_sec()

			# for period b function
			if count >= Bs and count <= Be:
				period_b_sec()

			# for cycle end function
			if count >= Es and count <= Ee:
				end_sec()

			# would normally start the function to adjust cycle times and restart cycle
			# instead, increments the warm-up repetition counter and starts cycle again
			if count == cycle_dur:
				reps += 1
				count = 0

			# increments loop
			count += 1
			# sleeps process for the rest of the second
			# takes process time and removes it from the second, then sleeps for remaining time
			time.sleep(1.0 - ((time.time() - start_time) % 60))
      


# begin initialising the variables needed for cycle
# start with duration of different parts of the cycle 
cycle_dur = input("Enter CYCLE TIME in seconds: ")
cycle_dur = int(cycle_dur)
intergreen = input("Enter INTERGREEN TIME in seconds: ")
intergreen = int(intergreen)
cyc_start_dur = 3
cyc_end_dur = 4
transition_dur = 7 + intergreen
green_split = cycle_dur - cyc_start_dur - transition_dur - cyc_end_dur
phase_count = 2

periodA_dur = green_split / 2
periodA_dur = int(periodA_dur)
periodB_dur = green_split - periodA_dur
periodB_dur = int(periodB_dur)

# print value to terminal
print("\n\tCYCLE TIME\tINTERGREEN\tGREEN SPLIT\tPERIOD A\tPERIOD B\n\t" + str(cycle_dur) + "\t\t" + str(intergreen) + "\t\t" + str(green_split) + "\t\t" + str(periodA_dur) + "\t\t" + str(periodB_dur) +  "\n")

# defines starting values of the statuses of the lights
sts_A = 'RED'
sts_B = 'RED'

# define the start/end times of each stage
# naming convention
# Xs = section start
# Xe = section end
# Sx = Start section
# Ax = period A section
# Tx = transition section
# Bx = period B section
# Ex = end section

Ss = 0
Se = 3
As = Se
Ae = As + periodA_dur
Ts = Ae 
Te = Ts + 7 + intergreen
Bs = Te
Be = Bs + periodB_dur
Es = Be
Ee = Es + 4
# print values to terminal
print("\tSs\tSe\tAs\tAe\tTs\tTe\tBs\tBe\tEs\tEe\n\t" + str(Ss) + "\t" + str(Se) + "\t" + str(As) + "\t" + str(Ae) + "\t" + str(Ts) + "\t" + str(Te) + "\t" + str(Bs) + "\t" + str(Be) + "\t" + str(Es) + "\t" + str(Ee) + "\n")

# set counter for loop
count = 0

# create lists for use throughout functions
eco2_data_A = []
tvoc_data_A = []
redu_data_A = []
oxi_data_A = []
eco2_data_B = []
tvoc_data_B = []
redu_data_B = []
oxi_data_B = []

# warm-up function is run before the main loop to allow sensors to warm up
warmup()

# reinitialises the counter for main loop
count = 0

while count <= cycle_dur: # main loop
	# sets time variable to ensure loop happens every second
	# rather than <loop run time> + 1 second
	start_time = time.time()
	
	# run data_send function as a daemon thread
	data_send_thread = threading.Thread(target = data_send)
	data_send_thread.start()
	
	# if function to run the data_read function when neccesary
	# the range here works every 10 values of count between the start and end of the cycle
	if count == count in range(Ss, Ee, 10):
		# start a thread to run the data_read function as a daemon thread, thread is defined then started
		data_read_thread = threading.Thread(target = data_read)
		data_read_thread.start()
	
	# series of if functions to run the relevant function for section of cycle at correct time
	# convention is when the count value is between the start and end times of the relevant function, the function runs
	
	# for cycle start function
	if count >= Ss and count <= Se:
		start_sec()

	# for period A function
	if count >= As and count <= Ae:
		period_a_sec()

	# for transition function
	if count >= Ts and count <= Te:
		transition_sec()

	# for period b function
	if count >= Bs and count <= Be:
		period_b_sec()

	# for cycle end section function
	if count >= Es and count <= Ee:
		end_sec()

	# for cycle end function that adjusts cycle times and restarts cycle
	if count == cycle_dur:
		cycle_end()
		count = 0
		
	# increments loop
	count += 1
	# sleeps process for the rest of the second
	# takes process time and removes it from the second, then sleeps for remaining time
	time.sleep(1.0 - ((time.time() - start_time) % 60))
		

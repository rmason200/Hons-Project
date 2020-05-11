# import relevant libraries
# system libraries
import time
import threading
from subprocess import call


def cycle_end():
	# find final ratio
	final_ratio =  1
	print("\nFinal ratio: " + str(final_ratio))
	
	global periodA_dur
	global periodB_dur

	# calculate each period druation using the new ratio
	# for equal phase times, each phase duration would be half the available green split
	# to allow a decent time available for both phases, the entire phase time is not adjustable
	# in this instance, half of the available time will be the minimum available, plus the adjusted ratio
	periodA_dur = (green_split / 4) + ((green_split / 4) * final_ratio)
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
	

def data_read():
	print("\nREAD DATA")


def data_send():
	print("\nSEND DATA")
	
	
# begin initialising the variables needed for cycle
# start with duration of different parts of the cycle 
cycle_dur = 110
intergreen = 2
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

	
# variable to allow warm-up repetitions of cycle
reps = 0
# initialise counter
count = 0

warmup_time_start = time.time()

while reps < 7: # 7 was selected since 600 (10 minutes) / 90 (minimum allowable cycle time) = 6.7
	# version of main loop of program for warm-up, with some changes as necessary
	if count <= cycle_dur: # main loop
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
			# print status to terminal
			# prints counter to display progress of loop
			print("\n+ - - - - - - - - +\n")
			print("Repetitions: " + str(reps))
			print("Time: " + str(count) + " second(s)")
			print ("START SECTION")

		# for period A function
		if count >= As and count <= Ae:
			# prints counter to display progress of loop
			print("\n+ - - - - - - - - +\n")
			print("Repetitions: " + str(reps))
			print("Time: " + str(count) + " second(s)")
			print ("PERIOD A")

		# for transition function
		if count >= Ts and count <= Te:
			# prints counter to display progress of loop
			print("\n+ - - - - - - - - +\n")
			print("Repetitions: " + str(reps))
			print("Time: " + str(count) + " second(s)")
			print ("TRANSITION")

		# for period b function
		if count >= Bs and count <= Be:
			# prints counter to display progress of loop
			print("\n+ - - - - - - - - +\n")
			print("Repetitions: " + str(reps))
			print("Time: " + str(count) + " second(s)")
			print ("PERIOD B")

		# for cycle end section function
		if count >= Es and count <= Ee:
			# prints counter to display progress of loop
			print("\n+ - - - - - - - - +\n")
			print("Repetitions: " + str(reps))
			print("Time: " + str(count) + " second(s)")
			print ("END SECTION")

		# for cycle end function that adjusts cycle times and restarts cycle
		if count == cycle_dur:
			cycle_end()
			reps += 1
			count = 0
			

		# increments loop
		count += 1
		# sleeps process for the rest of the second
		# takes process time and removes it from the second, then sleeps for remaining time
		time.sleep(1.0 - ((time.time() - start_time) % 60))


# find time elapsed by warm-up function
elapsed_time = time.time() - warmup_time_start
print("Warm-up length: " + str(elapsed_time) + " seconds")

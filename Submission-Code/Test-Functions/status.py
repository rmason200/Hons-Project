def start_sec(): # function to control signal status at each second of the cycle start section
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
	# call global variables for use in function
	global sts_A
	global sts_B
	
	if count >= Bs and count <= Be:
		sts_A = 'RED'
		sts_B = 'GREEN'
		print("A: " + sts_A)
		print("B: " + sts_B)


def end_sec(): # function to control signal status at each second of the cycle start section
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

# begin initialising the variables needed for cycle
# start with duration of different parts of the cycle 
cycle_dur = 22
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

# defines starting values of the statuses of the lights
sts_A = 'UNCHANGED'
sts_B = 'UNCHANGED'

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

# takes test input
count = input("\nEnter TIME INDEX: ")
count = int(count)
	
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


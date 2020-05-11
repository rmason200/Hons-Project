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

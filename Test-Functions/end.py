# begin initialising the variables needed for cycle
# start with duration of different parts of the cycle 
cycle_dur = 120
cycle_dur = int(cycle_dur)
intergreen = 2
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


# start by finding average reading of each list
# list average = sum of list / number of terms in list
eco2_av_A = input("Enter eCO2 at A: ")
eco2_av_A = int(eco2_av_A)
tvoc_av_A = input("Enter TVOC at A: ")
tvoc_av_A = int(tvoc_av_A)
redu_av_A = input("Enter CO at A: ")
redu_av_A = int(redu_av_A)
oxi_av_A = input("Enter NO2 at A: ")
oxi_av_A = int(oxi_av_A)
eco2_av_B = 100
tvoc_av_B = 100
redu_av_B = 100
oxi_av_B = 100

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

print("eCO2 ratio: " + str(ratios[0]))
print("TVOC ratio: " + str(ratios[1]))
print("CO ratio: " + str(ratios[2]))
print("NO2 ratio: " + str(ratios[3]))

# find mean value of ratios to find final ratio
final_ratio = sum(ratios) / 4
print("\nFinal ratio: " + str(final_ratio))

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

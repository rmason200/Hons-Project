# test for normalisation of data
# setting value of data to test for expected results


# gathering cycle parameters, then making sure they are integers
# values set for testing, can input own values at each run by removing commented info
cyc_time = 90 # input("Enter CYCLE TIME in seconds: ")
cyc_time = int(cyc_time)
intergreen = 10 # input("Enter INTERGREEN TIME in seconds: ")
intergreen = int(intergreen)
ped = 0 # input("Enter PEDESTRIAN TIME in seconds: ")
ped = int(ped)
phase_count = 2

# calculate total available green split
green_split = cyc_time - (intergreen * phase_count) - ped

# present current info to user
print("\n\tCYCLE TIME\tINTERGREEN\tPEDESTRIAN\tGREEN SPLIT\n\t" + str(cyc_time) + "\t\t" + str(intergreen) + "\t\t" + str(ped) + "\t\t" + str(green_split)+ "\n")


# put readings at each unit into lists
readings_A = [1.0, 1.0, 1.0, 1.0]
readings_B = [2.0, 1.5, 0.5, 1.0]
# find ratio of each reading by dividing each reading for entire list
ratios = [a/b for a, b in zip(readings_A, readings_B)]
print("\nRatios: " + str(ratios))

# ratios sorted as first part of normalisation process
ratios.sort()
print("\nSorted Ratios: " + str(ratios))

# normalisation process called min-max normalisation, rescales data to be used
# sets values as 0 to z by subtracting the smallest value in list from each value in list
ratios_0toz = [float(n) - min(ratios) for n in ratios] # n is just index counter
print("\nRatios 0 to Z: " + str(ratios_0toz))
# sets values between 0 and 1 by dividing all values in list by largest value in list
ratios_0to1 = [float(n) / max(ratios_0toz) for n in ratios_0toz]
print("Ratios 0 to 1: " + str(ratios_0to1))
# sets values between 1 and 2 by adding 1 to each value in list
ratios_1to2 = [float(n) + 1 for n in ratios_0to1]
print("Ratios 1 to 2: " + str(ratios_1to2))


# finds final ratio by finding mean value of normalised data
final_ratio = (sum(ratios_0to1)/ 4)
print("\nNormalised Ratio: " + str(final_ratio))

# finding the period durations by adjusting the value of the 
periodA = (green_split / phase_count) * final_ratio
periodA = int(periodA)
periodB = green_split - periodA
periodB = int(periodB)

print("\n\tPeriod A\tPeriod B\n\t" + str(periodA) + "\t\t" + str(periodB) + "\n")


# un_final_ratio = (sum(ratios) / 4)
# print("Non-Normalised Ratios: " + str(un_final_ratio))
# periodA = (green_split / phase_count) * final_ratio
# periodA = int(periodA)
# periodB = green_split - periodA
# periodB = int(periodB)

# print("\n\tPeriod A\tPeriod B\n\t" + str(periodA) + "\t\t" + str(periodB) + "\n")

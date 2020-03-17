# code to modify cycle time of simple 2-light system based on ratio of inputs

# gathering cycle parameters, then making sure they are integers
cyc_time = input("Enter CYCLE TIME in seconds: ")
cyc_time = int(cyc_time)
intergreen = input("Enter INTERGREEN TIME in seconds: ")
intergreen = int(intergreen)
ped = input("Enter PEDESTRIAN TIME in seconds: ")
ped = int(ped)
phase_count = 2     # would be an input in dynamic system
phase_count = int(phase_count)  # unnecessary here, but would be needed if taking input

# calculate total available green split
green_split = cyc_time - (intergreen * phase_count) - ped

# present current info to user
print("\n\tCYCLE TIME\tINTERGREEN\tPEDESTRIAN\tGREEN SPLIT\n\t" + str(cyc_time) + "\t\t\t" + str(intergreen) + "\t\t\t" + str(ped) + "\t\t\t" + str(green_split)+ "\n")

# take user input for weightings
weightA = input("Enter weighting for light A: ")
weightA = int(weightA)
weightB = input("Enter weighting for light B: ")
weightB = int(weightB)

# calculate and print weight ratio
weightRatio = weightA / weightB
print("Weight Ratio: " + str(weightRatio))

periodA = (green_split / phase_count) * weightRatio
periodA = int(periodA)
periodB = green_split - periodA
periodB = int(periodB)

print("\n\tPeriod A\tPeriod B\n\t" + str(periodA) + "\t\t\t" + str(periodB))

exit()
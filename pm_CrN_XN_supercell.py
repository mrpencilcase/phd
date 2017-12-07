import os
import numpy as np

path_xyz = "/home/lukas/documents/thesis/Structures/pmCrN.xyz"
path_save = "/home/lukas/documents/thesis/Structures/"
filename = "test.vasp"
header = "test cell"
a_latt = [21.5,0, 0]
b_latt = [0,8.6,0]
c_latt = [0,0,8.6]
matUp = "Cr"
matDown = "Ag"
matMet = "Ti"

with open(path_xyz,"r") as data:
    supercell = list(data)

posN = []
posUp = []
posDown = []
# Read data from the xyz file of the SQS cell
for pos in supercell:
    line = [ent for ent in pos.split()]
    if line [0] == "N":
        posN.append([float(line[1]), float(line[2]), float(line[3])])
    elif line[0] == "Ti":
        posUp.append([float(line[1]), float(line[2]), float(line[3])])
    elif line[0] == "Cr":
        posDown.append([float(line[1]), float(line[2]), float(line[3])])

# Calculate the relative atom positions

x_min = posN[0][0]
x_max = posN[0][0]
y_min = posN[0][1]
y_max = posN[0][1]
z_min = posN[0][2]
z_max = posN[0][2]


for pos in posN:

    if pos[0] < x_min:
        x_min = pos[0]
    if pos[0] > x_max:
        x_max = pos[0]

    if pos[1] < y_min:
        y_min = pos[1]
    if pos[1] > y_max:
        y_max = pos[1]

    if pos[2] < z_min:
        z_min = pos[2]
    if pos[2] > z_max:
        z_max = pos[2]

for pos in posUp:

    if pos[0] < x_min:
        x_min = pos[0]
    if pos[0] > x_max:
        x_max = pos[0]

    if pos[1] < y_min:
        y_min = pos[1]
    if pos[1] > y_max:
        y_max = pos[1]

    if pos[2] < z_min:
        z_min = pos[2]
    if pos[2] > z_max:
        z_max = pos[2]

for pos in posDown:

    if pos[0] < x_min:
        x_min = pos[0]
    if pos[0] > x_max:
        x_max = pos[0]

    if pos[1] < y_min:
        y_min = pos[1]
    if pos[1] > y_max:
        y_max = pos[1]

    if pos[2] < z_min:
        z_min = pos[2]
    if pos[2] > z_max:
        z_max = pos[2]

x_cell = x_max-x_min
y_cell = y_max-y_min
z_cell = z_max-z_min

print(x_cell)
print(x_min)

for i in range(len(posN)):
    posN[i] = [(((posN[i][0] - x_min) ) / x_cell)*(2./5),
               (posN[i][1] - y_min) / y_cell,
               (posN[i][2] - z_min) / z_cell]
for i in range(len(posUp)):
    posUp[i] = [(((posUp[i][0] - x_min) ) / (x_cell))*(2./5),
               (posUp[i][1] - y_min) / y_cell,
               (posUp[i][2] - z_min) / z_cell]
for i in range(len(posDown)):
    posDown[i] = [(((posDown[i][0] - x_min) ) / ( x_cell))*(2./5),
                 (posDown[i][1] - y_min) / y_cell,
                 (posDown[i][2] - z_min) / z_cell]
print(posN)

posN_a = posN
posN_b = []
pos_met_b = []
# Shift of the postitions of the N and metal atoms is needed!!! to continiue the
#  crystal structure.
for ent in posN:
    pos_met_b.append([ent[0]+0.5,ent[1],ent[2]])

for ent in posUp:
    posN_b.append([ent[0]+0.5,ent[1],ent[2]])

for ent in posDown:
    posN_b.append([ent[0]+0.5,ent[1],ent[2]])

posN_end = []
posDown_end = []
posUp_end = []

for ent in posN:
    if ent[0] == 0:
        posN_end.append([1,ent[1],ent[2]])
for ent in posUp:
    if ent[0] == 0:
        posUp_end.append([1,ent[1],ent[2]])
for ent in posDown:
    if ent[0] == 0:
        posDown_end.append([1,ent[1],ent[2]])

with open(os.path.join(path_save,filename),"w") as file:
    file.write(header+"\n")
    file.write("1\n")
    file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(a_latt[0], a_latt[1], a_latt[2]))
    file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(b_latt[0], b_latt[1], b_latt[2]))
    file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(c_latt[0], c_latt[1], c_latt[2]))
    file.write("{}      {}      {}      {}\n".format(matUp,matDown,matMet,"N"))
    file.write("{}      {}      {}      {}\n".format(len(posUp)+len(posUp_end),
                                        len(posDown)+len(posDown_end),
                                        len(pos_met_b),
                                        len(posN_a)+len(posN_b)+len(posN_end)))
    file.write("Direct\n")
    for ent in posUp:
        file.write("{:6.4f}      {:6.4f}      {:6.4f} ## Cr u\n".format(ent[0],ent[1],ent[2]))

    for ent in posUp_end:
        file.write("{:6.4f}      {:6.4f}      {:6.4f} ## Cr u\n".format(ent[0],ent[1],ent[2]))

    for ent in posDown:
        file.write("{:6.4f}      {:6.4f}      {:6.4f} ## Cr d\n".format(ent[0],ent[1],ent[2]))

    for ent in posDown_end:
        file.write("{:6.4f}      {:6.4f}      {:6.4f} ## Cr d\n".format(ent[0],ent[1],ent[2]))

    for ent in pos_met_b:
        file.write("{:6.4f}      {:6.4f}      {:6.4f} ## Ti\n".format(ent[0],ent[1],ent[2]))

    for ent in posN_a:
        file.write("{:6.4f}      {:6.4f}      {:6.4f} ## Ti\n".format(ent[0],ent[1],ent[2]))

    for ent in posN_b:
        file.write("{:6.4f}      {:6.4f}      {:6.4f} ## N\n".format(ent[0],ent[1],ent[2]))

    for ent in posN_end:
        file.write("{:6.4f}      {:6.4f}      {:6.4f} ## N\n".format(ent[0],ent[1],ent[2]))
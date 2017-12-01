"""
Script to create POSCARS of cleaved supercells. The scripts assumes there
the cleave postions are within the x direction of the supercell and that
there are planes in this dirctions at which the atoms are positoned

"""

import os
import numpy as np

path_xyz = "/home/lukas/documents/thesis/Structures/pmCrN.xyz"
path_save = "/home/lukas/documents/thesis/Structures/"
filename = "test.vasp"
header = "test cell"
a_latt = [21.5, 0, 0]
b_latt = [0, 8.6, 0]
c_latt = [0, 0, 8.6]

cleave_x = 20  # length of the created gap (between 1 and number of planes)
cleave_pos = 1  # position of the gap

# Read the xyz file of the relaxed cell.
with open(path_xyz, "r") as data:
    supercell = list(data)

elements = []
# Read data from the xyz file of the SQS cell
for i in range(2, len(supercell)):
    line = [ent for ent in supercell[i].split()]
    if line[0] not in elements:
        elements.append(line[0])

# Create list of to store the atom positions.
at_pos = [[] for Null in range(len(elements))]
print(at_pos)

for pos in supercell:
    line = [ent for ent in pos.split()]
    if line[0] in elements:
        at_pos[elements.index(line[0])].append(
            [float(line[1]), float(line[2]), float(line[3])])

print([elements])
print(at_pos[0])
print(at_pos[1])
print(at_pos[2])
# Calculate the extreme atom positions

x_min = at_pos[0][0][0]
x_max = at_pos[0][0][0]
y_min = at_pos[0][0][1]
y_max = at_pos[0][0][1]
z_min = at_pos[0][0][2]
z_max = at_pos[0][0][2]

for el_pos in at_pos:
    for pos in el_pos:

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

x_cell = x_max - x_min
y_cell = y_max - y_min
z_cell = z_max - z_min

for i in range(len(at_pos)):
    for j in range(len(at_pos[i])):
        at_pos[i][j][0] = at_pos[i][j][0] - x_min
        at_pos[i][j][1] = at_pos[i][j][1] - y_min
        at_pos[i][j][2] = at_pos[i][j][2] - z_min

# Determin unique x postions
x_pos = []
for el_pos in at_pos:
    for pos in el_pos:
        if pos[0] not in x_pos:
            x_pos.append(pos[0])
x_pos.sort()

if cleave_pos > len(x_pos):
    print("The postion of the cleave is not in the super cell. \n"
          "Please change the postions and start the script again."
          )
    exit()

for i in range(len(at_pos)):
    for j in range(len(at_pos[i])):
        if at_pos[i][j][0] > x_pos[cleave_pos - 1]:
            at_pos[i][j][0] += cleave_x
x_cell += cleave_x

for i in range(len(at_pos)):
    for j in range(len(at_pos[i])):
        at_pos[i][j][0] = at_pos[i][j][0] / x_cell
        at_pos[i][j][1] = at_pos[i][j][1] / y_cell
        at_pos[i][j][2] = at_pos[i][j][2] / z_cell



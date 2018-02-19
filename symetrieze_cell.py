"""
Script to symmetrize the sub cell of the distorted CrN lattice
"""

import os

path = "/home/lukas/documents/thesis/Structures/substructures_CrN_and_TiN/CrN110_red.vasp"

with open(path,"r") as file:
    cell_data = list(file)

coordinates = []
# read atom coordinates
for i in range(8,len(cell_data)):
    coordinates.append([float(ent) for ent in cell_data[i].split()])

# determine extreme values
x_min = coordinates[0][0]
x_max = coordinates[0][0]

y_min = coordinates[0][1]
y_max = coordinates[0][1]

z_min = coordinates[0][2]
z_max = coordinates[0][2]

for cor in coordinates:
    if cor[0] < x_min:
        x_min = cor[0]
    if cor[0] > x_max:
        x_max = cor[0]

    if cor[1] < y_min:
        y_min = cor[1]
    if cor[1] > y_max:
        y_max = cor[1]

    if cor[2] < z_min:
        z_min = cor[2]
    if cor[2] > z_max:
        z_max = cor[2]

# shift atoms
for i in range(len(coordinates)):
    coordinates[i][0] -= x_min
    coordinates[i][1] -= y_min
    coordinates[i][2] -= z_min

# x_shift : distance between the two selected atoms
#x_shift = coordinates[0][0]-coordinates[5][0]
#coordinates[9][0] = coordinates[4][0] - x_shift

print(coordinates[4][0]-coordinates[0][0])

path = "/home/lukas/documents/thesis/Structures/substructures_CrN_and_TiN/mod.vasp"
with(open(path,"w")) as file:
    for i in range(2):
        file.write(cell_data[i])
    # file.write("{:8.6f}   {:8.6f}    {:8.6f}\n".format((x_max - x_min), 0, 0))
    # file.write("{:8.6f}   {:8.6f}    {:8.6f}\n".format(0, (y_max - y_min), 0))
    # file.write("{:8.6f}   {:8.6f}    {:8.6f}\n".format(0, 0, (z_max - z_min)))
    for i in range(2,8):
        file.write(cell_data[i])
    for cor in coordinates:
        file.write("{:8.6f}  {:8.6f}  {:8.6f}\n".format(cor[0],cor[1],cor[2]))

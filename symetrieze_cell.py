import os

path = "/home/lukas/documents/thesis/upload/relax/af_CrN_Nstruct_1/POSCAR.vasp"

with open(path,"r") as file:
    cell_data = list(file)

coordinates = []
for i in range(8,len(cell_data)):
    coordinates.append([float(ent) for ent in cell_data[i].split()])

x_min = coordinates[0][0]
x_max = coordinates[0][0]

for cor in coordinates:
    if cor[0] < x_min:
        x_min = cor[0]

    if cor[0] > x_max:
        x_max = cor[0]

for i in range(len(coordinates)):
    coordinates[i][0] -= x_min

x_shift = coordinates[0][0]-coordinates[5][0]
coordinates[9][0] = coordinates[4][0] - x_shift

print(coordinates[4vi ][0]-coordinates[0][0])

path = "/home/lukas/documents/thesis/upload/relax/af_CrN_Nstruct_1/mod.vasp"
with(open(path,"w")) as file:
    for i in range(8):
        file.write(cell_data[i])
    for cor in coordinates:
        file.write("{:8.6f}  {:8.6f}  {:8.6f}\n".format(cor[0],cor[1],cor[2]))

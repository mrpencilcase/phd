import os
import numpy as np

path_open,filename = os.path.split("/home/lukas/Documents/thesis/Structures/orth_af_CrN_TiN_s_export.vasp")
with open(os.path.join(path_open,filename),"r") as data:
    poscar = list(data)

atom_pos = []
n_cleave = 3
gap_cleave = 20
lattice = []
lattice.append([float(cor) for cor in poscar[2].split()])
lattice.append([float(cor) for cor in poscar[3].split()])
lattice.append([float(cor) for cor in poscar[4].split()])

lattice = np.asarray(lattice)

for i in range(8,len(poscar)):
    atom_pos.append([float(cor) for cor in poscar[i].split()])

atom_pos = np.asarray(atom_pos)
atom_pos = np.dot(atom_pos,lattice)

x_pos = [ent[0] for ent in atom_pos ]
x_pos = set(x_pos)
x_pos = sorted(x_pos)
n_x_u = len(set(x_pos))
lattice[0,0] = lattice[0,0] + gap_cleave
i = 0
while i in range(len(atom_pos[:,0])):
    if atom_pos[i,0] >= x_pos[n_cleave]:
        atom_pos[i,0] += gap_cleave
    i += 1

print(lattice)
inv_lat = lattice*1
print(inv_lat)
inv_lat[0,0] = 1./lattice[0,0]
inv_lat[1,1] = 1./lattice[1,1]
inv_lat[2,2] = 1./lattice[2,2]
print(inv_lat)
atom_pos = np.dot(atom_pos,inv_lat)
with open(os.path.join(path_open,"cleave_"+filename),"w") as out_file:
    out_file.write(poscar[0])
    out_file.write(poscar[1])
    i = 0
    while i in range(len(lattice[:,0])):
        out_file.write("{:6.4f}  {:6.4f}  {:6.4f}\n".format(lattice[i,0],
                                                    lattice[i,1],lattice[i,2]))
        i += 1
    out_file.write(poscar[5])
    out_file.write(poscar[6])
    out_file.write(poscar[7])

    while i in range(len(atom_pos[:,0])):
        out_file.write("{:6.4f}  {:6.4f}  {:6.4f}\n".format(atom_pos[i,0],
                                                atom_pos[i,1],atom_pos[i,2]))
        i += 1
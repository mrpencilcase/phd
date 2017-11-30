"""
author : Lukas
python : 3.5

Skript to create a Supercell

Takes the coordinate data provided by the xyz file from VESTA and formats it
to the needs of VASP for an POSCAR file
"""

import os
import numpy as np
from numpy import linalg as la


class Phase():
    def __init__(self, elements, lattice):
        self.elements = elements
        self.lattice = lattice


class Structure():
    def __init__(self):
        self.layer_1
        self.layer_2


path_save = "/home/lukas/Documents/thesis/Structures/"
filename = "CrN_TiN_test"
info = "5 planes per material, af config"
CrN = Phase(["Cr", "N"], 4.438)
TiN = Phase(["Ti", "N"], 4.438)
n_planes_1 = 6
n_planes_2 = 6
# Atom positions for NaCl structure in one plane. The first 4 entires are
# occupied by ones atom species the last one by the other.
nacl_struct_1 = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0.5, 0.5]])
nacl_struct_2 = np.array([[0.5, 0], [0.5, 1], [1, 0.5], [0, 0.5]])
x1_full = np.array([[1], [1], [1], [1], [1]])
x2_full = np.array([[1], [1], [1], [1]])

nacl_struct_1_red = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
nacl_struct_2_red = np.array([[0.5, 0.5]])
x1_red = np.array([[1], [1], [1], [1]])
x2_red = np.array([[1]])

# Atom positions for the POSCAR file which already consider the equivalenz of
# different atom postions.
nacl_pos1 = np.array([[0, 0], [0.5, 0.5]])
nacl_pos2 = np.array([[0.5, 0], [0, 0.5]])

x_pos_1 = np.array([[1], [1]])
x_pos_2 = np.array([[1], [1]])

# Used structure prameters
struct_1 = nacl_pos1
struct_2 = nacl_pos2
x1 = x_pos_1
x2 = x_pos_2
lattice_par = (CrN.lattice + TiN.lattice) / 2
half_plane_shift = lattice_par / 2

Cr_pos = []
Ti_pos = []
N_pos = []
i = 0
gap = 20
gap_pos = 20
plane_1 = 0
plane_2 = 0
shift = 0
add_end = True

while i in range(n_planes_1 + n_planes_2):

    if i < n_planes_1:
        add_1 = struct_1 * lattice_par
        add_2 = struct_2 * lattice_par

        if plane_1 == 0:

            x = x1 * shift
            add = np.ndarray.tolist(np.concatenate((x, add_1), 1))
            Cr_pos.extend(add)

            x = x2 * shift
            add = np.ndarray.tolist(np.concatenate((x, add_2), 1))
            N_pos.extend(add)
            plane_1 = 1

        else:
            x = x1 * shift
            add = np.ndarray.tolist(np.concatenate((x, add_1), 1))
            N_pos.extend(add)
            x = x2 * shift
            add = np.ndarray.tolist(np.concatenate((x, add_2), 1))
            Cr_pos.extend(add)
            plane_1 = 0

    else:
        add_1 = struct_1 * lattice_par
        add_2 = struct_2 * lattice_par

        if plane_2 == 0:
            x = x1 * shift
            add = np.ndarray.tolist(np.concatenate((x, add_1), 1))
            Ti_pos.extend(add)
            x = x2 * shift
            add = np.ndarray.tolist(np.concatenate((x, add_2), 1))
            N_pos.extend(add)
            plane_2 = 1

        else:
            x = x1 * shift
            add = np.ndarray.tolist(np.concatenate((x, add_1), 1))
            N_pos.extend(add)
            x = x2 * shift
            add = np.ndarray.tolist(np.concatenate((x, add_2), 1))
            Ti_pos.extend(add)
            plane_2 = 0

    if i == gap_pos and gap_pos < n_planes_1 + n_planes_2:
        shift = shift + gap - half_plane_shift
    shift += half_plane_shift
    i += 1
shift -= half_plane_shift

if add_end == True:
    shift += half_plane_shift
    if plane_2 == 0:
        x = x1 * shift
        add = np.ndarray.tolist(np.concatenate((x, add_1), 1))
        Cr_pos.extend(add)
        x = x2 * shift
        add = np.ndarray.tolist(np.concatenate((x, add_2), 1))
        N_pos.extend(add)
        plane_2 = 1

    else:
        x = x1 * shift
        add = np.ndarray.tolist(np.concatenate((x, add_1), 1))
        N_pos.extend(add)
        x = x2 * shift
        add = np.ndarray.tolist(np.concatenate((x, add_2), 1))
        Cr_pos.extend(add)
        plane_2 = 0

# reduce to relatice coordinates of the super cell

i = 0
while i in range(len(Cr_pos)):
    Cr_pos[i][0] = Cr_pos[i][0] / shift
    Cr_pos[i][1] = Cr_pos[i][1] / lattice_par
    Cr_pos[i][2] = Cr_pos[i][2] / lattice_par
    i += 1

i = 0
while i in range(len(Ti_pos)):
    Ti_pos[i][0] = Ti_pos[i][0] / shift
    Ti_pos[i][1] = Ti_pos[i][1] / lattice_par
    Ti_pos[i][2] = Ti_pos[i][2] / lattice_par
    i += 1

i = 0
while i in range(len(N_pos)):
    N_pos[i][0] = N_pos[i][0] / shift
    N_pos[i][1] = N_pos[i][1] / lattice_par
    N_pos[i][2] = N_pos[i][2] / lattice_par
    i += 1

# Split Cr atoms in spin up and down groups for a af configuration
Cr_pos_up = []
Cr_pos_down = []

for atom in Cr_pos:

    if atom[2] == 0 or atom[2] == 1:
        Cr_pos_up.append((atom))

    if atom[2] == 0.5:
        Cr_pos_down.append(atom)

# Create the poscar file
with open(os.path.join(path_save, filename + ".vasp"), 'w') as file:
    file.write(filename + "  " + info + "\n")
    file.write("1\n")
    file.write("{:6.4f}    0.0000     0.0000\n".format(shift))
    file.write("0.0000     {:6.4f}    0.0000\n".format(lattice_par))
    file.write("0.0000    0.0000     {:6.4f}\n".format(lattice_par))
    file.write("{}      {}      {}      {}\n".format(CrN.elements[0],
                                                     CrN.elements[0],
                                                     TiN.elements[0],
                                                     CrN.elements[1]))
    file.write("{}      {}      {}      {}\n".format(len(Cr_pos_up),
                                                     len(Cr_pos_down),
                                                     len(Ti_pos),
                                                     len(N_pos)))
    file.write("Direct\n")

    for ent in Cr_pos_up:
        file.write("{:5.4f}      {:5.4f}      {:5.4f}\n".format(ent[0],
                                                                ent[1], ent[2]))
    for ent in Cr_pos_down:
        file.write("{:5.4f}      {:5.4f}      {:5.4f}\n".format(ent[0],
                                                                ent[1], ent[2]))
    for ent in Ti_pos:
        file.write("{:5.4f}      {:5.4f}      {:5.4f}\n".format(ent[0],
                                                                ent[1], ent[2]))
    for ent in N_pos:
        file.write("{:5.4f}      {:5.4f}      {:5.4f}\n".format(ent[0],
                                                                ent[1], ent[2]))
print(len(Cr_pos))
print(len(Ti_pos))
print(len(N_pos))

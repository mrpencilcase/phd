"""
author : Lukas
python : 3.5

Skript to create a Supercell

Takes the coordinate data provided by the xyz file from VESTA and formats it
to the needs of VASP for an POSCAR file
"""

import os
import numpy as np


class Structure():
    def __init__(self, elements, lattice):
        self.elements = elements
        self.lattice = lattice


path_save = "/home/lukas/Documents/Thesis/Strutures/"
filename = "CrN_af_1x1x1"
info = ""
CrN = Structure(["Cr", "N"], 4.138)

n_planes = 3

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

struct_1 = nacl_struct_1
struct_2 = nacl_struct_2
x1 = x1_full
x2 = x2_full
lattice_par = CrN.lattice
half_plane_shift = lattice_par / 2

at1_pos = []
at2_pos = []
i = 0
gap = 20
gap_pos = 7
plane_1 = 0
plane_2 = 0
shift = 0

while i in range(n_planes):

    add_1 = struct_1 * lattice_par
    add_2 = struct_2 * lattice_par

    if plane_1 == 0:

        x = x1 * shift
        add = np.ndarray.tolist(np.concatenate((x, add_1), 1))
        at1_pos.extend(add)

        x = x2 * shift
        add = np.ndarray.tolist(np.concatenate((x, add_2), 1))
        at2_pos.extend(add)
        plane_1 = 1

    else:
        x = x1 * shift
        add = np.ndarray.tolist(np.concatenate((x, add_1), 1))
        at2_pos.extend(add)
        x = x2 * shift
        add = np.ndarray.tolist(np.concatenate((x, add_2), 1))
        at1_pos.extend(add)
        plane_1 = 0

    shift += half_plane_shift
    i += 1
    if i == gap_pos and gap_pos < n_planes:
        shift = shift + gap - half_plane_shift
shift -= half_plane_shift

spin_group_1 = []
spin_group_2 = []

i = 0
while i in range(len(at1_pos)):
    at1_pos[i][0] = at1_pos[i][0] / shift
    at1_pos[i][1] = at1_pos[i][1] / lattice_par
    at1_pos[i][2] = at1_pos[i][2] / lattice_par
    i += 1

i = 0
while i in range(len(at2_pos)):
    at2_pos[i][0] = at2_pos[i][0] / shift
    at2_pos[i][1] = at2_pos[i][1] / lattice_par
    at2_pos[i][2] = at2_pos[i][2] / lattice_par
    i += 1

for atom in at1_pos:

    if atom[2] == 0 or atom[2] == 1:
        spin_group_1.append((atom))

    if atom[2] == 0.5:
        spin_group_2.append(atom)
# Create the poscar file

with open(os.path.join(path_save, filename + ".vasp"), 'w') as file:
    file.write(filename + "   " + info + "\n")
    file.write("1\n")
    file.write("{:6.4f}    0.0000     0.0000\n".format(shift))
    file.write("0.0000     {:6.4f}    0.0000\n".format(lattice_par))
    file.write("0.0000    0.0000     {:6.4f}\n".format(lattice_par))
    file.write("{}   {}   {}\n".format(CrN.elements[0], CrN.elements[0],
                                       CrN.elements[1]))
    file.write("{}   {}   {}\n".format(len(spin_group_1), len(spin_group_2),
                                       len(at2_pos)))
    file.write("Direct\n")

    for ent in spin_group_1:
        file.write(
            "{:5.4f}      {:5.4f}      {:5.4f}     \n".format(ent[0], ent[1],
                                                              ent[2]))

    for ent in spin_group_2:
        file.write(
            "{:5.4f}      {:5.4f}      {:5.4f}     \n".format(ent[0], ent[1],
                                                              ent[2]))

    for ent in at2_pos:
        file.write(
            "{:5.4f}      {:5.4f}      {:5.4f}     \n".format(ent[0], ent[1],
                                                              ent[2]))
print("finished")

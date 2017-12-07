"""
Script to create POSCARS of a cleaved supercell. The script cleaves the cell
allong the given axis. As input file all POSCAR like files are tollerated.
Important is that the coordinates of the atoms are given in cartesian
coordinates.
"""

import os
import numpy as np


def cleave_cell(cleave_axis, cleave_d, cleave_pos, path_open, path_save):
    """
    Function to split the supercell at a certain postion
    :param cleave_axis:
    :param cleave_d: Distance of the created gap
    :param cleave_pos: Postion of the gap
    :param path_xyz:  Path to the relaxed supercell
    :param path_save: Path where the file should be stored (incl. filename)
    :return: None!! A file is created at the postion of path_save
    """

    delta_c = 0.8

    # Read the xyz file of the relaxed cell.
    with open(path_open, "r") as data:
        supercell = list(data)
    a_lattice = [float(ent) for ent in supercell[2].split()]
    b_lattice = [float(ent) for ent in supercell[3].split()]
    c_lattice = [float(ent) for ent in supercell[4].split()]
    ele_type = [ent for ent in supercell[5].split()]
    ele_num = [int(ent) for ent in supercell[6].split()]
    at_pos = []
    for i in range(8,len(supercell)):
        at_pos.append([float(ent) for ent in supercell[i].split()])

    if cleave_axis == "a":
        axis_index = 0
        a_lattice[axis_index] += cleave_d
    elif cleave_axis == "b":
        axis_index = 1
        b_lattice[axis_index] += cleave_d
    elif cleave_axis == "c":
        axis_index = 2
        c_lattice[axis_index] += cleave_d

    c_pos = []
    for pos in at_pos:
        if pos[axis_index] not in c_pos:
            c_pos.append(pos[axis_index])
    c_pos.sort()
    print((c_pos))
    i = 0
    while i < len(c_pos)-1:
        if c_pos[i+1] <= c_pos[i]+delta_c:
            c_pos.pop(i+1)
            i = -1
        i += 1
    print(c_pos)
    if cleave_pos > len(c_pos):
        print("The postion of the cleave is not in the super cell. \n"
              "Please change the postions and start the script again."
              )
        exit()

    for i in range(len(at_pos)):
        if at_pos[i][axis_index] > c_pos[cleave_pos - 1]+ delta_c:
            at_pos[i][axis_index] += cleave_d

    el_num_str = []
    for num in ele_num:
        el_num_str.append(str(num))

    with open(path_save,"w") as file:
        file.write(supercell[0])
        file.write(supercell[1])
        for vec in [a_lattice,b_lattice,c_lattice]:
            file.write("{:7.4f}  {:7.4f}  {:7.4f}\n".format(vec[0], vec[1], vec[2]))
        file.write("    ".join(ele_type) + "\n")
        file.write("  ".join(el_num_str) + "\n")
        file.write("Cartesian\n")
        for pos in at_pos:
            file.write("{:7.4f}  {:7.4f}  {:7.4f}\n".format(pos[0],pos[1],pos[2]))

def main():
    path_open = "/home/lukas/documents/thesis/Structures/afCrNTiN_1-10.vasp"

    dir_save_b = "/home/lukas/documents/thesis/Structures/CrNTiN_cleaved/afCrNTiN_1-10/"
    filename = "POSCAR"
    cleave_axis = "a"
    # length of the created gap (between 1 and number of planes)
    cleave_positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # position of the gap
    cleave_distances = [0.2,0.4,0.6,0.8,1,1.2,1.4,1.6,1.8,2,2.5,3,3.5,4,4.5,5]

    for cleave_d in cleave_distances:
        for cleave_pos in cleave_positions:
            dir_save = os.path.join(dir_save_b,"{}".format(cleave_pos))
            dis_str = str(cleave_d)
            if "." in dis_str:
                dis_str.replace(".","")

            filename_full = filename + "_p{}_d{}.vasp".format(cleave_pos,dis_str)
            path_save = os.path.join(dir_save, filename_full)
            cleave_cell(cleave_axis, cleave_d, cleave_pos,
                        path_open, path_save)


if __name__ == "__main__":
    main()

"""
Script to create POSCARS of a cleaved supercell. The script cleaves the cell
allong the given axis. As input file all POSCAR like files are tollerated.
Important is that the coordinates of the atoms are given in cartesian
coordinates.
"""

import os
from read_poscar import read_poscar
import numpy as np


def cleave_cell(cleave_axis, cleave_d, cleave_pos, path_open):
    """
    Function to split the supercell at a certain postion
    :param path_open:
    :param cleave_axis:
    :param cleave_d: Distance of the created gap
    :param cleave_pos: Postion of the gap
    :return: None!! A file is created at the postion of path_save
    """
    delta_c = 0.8

    poscar = read_poscar(path_open, "base cell")

    a_lattice = poscar.lattice.a
    b_lattice = poscar.lattice.b
    c_lattice = poscar.lattice.c
    ele_type = poscar.elements.element_type
    ele_num = poscar.elements.element_amount
    at_pos = []
    for at in poscar.atoms:
        at_pos.append(at.position)

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

    i = 0
    while i < len(c_pos) - 1:
        if c_pos[i + 1] <= c_pos[i] + delta_c:
            c_pos.pop(i + 1)
            i = -1
        i += 1

    if cleave_pos > len(c_pos):
        print("The postion of the cleave is not in the super cell. \n"
              "Please change the postions and start the script again."
              )
        exit()

    for i in range(len(at_pos)):
        if at_pos[i][axis_index] > c_pos[cleave_pos - 1] + delta_c:
            at_pos[i][axis_index] += cleave_d

    el_num_str = []
    for num in ele_num:
        el_num_str.append(str(num))

    file = ["{}\n".format(poscar.info), "{}\n".format(str(poscar.scale))]

    for vec in [a_lattice, b_lattice, c_lattice]:
        file.append(
            "{:7.4f}  {:7.4f}  {:7.4f}\n".format(vec[0], vec[1], vec[2]))
    file.append("    ".join(ele_type) + "\n")
    file.append("  ".join(el_num_str) + "\n")
    file.append("Cartesian\n")
    for pos in at_pos:
        file.append(
            "{:7.4f}  {:7.4f}  {:7.4f}\n".format(pos[0], pos[1], pos[2]))
    return file


def main():
    path_open = "/home/lukas/documents/thesis/result_vasp/relax/CrNTiN/CrN_TiN_110/relax_af_CrN_TiN_110/"

    dir_save_b = "/home/lukas/documents/thesis/Structures/TiN_cleaved/12_sheets/"
    filename = "POSCAR"
    cleave_axis = "a"
    # length of the created gap (between 1 and number of planes)
    cleave_positions = [1]  # position of the gap
    cleave_distances = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.5, 3,
                        3.5, 4, 4.5, 5]

    for cleave_d in cleave_distances:
        for cleave_pos in cleave_positions:
            dir_save = os.path.join(dir_save_b, "{}".format(cleave_pos))
            dis_str = str(cleave_d)
            if "." in dis_str:
                dis_str.replace(".", "")

            filename_full = filename + "_p{}_d{}.vasp".format(cleave_pos,
                                                              dis_str)
            path_save = os.path.join(dir_save, filename_full)
            outcar = cleave_cell(cleave_axis, cleave_d, cleave_pos,
                                 path_open)


if __name__ == "__main__":
    main()

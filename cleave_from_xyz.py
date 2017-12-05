"""
Script to create POSCARS of cleaved supercells. The scripts assumes there
the cleave postions are within the x direction of the supercell and that
there are planes in this dirctions at which the atoms are positoned

"""

import os
import numpy as np


def cleave_cell(lattice, cleave_axis, cleave_d, cleave_pos, path_xyz, path_save,
                header):
    """
    Function to split the supercell at a certain postion
    :param lattice:
    :param cleave_axis:
    :param cleave_d: Distance of the created gap
    :param cleave_pos: Postion of the gap
    :param path_xyz:  Path to the relaxed supercell
    :param path_save: Path where the file should be stored (incl. filename)
    :param header: Information for the first line in the OUTCAR
    :return: None!! A file is created at the postion of path_save
    """
    a_latt = lattice[0]
    b_latt = lattice[1]
    c_latt = lattice[2]
    cleave_axis_len = 0
    filetype = "xyz"
    delta_c = 0.8
    if cleave_axis == "a":
        axis_index = 0
    elif cleave_axis == "b":
        axis_index = 1

    elif cleave_axis == "c":
        axis_index = 2

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

    for pos in supercell:
        line = [ent for ent in pos.split()]
        if line[0] in elements:
            at_pos[elements.index(line[0])].append(
                [np.around(float(line[1]), 5), np.around(float(line[2]), 5),
                 np.around(float(line[3]), 5)])

    # Calculate the extreme atom positions

    # x_min = at_pos[0][0][0]
    # x_max = at_pos[0][0][0]
    # y_min = at_pos[0][0][1]
    # y_max = at_pos[0][0][1]
    # z_min = at_pos[0][0][2]
    # z_max = at_pos[0][0][2]
    #
    # for el_pos in at_pos:
    #     for pos in el_pos:
    #
    #         if pos[0] < x_min:
    #             x_min = pos[0]
    #         if pos[0] > x_max:
    #             x_max = pos[0]
    #
    #         if pos[1] < y_min:
    #             y_min = pos[1]
    #         if pos[1] > y_max:
    #             y_max = pos[1]
    #
    #         if pos[2] < z_min:
    #             z_min = pos[2]
    #         if pos[2] > z_max:
    #             z_max = pos[2]
    #
    # x_cell = x_max - x_min
    # y_cell = y_max - y_min
    # z_cell = z_max - z_min
    # print(x_cell)
    #
    #
    #
    # for i in range(len(at_pos)):
    #     for j in range(len(at_pos[i])):
    #         at_pos[i][j][0] = at_pos[i][j][0] - x_min
    #         at_pos[i][j][1] = at_pos[i][j][1] - y_min
    #         at_pos[i][j][2] = at_pos[i][j][2] - z_min

    # Determine unique atom positions in the cleave axis.
    c_pos = []
    c_pos_cleared = []
    c_pos_dummy_f = []
    c_pos_dummy_e = []
    c_pos_final = []
    for el_pos in at_pos:
        for pos in el_pos:
            if pos[axis_index] not in c_pos:
                c_pos.append(pos[axis_index])
    c_pos.sort()
    c_pos_final = c_pos
    print(c_pos_final)
    print(len(c_pos_final))
    # Compare postion one with all other and ignore all in range
    # Make new array and compare again first entry with all other to find
    # entries range
    # If none are found look at the second entry and look for entries in range
    # Make new array without entries in range of second entrie.
    c_pos_dummy_e = c_pos
    i = 0
    while i < len(c_pos_dummy_e)-1:
        if c_pos_dummy_e[i+1] <= c_pos_dummy_e[i]+delta_c:
            c_pos_dummy_e.pop(i+1)
            i = -1
        i += 1
    c_pos_final = c_pos_dummy_e

    if cleave_pos > len(c_pos_final):
        print("The postion of the cleave is not in the super cell. \n"
              "Please change the postions and start the script again."
              )
        exit()

    for i in range(len(at_pos)):
        for j in range(len(at_pos[axis_index])):
            if at_pos[i][j][axis_index] > c_pos_final[cleave_pos - 1]+ delta_c:
                at_pos[i][j][axis_index] += cleave_d

    # if cleave_axis == "a":
    #     x_cell += cleave_d
    # elif cleave_axis == "b":
    #     y_cell += cleave_d
    # elif cleave_axis == "c":
    #     y_cell += cleave_d

    if filetype == "VASP":
        for i in range(len(at_pos)):
            for j in range(len(at_pos[i])):
                at_pos[i][j][0] = at_pos[i][j][0] / x_cell
                at_pos[i][j][1] = at_pos[i][j][1] / y_cell
                at_pos[i][j][2] = at_pos[i][j][2] / z_cell
        len_pos = []
        for el_pos in at_pos:
            len_pos.append(str(len(el_pos)))


        with open(path_save, "w") as file:
            file.write(header + "\n")
            file.write("1\n")
            file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(a_latt[0],
                                                            a_latt[1], a_latt[2]))
            file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(b_latt[0],
                                                            b_latt[1], b_latt[2]))
            file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(c_latt[0],
                                                            c_latt[1], c_latt[2]))
            file.write("    ".join(elements) + "\n")
            file.write("    ".join(len_pos) + "\n")
            file.write("Direct\n")
            for el_pos in at_pos:
                for pos in el_pos:
                    file.write(
                        "{:6.4f}      {:6.4f}      {:6.4f}\n".format(pos[0], pos[1],
                                                                    pos[2]))
    elif filetype == "xyz":

        at_num = 0
        for el_pol in at_pos:
            at_num += len(el_pos)

        with open(path_save,"w") as file:
            file.write(supercell[0])
            file.write(supercell[1])

            for el_pos, el in zip(at_pos,elements):
                for pos in el_pos:
                    file.write(
                        " {}    {:6.4f}      {:6.4f}      {:6.4f}\n".
                            format(el, pos[0], pos[1], pos[2]))


def main():
    path_xyz = "/home/lukas/documents/thesis/Structures/pmCrN.xyz"
    path_xyz = "/home/lukas/documents/thesis/Structures/afCrNTiN_1-10.xyz"

    dir_save = "/home/lukas/documents/thesis/Structures" \
               "/CrNTin_cleaved/afCrNTiN_110/"
    filename = "CrNTiN_110"
    header = "af CrN TiN 110 interface"

    lattice_CrNTiN_110 = [
        [5.89584737116127, 0.00145103901071, 0.00000000000000],
        [0.00474199711955, 17.88908655024918, 0.00000000000000],
        [0.00000000000000, 0.00000000000000, 4.19716843678857]]

    lattice_CrNTiN_1_10 = [[17.600294097894, 0.000000000000, 0.000000000000],
                           [0.00000000000, 2.99968316020, 0.00000000000],
                           [0.00000000000, 0.00000000000, 4.19651745818]]

    cleave_axis = "a"
    cleave_x = 20  # length of the created gap (between 1 and number of planes)
    cleave_positions = [1, 3, 6, 9, 11]  # position of the gap
    cleave_positions = [6]

    for cleave_pos in cleave_positions:
        filename_full = filename + "_c{}.vasp".format(cleave_pos)
        path_save = os.path.join(dir_save, filename_full)
        cleave_cell(lattice_CrNTiN_110, cleave_axis, cleave_x, cleave_pos,
                    path_xyz, path_save, header)


if __name__ == "__main__":
    main()

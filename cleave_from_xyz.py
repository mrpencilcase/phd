"""
Script to create POSCARS of cleaved supercells. The scripts assumes there
the cleave postions are within the x direction of the supercell and that
there are planes in this dirctions at which the atoms are positoned

"""

import os
import numpy as np

def cleave_cell(lattice,cleave_axis,cleave_d, cleave_pos, path_xyz, path_save, header):
    """
    Function to split the supercell at a certain postion
    :param lalttic: Lattice vectors of the supercell
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

    if cleave_axis == "a":
        axis_index = 0
        cleave_axis_len = np.linalg.norm(a_latt)
    elif cleave_axis == "b":
        axis_index = 1
        cleave_axis_len = np.linalg.norm(b_latt)
    elif cleave_axis == "c":
        axis_index = 2
        cleave_axis_len = np.linalg.norm(c_latt)

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
                [np.around(float(line[1]),5), np.around(float(line[2]),5),
                 np.around(float(line[3]),5)])

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

    # Determine unique atom positions in the cleave axis.
    c_pos = []
    c_pos_cleared = []
    c_pos_dummy = []
    c_pos_final = []
    for el_pos in at_pos:
        for pos in el_pos:
            if pos[axis_index] not in c_pos:
                c_pos.append(pos[axis_index])
    c_pos.sort()
    print(c_pos)
    print(len(c_pos))

    i = 0
    while i < len(c_pos):
        c_pos_dummy.append(c_pos[i])
        j = i + 1
        while j < len(c_pos):
            if c_pos[i]+0.02*cleave_axis_len < c_pos[j]:
                c_pos_dummy.append(c_pos[j])

            j += 1
        c_pos_final.append(c_pos[i])
        c_pos = c_pos_dummy
        c_pos_dummy = []
        i += 1
    print(c_pos_final)
    for i in range(1,len(c_pos)):
        for pos in c_pos:
#            print(c_pos[i])
#            print(pos)

#            print(c_pos[i] != pos )
#            print(c_pos.index(pos))
#            print( i > c_pos.index(pos))
            if c_pos[i]+0.02*cleave_axis_len > pos and c_pos[i] != pos and i > c_pos.index(pos):
                c_pos_dummy.append(c_pos.index(pos))

    print(len(c_pos))
    print(cleave_pos)
    if cleave_pos > len(c_pos_final):
        print("The postion of the cleave is not in the super cell. \n"
              "Please change the postions and start the script again."
              )
        exit()

    for i in range(len(at_pos)):
        for j in range(len(at_pos[axis_index])):
            if at_pos[i][j][axis_index] > c_pos_final[cleave_pos - 1]:
                at_pos[i][j][axis_index] += cleave_d

    if cleave_axis == "a":
        x_cell += cleave_d
    elif cleave_axis == "b":
        y_cell += cleave_d
    elif cleave_axis == "c":
        y_cell += cleave_d

    for i in range(len(at_pos)):
        for j in range(len(at_pos[i])):
            at_pos[i][j][0] = at_pos[i][j][0] / x_cell
            at_pos[i][j][1] = at_pos[i][j][1] / y_cell
            at_pos[i][j][2] = at_pos[i][j][2] / z_cell
    len_pos = []
    for el_pos in at_pos:
        len_pos.append(str(len(el_pos)))

    with open(path_save,"w") as file:
        file.write(header+"\n")
        file.write("1\n")
        file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(a_latt[0], a_latt[1], a_latt[2]))
        file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(b_latt[0], b_latt[1], b_latt[2]))
        file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(c_latt[0], c_latt[1], c_latt[2]))
        file.write("    ".join(elements)+"\n")
        file.write("    ".join(len_pos)+"\n")
        file.write("Direct\n")
        for el_pos in at_pos:
            for pos in el_pos:
                file.write("{:6.4f}      {:6.4f}      {:6.4f}\n".format(pos[0],pos[1],pos[2]))

def main():
    path_xyz = "/home/lukas/documents/thesis/Structures/pmCrN.xyz"
    path_xyz = "/home/lukas/documents/thesis/Structures/afCrNTiN_110.xyz"

    dir_save = "/home/lukas/documents/thesis/Structures/CrNTin_cleaved/afCrNTiN_110/"
    filename = "CrNTiN_110"
    header = "af CrN TiN 110 interface"

    lattice_CrNTiN_110 =  [ [5.89584737116127,    0.00145103901071,    0.00000000000000],
                            [0.00474199711955,   17.88908655024918,    0.00000000000000],
                            [0.00000000000000,    0.00000000000000,    4.19716843678857]]
    cleave_axis = "b"
    cleave_x = 20  # length of the created gap (between 1 and number of planes)
    cleave_positions = [1,3,6,9,11]  # position of the gap
    cleave_positions = [6]

    for cleave_pos in cleave_positions:
        filename_full = filename + "_c{}.vasp".format((cleave_pos))
        path_save = os.path.join(dir_save, filename_full)
        cleave_cell(lattice_CrNTiN_110, cleave_axis, cleave_x,cleave_pos,path_xyz, path_save,header)

if __name__ == "__main__":
    main()

import os.path as path
import numpy as np

path_save = "/home/lukas/documents/thesis/Structures/"
filename = "CrN_TiN_1-10_16sheets"
struct_name = "TiN 1-10."
atom_spin1 = "Cr"
atom_spin2 = "Al"
atom_add = "N"
atom_metal = "Ti"
n_sheets = 8 # Number of planes. Has to be an even number.
cleave = 20 # Distance of the cleave in nm
cleave_pos = [18] # Number of plane after which the cell
                                       # is cleaved.

for cleave_index in cleave_pos:


    a = np.array([[3.55528], [0], [0]])
    b = np.array([[0], [3.85528], [0]])
    c = np.array([[0], [0], [4.25528]])
    # orthorombic lattice parameters
    a_orth = [np.linalg.norm(a + b), 0, 0]
    b_orth = [0, np.linalg.norm((a - b) / 2), 0]
    c_orth = [0, 0, c[2][0]]

    a_orth = [5.74, 0, 0]
    b_orth = [0, 2.8, 0]
    c_orth = [0, 0, 4.0588]


    x_m_a = np.array([[1],[1],[1],[1]])
    y_m_a = np.array([[0],[0],[1],[1]])
    z_m_a = np.array([[0],[1],[0],[1]])

    x_n_a = np.array([[1], [1]])
    y_n_a = np.array([[0], [1]])
    z_n_a = np.array([[0.5], [0.5]])

    x_m_b = np.array([[1]])
    y_m_b = np.array([[0.5]])
    z_m_b = np.array([[0.5]])

    x_n_b = np.array([[1], [1]])
    y_n_b = np.array([[0.5], [0.5]])
    z_n_b = np.array([[0], [1]])

    index = 1
    print(cleave_index)
    spin1 = True
    pos_sp_1 = []
    pos_sp_2 = []
    pos_met = []
    pos_add = []
    shift_tot = 0
    shift_half_plane = a_orth[0] / 4

    while index <= (n_sheets * 2):

        if index <= n_sheets:
            if spin1 == True:

                x = x_m_a * shift_tot
                pos_sp_1.extend(np.ndarray.tolist(np.concatenate((x,y_m_a,z_m_a)
                                                                 , 1)))
                x = x_n_a * shift_tot
                pos_add.extend(np.ndarray.tolist(np.concatenate((x,y_n_a,z_n_a)
                                                                 , 1)))
                if index == cleave_index:
                    shift_tot += cleave
                else:
                    shift_tot += shift_half_plane
                index += 1
                x = x_m_b * shift_tot
                pos_sp_2.extend(np.ndarray.tolist(np.concatenate((x,y_m_b,z_m_b)
                                                                 , 1)))
                x = x_n_b * shift_tot
                pos_add.extend(np.ndarray.tolist(np.concatenate((x, y_n_b, z_n_b),
                                                                1)))
                if index == cleave_index:
                    shift_tot += cleave
                else:
                    shift_tot += shift_half_plane
                index += 1

                spin1 = False

            else:
                x = x_m_a * shift_tot
                pos_sp_2.extend(
                    np.ndarray.tolist(np.concatenate((x, y_m_a, z_m_a)
                                                     , 1)))
                x = x_n_a * shift_tot
                pos_add.extend(
                    np.ndarray.tolist(np.concatenate((x, y_n_a, z_n_a)
                                                     , 1)))
                if index == cleave_index:
                    shift_tot += cleave
                else:
                    shift_tot += shift_half_plane
                index += 1
                x = x_m_b * shift_tot
                pos_sp_1.extend(
                    np.ndarray.tolist(np.concatenate((x, y_m_b, z_m_b)
                                                     , 1)))
                x = x_n_b * shift_tot
                pos_add.extend(
                    np.ndarray.tolist(np.concatenate((x, y_n_b, z_n_b),
                                                     1)))
                if index == cleave_index:
                    shift_tot += cleave
                else:
                    shift_tot += shift_half_plane
                index += 1

                spin1 = True

        else:
            x = x_m_a * shift_tot
            pos_met.extend(np.ndarray.tolist(np.concatenate((x, y_m_a, z_m_a)
                                                             , 1)))
            x = x_n_a * shift_tot
            pos_add.extend(np.ndarray.tolist(np.concatenate((x, y_n_a, z_n_a)
                                                            , 1)))
            if index == cleave_index:
                shift_tot += cleave
            else:
                shift_tot += shift_half_plane
            index += 1
            x = x_m_b * shift_tot
            pos_met.extend(np.ndarray.tolist(np.concatenate((x, y_m_b, z_m_b)
                                                             , 1)))
            x = x_n_b * shift_tot
            pos_add.extend(np.ndarray.tolist(np.concatenate((x, y_n_b, z_n_b),
                                                            1)))
            if index == cleave_index:
                shift_tot += cleave
            else:
                shift_tot += shift_half_plane
            index += 1


        #       if cleave_index > n_sheets*2:
#           shift_tot += cleave

    x = x_m_a * shift_tot
    pos_sp_1.extend(np.ndarray.tolist(np.concatenate((x, y_m_a, z_m_a)
                                                     , 1)))
    x = x_n_a * shift_tot
    pos_add.extend(np.ndarray.tolist(np.concatenate((x, y_n_a, z_n_a)
                                                    , 1)))


    i = 0
    while i in range(len(pos_sp_1)):
        pos_sp_1[i][0] /= shift_tot
        i += 1
    i = 0
    while i in range(len(pos_sp_2)):
        pos_sp_2[i][0] /= shift_tot
        i += 1
    i = 0
    while i in range(len(pos_met)):
        pos_met[i][0] /= shift_tot
        i += 1

    i = 0
    while i in range(len(pos_add)):
        pos_add[i][0] /= shift_tot
        i += 1

    a_orth = [shift_tot, 0, 0]
    with open(path.join(path_save, filename+"_clpos{}.vasp"
            .format(cleave_index)), "w") as poscar:
        poscar.write(struct_name + "\n")
        poscar.write("1\n")
        poscar.write(
            "{:6.4f} {:6.4f} {:6.4f}\n".format(a_orth[0], a_orth[1], a_orth[2]))
        poscar.write(
            "{:6.4f} {:6.4f} {:6.4f}\n".format(b_orth[0], b_orth[1], b_orth[2]))
        poscar.write(
            "{:6.4f} {:6.4f} {:6.4f}\n".format(c_orth[0], c_orth[1], c_orth[2]))
        poscar.write("{} {} {} {}\n".format(atom_spin1 , atom_spin2 ,
                                            atom_metal, atom_add))
        poscar.write(
            "{} {} {} {}\n".format(len(pos_sp_1), len(pos_sp_2), len(pos_met),
                                   len(pos_add)))
        poscar.write("Direct\n")
        for pos in pos_sp_1:
            poscar.write("{:6.4f} {:6.4f} {:6.4f} ## up\n".format(pos[0], pos[1]
                                                                  , pos[2]))

        for pos in pos_sp_2:
            poscar.write("{:6.4f} {:6.4f} {:6.4f} ## down\n".format(pos[0],
                                                                pos[1], pos[2]))

        for pos in pos_met:
            poscar.write("{:6.4f} {:6.4f} {:6.4f} ## met\n".format(pos[0],
                                                                pos[1], pos[2]))

        for pos in pos_add:
            poscar.write("{:6.4f} {:6.4f} {:6.4f} ## add\n".format(pos[0],
                                                                pos[1], pos[2]))

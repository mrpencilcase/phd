import os.path as path
import numpy as np

path_save = "/home/lukas/documents/thesis/Structures/"
filename = "TEST"
struct_name = "CrN a.f."
atom_spin1 = "Cr"
atom_spin2 = "O"
atom_add = "N"
atom_metal = "Ti"
n_sheets = 6 # Number of planes. Has to be an even number.




a = np.array([[4.238], [0], [0]])
b = np.array([[0], [4.238], [0]])
c = np.array([[0], [0], [4.238]])
# orthorombic lattice parameters
a_orth = [np.linalg.norm(a + b), 0, 0]
b_orth = [0, np.linalg.norm((a - b) / 2), 0]
c_orth = [0, 0, c[2][0]]

a_orth = [5.74049, 0, 0]
b_orth = [0, 2.87044, 0]
c_orth = [0, 0, 4.05886]

x_m_a_1 = np.array([[0],[0],[1],[1]])
y_m_a_1 = np.array([[0],[1],[0],[1]])
z_m_a_1 = np.array([[1],[1],[1],[1]])

x_m_a_2 = np.array([[0.5], [0.5]])
y_m_a_2 = np.array([[0], [1]])
z_m_a_2 = np.array([[1], [1]])

x_n_a = np.array([[0.25], [0.75]])
y_n_a = np.array([[0.5], [0.5]])
z_n_a = np.array([[1], [1]])

x_m_b_1 = np.array([[0.75]])
y_m_b_1 = np.array([[0.5]])
z_m_b_1 = np.array([[1]])

x_m_b_2 = np.array([[0.25]])
y_m_b_2 = np.array([[0.5]])
z_m_b_2 = np.array([[1]])

x_n_b = np.array([[0], [0], [1], [1], [0.5],[0.5]])
y_n_b = np.array([[0], [1], [0], [1],[0],[1]])
z_n_b = np.array([[1], [1], [1], [1],[1],[1]])

index = 1

pos_sp_1 = []
pos_sp_2 = []
pos_met = []
pos_add = []
shift_tot = 0
shift_half_plane = c_orth[2] / 2

while index <= (n_sheets * 2):

    if index <= n_sheets:
        z = z_m_a_1 * shift_tot
        pos_sp_1.extend(np.ndarray.tolist(np.concatenate((x_m_a_1,y_m_a_1,z)
                                                       , 1)))

        z = z_m_a_2 * shift_tot
        pos_sp_2.extend(np.ndarray.tolist(np.concatenate((x_m_a_2,y_m_a_2,z)
                                                         , 1)))
        z = z_n_a * shift_tot
        pos_add.extend(np.ndarray.tolist(np.concatenate((x_n_a, y_n_a, z),
                                                        1)))

        shift_tot += shift_half_plane


        z = z_m_b_1 * shift_tot
        pos_sp_1.extend(np.ndarray.tolist(np.concatenate((x_m_b_1,y_m_b_1,z)
                                                         , 1)))
        z = z_m_b_2 * shift_tot
        pos_sp_2.extend(np.ndarray.tolist(np.concatenate((x_m_b_2,y_m_b_2,z)
                                                         , 1)))
        z = z_n_b * shift_tot
        pos_add.extend(np.ndarray.tolist(np.concatenate((x_n_b, y_n_b, z),
                                                        1)))
        shift_tot += shift_half_plane
        index += 2

    else:

        z = z_m_a_1 * shift_tot
        pos_met.extend(np.ndarray.tolist(np.concatenate((x_m_a_1,y_m_a_1,z)
                                                         , 1)))
        z = z_m_a_2 * shift_tot
        pos_met.extend(np.ndarray.tolist(np.concatenate((x_m_a_2,y_m_a_2,z)
                                                         , 1)))
        z = z_n_a * shift_tot
        pos_add.extend(np.ndarray.tolist(np.concatenate((x_n_a, y_n_a, z),
                                                        1)))
        shift_tot += shift_half_plane
        index += 1

        z = z_m_b_1 * shift_tot
        pos_met.extend(np.ndarray.tolist(np.concatenate((x_m_b_1,y_m_b_1,z)
                                                         , 1)))
        z = z_m_b_2 * shift_tot
        pos_met.extend(np.ndarray.tolist(np.concatenate((x_m_b_2,y_m_b_1,z)
                                                         , 1)))
        z = z_n_b * shift_tot
        pos_add.extend(np.ndarray.tolist(np.concatenate((x_n_b, y_n_b, z),
                                                        1)))

        shift_tot += shift_half_plane
        index += 1

#       if cleave_index > n_sheets*2:
#           shift_tot += cleave

z = z_m_a_1 * shift_tot
pos_sp_1.extend(np.ndarray.tolist(np.concatenate((x_m_a_1, y_m_a_1, z)
                                                 , 1)))
z = z_m_a_2 * shift_tot
pos_sp_2.extend(np.ndarray.tolist(np.concatenate((x_m_a_2, y_m_a_2, z)
                                                 , 1)))
z = z_n_a * shift_tot
pos_add.extend(np.ndarray.tolist(np.concatenate((x_n_a, y_n_a, z),
                                                1)))
print(shift_tot)
i = 0
while i in range(len(pos_sp_1)):
    pos_sp_1[i][2] /= shift_tot
    i += 1
i = 0
while i in range(len(pos_sp_2)):
    pos_sp_2[i][2] /= shift_tot
    i += 1
i = 0
while i in range(len(pos_met)):
    pos_met[i][2] /= shift_tot
    i += 1

i = 0
while i in range(len(pos_add)):
    pos_add[i][2] /= shift_tot
    i += 1

c_orth = [0, 0, shift_tot]
with open(path.join(path_save, filename+".vasp"), "w") as poscar:
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

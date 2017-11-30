import os.path as path
import numpy as np

path_save = "/home/lukas/Documents/thesis/"
filename = "test.vasp"
struct_name = "CrN a.f."
atom_spin = "Cr"
atom_add = "N"

a = np.array([[4.32],[0],[0]])
b = np.array([[0],[4.32],[0]])
c = np.array([[0],[0],[4.32]])

# orthorombic lattice parameters
a_orth = [np.linalg.norm(a+b),0,0]
b_orth = [0,np.linalg.norm((a-b)/2),0]
c_orth = np.ndarray.tolist(c)

pos_up_rel = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                   [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1],
                   [0.75, 0.5, 0.5]]
pos_down_rel =[[0.5, 0, 0], [0.5, 0, 1], [0.5, 1, 0], [0.5, 1, 1],
                    [0.25, 0.5, 0.5]]

pos_non_rel = [[0, 0, 0.5], [0, 1, 0.5],
               [0.25, 0.5, 0], [0.25, 0.5, 1],
               [0.5, 1, 0.5], [0.5, 1, 0.5],
               [0.75, 0.5, 0],[0.75, 0.5, 1],
               [1, 0, 0.5], [1, 1, 0.5]]

print(a_orth)
with open(path.join(path_save,filename),"w") as outcar:
    outcar.write(struct_name+"\n")
    outcar.write("1\n")
    outcar.write("{:6.4f} {:6.4f} {:6.4f}\n".format(a_orth[0],a_orth[1],a_orth[2]))
    outcar.write("{:6.4f} {:6.4f} {:6.4f}\n".format(b_orth[0],b_orth[1],b_orth[2]))
    outcar.write("{:6.4f} {:6.4f} {:6.4f}\n".format(c_orth[0][0],c_orth[1][0],c_orth[2][0]))
    outcar.write("{} {} {}\n".format(atom_spin +"_up",atom_spin+"_down",atom_add))
    outcar.write("{} {} {}\n".format(len(pos_up_rel),len(pos_down_rel),len(pos_non_rel)))
    outcar.write("Direct\n")
    for pos in pos_up_rel:
        outcar.write("{:6.4f} {:6.4f} {:6.4f}\n".format(pos[0], pos[1], pos[2]))

    for pos in pos_down_rel:
        outcar.write("{:6.4f} {:6.4f} {:6.4f}\n".format(pos[0], pos[1], pos[2]))

    for pos in pos_non_rel:
        outcar.write("{:6.4f} {:6.4f} {:6.4f}\n".format(pos[0], pos[1], pos[2]))



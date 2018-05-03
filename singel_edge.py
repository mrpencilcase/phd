import numpy as np
import md_functions as md_f
import time
from os.path import join
#-------------------------------------------------------------------------
# read and analyze the

path_lmp = "/home/lukas/Documents/work/md/TiN/dislocation/singel_edge/singel_edge.lmp"
path_in = "/home/lukas/Documents/work/md/TiN/dislocation/singel_edge/"
with open(path_lmp,"r") as file:
    struct = list(file)
# Box parameters
x = [float(struct[5].split()[0]), float(struct[5].split()[1])]
y = [float(struct[6].split()[0]), float(struct[6].split()[1])]
z = [float(struct[7].split()[0]), float(struct[7].split()[1])]

at_pos_3d = []
border_thickness = 10
direction = "z"
plane_pos = 0


for i in range(11,len(struct)-1):
    line = [float(ent) for ent in struct[i].split()]
#    print(struct[i])
    at_pos_3d.append([line[2], line[3], line[4]])

at_pos_2d = []
x_mid = (x[1]-x[0])/2
y_mid = (y[1]-y[0])/2
z_mid = (z[1]-z[0])/2

if direction == "z":
    for pos in  at_pos_3d:
        if pos[2] == plane_pos:
            at_pos_2d.append([pos[0], pos[1]])
    pos1 = x_mid
    pos2 = y_mid

if direction == "y":
    for pos in  at_pos_3d:
        if pos[1] == plane_pos:
            at_pos_2d.append([pos[0], pos[2]])
    pos1 = x_mid
    pos2 = z_mid

if direction == "x":
    for pos in  at_pos_3d:
        if pos[0] == plane_pos:
            at_pos_2d.append([pos[1],pos[2]])
    pos1 = z_mid
    pos2 = y_mid

radius=(md_f.find_largest_dist_con(at_pos_2d))/2 - border_thickness
print(radius)

with open(join(path_in,"singel_edge_base.in"),"r") as file:
    script = list(file)

#line to fix boarder of circle
def_border = "region border cylinder {} {:6.3f} {:6.3f} {:6.3f} EDGE EDGE side out \n".format(
    direction, pos1, pos2, radius)
script = md_f.insert_line(def_border, '#border region', script)


def_inner = "region inner cylinder {} {:6.3f} {:6.3f} {:6.3f} EDGE EDGE side in \n".format(
    direction, pos1, pos2, radius, script)
script = md_f.insert_line(def_inner, '#inner region', script)

with open(join(path_in,"singel_edge.in"),"w") as file:
    for line in script:
        file.write(line)



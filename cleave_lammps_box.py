from os.path import join

path_open = "/home/lukas/Documents/work/md/TiN/surface energy/"
file_open = "bulk.lmp"

path_save = path_open
file_save = "box_gap.lmp"

gap = 20
with open(join(path_open,file_open),"r") as file:
    box = list(file)
print(box[7])
z_coord = [str(ent) for ent in box[7].split()]
z_max_old = float(z_coord[1])
z_max_new = float(z_coord[1])+gap
z_coord[1] = str(z_max_new)
box_half = z_max_old * 0.5
at_coord = []

box[7] = "{:16.8f} {:16.8f}  {} {}\n".format(float(z_coord[0]), float(z_coord[1]),
                                                z_coord[2], z_coord[3])


for i in range(11,len(box)-1):
    line = [float(ent) for ent in box[i].split()]
    if line[4] >= box_half:
        box[i] = "{:10d}{:5d}{:18.8f}{:16.8f}{:16.8f}\n".format(int(line[0]), int(line[1]),
                                                line[2], line[3], line[4]+gap)

with open(join(path_save,file_save),"w") as file:
    for line in box:
        file.write(line)


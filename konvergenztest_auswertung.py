import os
import matplotlib.pyplot as plt
import numpy as np

path_dir = "/home/lukas/Documents/thesis/result_vasp/TiN/TiN"
path_dir = "/home/lukas/Documents/thesis/result_vasp/CrN_af/CrN/"


plot_title = "anti ferro mag CrN"

path_list = [os.path.join(path_dir,sub) for sub in os.listdir(path_dir) if
             os.path.isdir(os.path.join(path_dir,sub))]

data = []

for case in path_list:
    data_singel = [0,0,"none"]

    with open(os.path.join(case,"INCAR"),"r") as file:
        incar = list(file)
        for line in incar:
            if "ENCUT" in line:
                data_singel[0]=int(line.split()[2])

    with open(os.path.join(case,"KPOINTS"),"r") as file:
        data_singel[1] = int(list(file)[3])

    if os.path.exists(os.path.join(case,"OUTCAR")):
        with open(os.path.join(case,"OUTCAR"),"r") as file:
            outcar = list(file)
            for index, line in reversed(list(enumerate(outcar))):
                if "FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)" in line:
                    data_singel[2] = float(outcar[index+2].split()[4])

    data.append(data_singel)

data = sorted(data, key = lambda x : (x[0],x[1]))
data_split = []
dummy = []
index = 1
dummy.append(data[0])
while index in range(len(data)):
    if data[index][0] != dummy[-1][0]:
        data_split.append(dummy)
        dummy = []
        dummy.append(data[index])
        index += 1
    else:
        dummy.append(data[index])
        index += 1

data_split.append(dummy)
e_min = 400
e_max = 900

k_min = 30
k_max = 100

print("Plot")
linestyles = ["-","--","-.",""]
color = ["black","gray"]
fig, ax = plt.subplots()
for ent in data_split:

    if e_min <= ent[0][0] <= e_max:
        x = []
        y = []
        print(ent)
        for point in ent:
            if point[2] != "none" and k_min <= point[1] <= k_max:
                x.append(point[1])
                y.append(np.around(point[2]/4,3))
                label = "E Cutoff: "+str(point[0])

        ax.errorbar(x,y,yerr=0.001,capsize=2,
                     linewidth=1.0,label = label + " eV",marker ="+")
ax.set_xlabel("Number of k-points")
ax.set_ylabel("Ground State Energy [eV/at.]")
ax.legend()
ax.set_title(plot_title)
fig.savefig(os.path.join(path_dir,plot_title)+".pdf")
plt.show()
print("done")
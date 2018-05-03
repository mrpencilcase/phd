import numpy as np
from os import path
import matplotlib.pyplot as plt
import os

def read_lammps(data_struct,fixed,inspect,path, file,chunk_size):
    key_phrase = data_struct

    path_open = os.path.join(path,file)

    #path_open = "/home/lukas/Documents/thesis/lammps/whathappens/log.lammps"

    elements = [ent for ent in key_phrase.split()]
    keep_range = 100 #Value from which on the data is kept for statistical analysis
    step_number = []
    fixed_var = fixed
    inspect_var = inspect
    lammps_data = []

    fixed_index = elements.index(fixed_var)
    inspect_index =elements.index(inspect_var)
    step_index = elements.index("Step")
    with open(path_open,"r") as file:
        data = list(file)


    for i in range(len(data)):
        if key_phrase in data[i]:
            i += 1
            while i > -1:
                if "Loop time of" in data[i]:
                    break

                line = data[i].rstrip()
                lammps_data.append([float(ent) for ent in line.split()])
                i += 1
        i += 1
    lammps_data = np.asarray(lammps_data,dtype=np.float32)

    fixed_data = np.delete(lammps_data[:,fixed_index],np.s_[0:keep_range])

    inspect_data = np.delete(lammps_data[:,inspect_index],np.s_[0:keep_range])

    step_number = np.delete(lammps_data[:,step_index],np.s_[0:keep_range])


    inspect_chunks = np.array_split(inspect_data,int(len(inspect_data)/chunk_size))
    fixed_chunks = np.array_split(fixed_data,int(len(fixed_data)/chunk_size))

    inspect_mean, inspect_median, inspect_std = get_statistics(inspect_data)
    fixed_mean, fixed_median, fixed_std = get_statistics(fixed_data)

    inspect_chunks_mean = []
    inspect_chunks_median = []
    inspect_chunks_std = []
    for chunk in inspect_chunks:
        mean, median, std = get_statistics(chunk)
        inspect_chunks_mean.append(mean)
        inspect_chunks_median.append(median)
        inspect_chunks_std.append(std)

    fixed_chunks_mean = []
    fixed_chunks_median = []
    fixed_chunks_std = []
    for chunk in fixed_chunks:
        mean, median, std = get_statistics(chunk)
        fixed_chunks_mean.append(mean)
        fixed_chunks_median.append(median)
        fixed_chunks_std.append(std)

    #Output
    print("Statistics (whole set):")
    print("Mean ({})  : {}".format(inspect_var,inspect_mean))
    print("Median ({}): {}".format(inspect_var,inspect_median))
    print("STD ({})   : {}".format(inspect_var,inspect_std))
    print("")
    print("Mean ({})  : {}".format(fixed_var, fixed_mean))
    print("Median ({}): {}".format(fixed_var, fixed_median))
    print("STD ({})   : {}".format(fixed_var, fixed_std))
    print("")
    print("")
    # print("Statistics (chunks with size n={}):".format(chunk_size))
    # print("Mean ({})  :".format(inspect_var))
    # print(inspect_chunks_mean)
    # print("Median ({})  :".format(inspect_var))
    # print(inspect_chunks_median)
    # print("STD ({})  :".format(inspect_var))
    # print(inspect_chunks_std)
    # print("Mean ({})  :".format(fixed_var))
    # print(fixed_chunks_mean)
    # print("Median ({})  :".format(fixed_var))
    # print(fixed_chunks_median)
    # print("STD ({})  :".format(fixed_var))
    # print(fixed_chunks_std)

    #Plot
    plot = True
    if plot == True:
        linewidth = 1
        fig = plt.figure()


        ax1=fig.add_subplot(221)
        ax1.plot(step_number,fixed_data,"-b",lw=linewidth)

        ax1.set_xlabel("Step Number")
        ax1.set_ylabel("Temperature (K)")

        ax2=fig.add_subplot(222)
        ax2.plot(step_number,inspect_data,"-r",lw=linewidth)
        ax2.set_xlabel("Step Number")
        ax2.set_ylabel(r" Ground State Energy ($eV$)")

        ax3=fig.add_subplot(223)
        ax3.plot(fixed_chunks_mean,"-b",lw=linewidth)
        ax3.set_xlabel("Chunk number")
        ax3.set_ylabel("Mean Temperature (K)")

        ax4=fig.add_subplot(224)
        ax4.plot(inspect_chunks_mean,"-r",lw=linewidth)
        plt.suptitle("Relexation of TiN at {}K".format(np.around(fixed_mean)))
        ax4.set_ylabel(r"Ground State Energy($eV$)")
        ax4.set_xlabel("Chunk number")
        plt.show()
    #    plt.savefig(os.path.join(path,"energy.pdf"))


def get_statistics(data):
    mean = np.mean(data)
    median = np.median(data)
    std = np.std(data)
    return mean, median, std


def main():

    path = "/home/lukas/Documents/work/md/TiN/surface energy/100/"
    files = ["base/log.lammps","cleaved/log.lammps"]
    key_phrase = "Step Time Temp Volume TotEng PotEng KinEng Enthalpy Pxx Pyy Pzz"
    for file in files:
        read_lammps(key_phrase,"Temp","TotEng",path, file,10)




if __name__ =="__main__":
    main()
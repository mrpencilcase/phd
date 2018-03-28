import numpy as np
import matplotlib.pyplot as plt
import  read_outcar

def main():
    path_open = "/home/lukas/Documents/thesis/result_vasp/vsc3/CrN_TiN/relax/relax_af_CrN_TiN_1-10/OUTCAR"
   # plot_energy(path_open)
    plot_force(path_open,4,"x")

def plot_energy(path_open):
    """
    :param path_open: path to the OUTCAR file
    :return:
    """

    print("reading data")
    free_energy = read_outcar.read_tot_en(path_open,"all")
    print("ploting")
    lw = 1
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(free_energy,"-k",linewidth = lw)
    ax.set_xlabel("Step")
    ax.set_ylabel(r"Free Total Energy (eV)")
    plt.show()


def plot_force(path_open,n_atom,axis):
    """
    :param path_open: path to the OUTCAR file
    :param n_atom: number of the atom of interest
    :param axis: axis in which the force is directed
    :return:
    """

    if axis == "x":
        n_axis = 0

    elif axis == "y":
        n_axis = 1

    elif axis == "z":
        n_axis = 2
    else:
        print("wrong axis")


    print("reading data")
    forces = read_outcar.read_forces(path_open)
    fxn = []
    for steps in forces:
        fxn.append(steps[n_axis][n_atom-1])

    lw = 1
    border_up = [0.01]*len(fxn)
    border_down = [-0.01]*len(fxn)
    x = np.arange(0,len(fxn),1)
    print("ploting")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Forces on Atom #{} in {} direction".format(n_atom,axis))
    ax.plot(border_up,linewidth = lw,color="grey")
    ax.plot(border_down,linewidth = lw,color="grey")
    ax.fill_between(x,border_down,border_up,facecolors="silver",alpha=0.4)
    ax.plot(fxn,"-k",linewidth = lw)
    ax.set_xlabel("Step")
    ax.set_ylabel(r"Force (eV/$\AA$)")
    plt.show()

if __name__ == "__main__":
    main()
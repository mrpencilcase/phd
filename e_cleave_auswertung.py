"""
script to analyze the cleave energy from calculations
calculate the critical length and the E_cleave for the given planes
from the OUTCAR results.
"""
from os.path import isdir,join
from os import listdir
import numpy as np
from read_outcar import read_tot_en
from read_poscar import read_poscar
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def main():
    mat = "CrN_TiN"
    path_parent_open = "/home/lukas/documents/thesis/result_vasp/cleave/TiN/12sheets/1/"
    path_poscar_rel = ""
    sub_folders = [f for f in listdir(path_parent_open) if
     isdir(join(path_parent_open, f))]
    n_at = 1
    e_x = []
    x_c = []
    cell_relaxed = read_poscar(join(path_parent_open,"CONTCAR"),mat)
    area = cell_relaxed.lattice.b[1] * cell_relaxed.lattice.c[2]

    for folder in sub_folders:
        path = join(path_parent_open,folder)
        tot_en = read_tot_en(join(path,"OUTCAR"),"last")
        cell_new = read_poscar(join(path,"POSCAR"),mat)

        x_c.append(cell_new.lattice.a[0]-cell_relaxed.lattice.a[0])
        e_x.append(tot_en[0]/n_at)
        #print(tot_en)

    pop_int = []
    for i in range(len(e_x)):
        if not e_x[i]:
            pop_int.append(i)

    pop_int.reverse()

    for ent in pop_int:
        e_x.pop(ent)
        x_c.pop(ent)




    e_x.sort(key=dict(zip(e_x, x_c)).get)
    x_c.sort()

    with open(join(path_parent_open,"e_cleave.dat"),"w") as file:
        file.write("d cleave       E total\n")
        for x,e in zip(x_c,e_x):
            file.write("{:8.3f}      {:8.3f}\n".format(x,e))


    e_x = [(ent - e_x[0])/area for ent in e_x]


    fit = curve_fit(E_x, x_c, e_x)
    e_c_fit = fit[0][0]
    l_fit = fit[0][1]
    x_plt = np.linspace(0,max(x_c),100)
    e_x_plt = E_x(x_plt,e_c_fit,l_fit)





    plt.plot(x_c,e_x,"ob")
    plt.plot(x_plt,e_x_plt,"-k")
    plt.title(r"12 sheets")
    plt.xlabel(r"x [$\AA$]")
    plt.ylabel(r"Ground State Energy [eV/at.]")
    plt.show()
    print(fit)



def E_x(x,E_c,l):
    return E_c*(1-(1+x/l)*np.exp(-x/l))



if __name__ =="__main__":
    main()
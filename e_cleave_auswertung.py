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
def main():
    mat = "CrN_TiN"
    path_parent_open = "/home/lukas/documents/thesis/result_vasp/cleave/afCrN_TiN_1-10/distance_variation/7/"
    path_poscar_rel = ""
    sub_folders = [f for f in listdir(path_parent_open) if
     isdir(join(path_parent_open, f))]

    e_x = []
    x = []
    cell_relaxed = read_poscar(join(path_parent_open,"CONTCAR"),mat)
    for folder in sub_folders:
        path = join(path_parent_open,folder)
        tot_en = read_tot_en(join(path,"OUTCAR"),"first")
        cell_new = read_poscar(join(path,"POSCAR"),mat)

        x.append(cell_new.lattice.a[0]-cell_relaxed.lattice.a[0])
        e_x.append(tot_en)
        #print(tot_en)

    print(x)
    print(e_x)

def E_x(E_c,x,l):
    return E_c*(1-(1+x/l)*np.exp(-x/l))






if __name__ =="__main__":
    main()
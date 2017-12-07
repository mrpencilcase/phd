"""
script to analyze the cleave energy from calculations
calculate the critical length and the E_cleave for the given planes
from the OUTCAR results.
"""
from os.path import isdir,join
from os import listdir
import numpy as np
from read_outcar import read_tot_en

def main():
    path_parent_open = "/home/lukas/documents/thesis/result_vasp/cleave/afCrN_TiN_1-10/distance_variation/7/"
    path_poscar_rel = ""
    sub_folders = [f for f in listdir(path_parent_open) if
     isdir(join(path_parent_open, f))]

    for folder in sub_folders:
        path = join(path_parent_open,folder)
        path = join(path,"OUTCAR")
        tot_en = read_tot_en(path,"first")
        print(tot_en)


if __name__ =="__main__":
    main()
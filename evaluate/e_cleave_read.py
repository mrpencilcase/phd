"""
Script to read the energies and distantces of cleave calculations in the given
folder. Creates file with the distances the total energies and the relative energies
per area
"""
from os.path import isdir,join
from os import listdir
from read_outcar import read_tot_en
from read_poscar import read_poscar

def main():
    mat = "CrN_TiN"
    path_parent_open = "/home/lukas/Documents/work/dft/vasp_results/CrN_TiN/cleave/001/a1452" \
                       "f/plane_5/"
    path_poscar_rel = ""
    sub_folders = [f for f in listdir(path_parent_open) if
     isdir(join(path_parent_open, f))]
    n_at = 1
    e_x = []
    x_c = []
    cell_relaxed = read_poscar(join(path_parent_open,"POSCAR"),mat)
    area = cell_relaxed.lattice.b[1] * cell_relaxed.lattice.a[0]
    print("unsorted")
    for folder in sub_folders:
        path = join(path_parent_open,folder)
        tot_en = read_tot_en(join(path,"OUTCAR"),"last")
        cell_new = read_poscar(join(path,"POSCAR"),mat)
        if tot_en:
            x_c.append(cell_new.lattice.c[2]-cell_relaxed.lattice.c[2])
            e_x.append(tot_en[0]/n_at)

            print("{}   {}".format(tot_en[0] / n_at,cell_new.lattice.c[2] - cell_relaxed.lattice.c[2]))
    e_x.sort(key=dict(zip(e_x, x_c)).get)
    x_c.sort()

    e_x_a = [(ent - e_x[0])/area for ent in e_x]

    print("sorted")
    for e, x in zip(e_x,x_c):
        print("{}   {}".format(e,x))

    # x_c.sort(key=dict(zip(x_c, e_x)).get)
    # e_x.sort()
    # print("sorted")
    # for e, x in zip(e_x,x_c):
    #     print("{}   {}".format(e,x))

    with open(join(path_parent_open,"e_cleave.dat"),"w") as file:
        file.write("# d cleave       E total        E_diff\n")
        for x,e,ea in zip(x_c,e_x,e_x_a):
            file.write("  {:8.3f}      {:8.3f}        {:8.3f}\n".format(x,e,ea))

if __name__ =="__main__":
    main()
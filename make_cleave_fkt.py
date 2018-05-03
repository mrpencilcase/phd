"""
Skript to make cleave calculations from an relaxed OUTCAR and POSCAR file
Checks if the realxed cell has any moments and if yes transfers them to the
new calculation as starting moments
"""
from os.path import join
from itertools import repeat
import file_functions as ff
import read_outcar as ro

def make_cleave_calc(path_base, cleave_planes, cleave_dist, cleave_direction):
    # check the OUTACR for magnetic moments
    spins = ro.get_spins(join(path_base,"OUTCAR_relaxed"))
    if not spins:
        magnetic = False
    else:
        magnetic = True
    print("Magnetic: {}".format(magnetic))
    # Create calculations without modification
    if not magnetic:
        ff.create_potcar(path_base,"POSCAR_relaxed")

    if magnetic:
        moments = ro.get_spins(join(path_base,"OUTCAR_relaxed"))[-1]
        poscar = ff.read_file(join(path_base,"POSCAR_relaxed"),"POSCAR")
        specis = [ent for ent in poscar.data[5].split()]
        amount = [float(ent) for ent in poscar.data[6].split()]
        # Create lines for POSCAR and INCAR and file list for POTCAR
        i = 0
        ind_ele = []
        potcar_filelist = []
        for ele, num in zip(specis, amount):
            ind_ele.extend(repeat(ele,int(num)))
            potcar_filelist.extend(repeat(join(path_base,"POTCAR_"+ele),int(num)))


        moment_line = ""
        for ent in moments:
            moment_line = moment_line + " 1*" + str(ent)

        #POTCAR
        ff.contegate_files(potcar_filelist,join(path_base,"POTCAR"))
        # POSCAR
        ind_am = ["1"] * len(ind_ele)
     #   c = ', '.join('{}={}'.format(*t) for t in zip(a, b))
        poscar.data[5] = " ".join("{:3s}".format(t) for t in ind_ele) + "\n"
        poscar.data[6] = " ".join("{:3s}".format(t) for t in ind_am) + "\n"
        with open(join(path_base,"POSCAR"),"w") as file:
            for line in poscar.data:
                file.write(line)

        #INCAR
        ff.modifiy_incar(path_base,"MAGMOM",moment_line)
        ff.modifiy_incar(path_base,"LORBIT","11")
        ff.modifiy_incar(path_base,"ISPIN","2")

    # Create the individuall calcultions from the created input files

    incar = ff.read_file(join(path_base,"INCAR"),"INCAR")
    potcar = ff.read_file(join(path_base,"POTCAR"),"POTCAR")
    kpoints = ff.read_file(join(path_base,"KPOINTS"),"KPOINTS")
    run = ff.read_file(join(path_base,"check.slrm"),"check.slrm")

    for plane in cleave_planes:

        # make directory
        name_dir_plane = "plane_{}".format(plane)
        path_dir_plane = join(path_base,name_dir_plane)
        submit_data = []

        if not ff.exists(path_dir_plane):
            ff.makedirs(path_dir_plane)

        # create folder for each distance with the right files in it
        for dist in cleave_dist:
            poscar = ff.File("POSCAR","",ff.cleave_cell(cleave_direction,
                                                    dist,plane,
                                                    join(path_base,"POSCAR")))
            print(poscar.data[0])
            name_dir_cleave = "d_cleave_{}".format(dist)
            path_dir_cleave = join(path_dir_plane,name_dir_cleave)
            ff.create_singel_calc(path_dir_cleave,
                                  poscar,incar,potcar,kpoints,run)

            submit_data.append(name_dir_cleave)

        # create submission file for the plane
        with open(join(path_dir_plane,"job_sub.sh"),"w") as file:
            for ent in submit_data:
                file.write("cd {}\n".format(ent))
                file.write("sbatch check.slrm\n")
                file.write("cd ..\n")

    return

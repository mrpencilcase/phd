"""
script that creates folders for a series of calculations
creates subfolders within the given folder and copies present in this parent
folder into the subfolders.
The files that are different for the differnt calculations have to be in another
folder.
"""
import file_functions as ff
import read_outcar as ro
from cleave_from_poscar import cleave_cell
from os.path import join

path_parent_folder = "/home/lukas/Documents/thesis/upload/vsc3/CrN_TiN/cleave/1-10/"
path_incar = join(path_parent_folder,"INCAR")
path_poscar = join(path_parent_folder,"POSCAR")
path_potcar = join(path_parent_folder,"POTCAR")
path_kpoints = join(path_parent_folder,"KPOINTS")
path_sub = join(path_parent_folder,"check.slrm")
cleave_planes = [4, 5, 6, 7, 8]
cleave_dist =[ 0.1 ,0.15, 0.2, 0.25, 0.3 , 0.4, 0.5,  0.8, 1, 1.5, 2, 2.5, 3, 4, 5, 7]
cleave_axis = "a"

incar = ff.read_file(path_incar,"INCAR")
potcar = ff.read_file(path_potcar,"POTCAR")
kpoints = ff.read_file(path_kpoints,"KPOINTS")
run = ff.read_file(path_sub,"check.slrm")

# loop over the individual planes that are cleaved
for plane in cleave_planes:

    # make directory
    name_dir_plane = "plane_{}".format(plane)
    path_dir_plane = join(path_parent_folder,name_dir_plane)
    submit_data = []

    if not ff.exists(path_dir_plane):
        ff.makedirs(path_dir_plane)

    # create folder for each distance with the right files in it
    for dist in cleave_dist:
        poscar = ff.File("POSCAR","",cleave_cell(cleave_axis,dist,plane,path_poscar))
        print(poscar.data[0])
        name_dir_cleave = "d_cleave_{}".format(dist)
        path_dir_cleave = join(path_dir_plane,name_dir_cleave)
        ff.create_singel_calc(path_dir_cleave,
                              poscar,incar,potcar,kpoints,run)
        # Create the magnetic configuration as
        mag_mom = ro.get_spins(path_out)
        spins = mag_mom[-1]
        mag_line = "1*".join(spins+" ")

        submit_data.append(name_dir_cleave)

    # create submission file for the plane
    with open(join(path_dir_plane,"job_sub.sh"),"w") as file:
        for ent in submit_data:
            file.write("cd {}\n".format(ent))
            file.write("sbatch check.slrm\n")
            file.write("cd ..\n")

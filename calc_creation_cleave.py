"""
script that creates folders for a series of calculations
creates subfolders within the given folder and copies present in this parent
folder into the subfolders.
The files that are different for the differnt calculations have to be in another
folder.
"""
import file_functions as ff
from cleave_from_poscar import cleave_cell
from os.path import join

path_parent_folder = "/home/lukas/documents/thesis/upload/cleave/afCrN_TiN_1-10/"
path_incar = join(path_parent_folder,"INCAR")
path_poscar = join(path_parent_folder,"POSCAR")
path_potcar = join(path_parent_folder,"POTCAR")
path_kpoints = join(path_parent_folder,"KPOINTS")
path_sub = join(path_parent_folder,"job_run.sh")
cleave_planes = [5, 6, 7]
cleave_dist =[ 0.05, 0.1 ,0.15, 0.2, 0.25, 0.3 ,0.35, 0.4, 0.5, 0.6, 0.8, 1, 1.5, 2, 2.5, 3, 4, 5]
cleave_axis = "a"

incar = ff.read_file(path_incar,"INCAR")
potcar = ff.read_file(path_potcar,"POTCAR")
kpoints = ff.read_file(path_kpoints,"KPOINTS")
run = ff.read_file(path_sub,"job_run.sh")

for plane in cleave_planes:

    name_dir_plane = "plane_{}".format(plane)
    path_dir_plane = join(path_parent_folder,name_dir_plane)
    submit_data = []

    if not ff.exists(path_dir_plane):
        ff.makedirs(path_dir_plane)

    for dist in cleave_dist:
        poscar = ff.File("POSCAR","",cleave_cell(cleave_axis,dist,plane,path_poscar))
        print(poscar.data[0])
        name_dir_cleave = "d_cleave_{}".format(dist)
        path_dir_cleave = join(path_dir_plane,name_dir_cleave)
        ff.create_singel_calc(path_dir_cleave,
                              poscar,incar,potcar,kpoints,run)
        submit_data.append(name_dir_cleave)

    with open(join(path_dir_plane,"job_sub.sh"),"w") as file:
        for ent in submit_data:
            file.write("cd {}\n".format(ent))
            file.write("qsub job_run.sh\n")
            file.write("cd ..\n")

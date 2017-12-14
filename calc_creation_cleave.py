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

path_parent_folder = "/home/lukas/documents/thesis/upload/cleave/TiN/16sheets/"
path_incar = ""
path_poscar = ""
path_potcar = ""
path_kpoints = ""
path_sub = ""
cleave_planes = []
cleave_dist = []
cleave_axis = "a"

incar = ff.read_file(path_incar,"INCAR")
potcar = ff.read_file(path_potcar,"POTCAR")
kpoints = ff.read_file(path_kpoints,"KPOINTS")
submit = ff.read_file((path_sub,"job_sub.sh"))

for plane in cleave_planes:
    for dist in cleave_dist:
        poscar = cleave_cell(cleave_axis,dist,plane,path_poscar)
    path_dir = join(path_parent_folder,plane,dist)
    ff.create_singel_calc(path_dir,poscar,incar,potcar,kpoints,submit)


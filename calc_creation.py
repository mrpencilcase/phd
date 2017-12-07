"""
script that creates folders for a series of calculations
creates subfolders within the given folder and copies present in this parent
folder into the subfolders.
The files that are different for the differnt calculations have to be in another
folder.
"""

from shutil import copyfile
from os import listdir
from os.path import isfile, join, exists
from os import path, makedirs
path_parent_folder = "/home/lukas/documents/thesis/upload/cleave/afCrN_TiN_1-10/distance_variation/"
path_var_folder = "/home/lukas/documents/thesis/Structures/CrNTiN_cleaved/afCrNTiN_1-10/"
number = "11"
subfolder_name = "d"
file_name = "POSCAR"
subfolder_names = []

path_parent_folder += number
path_var_folder += number

files_parent = [f for f in listdir(path_parent_folder) if isfile(join(path_parent_folder, f))]


files_var = [join(path_var_folder,f) for f in listdir(path_var_folder)
             if isfile(join(path_var_folder,f))]

i = 1

for path_var in files_var:
    path_sub = join(path_parent_folder,subfolder_name+"_{}".format(i))
    subfolder_names.append(subfolder_name+"_{}".format(i))
    if not exists(path_sub):
        makedirs(path_sub)

    copyfile(path_var,join(path_sub,file_name))

    for file in files_parent:
        copyfile(join(path_parent_folder,file),join(path_sub,file))
    i += 1

with open(join(path_parent_folder,"job_sub.sh"),"w") as file:
    for ent in subfolder_names:
        file.write("cd {}\n".format(ent))
        file.write("qsub job_run.sh\n")
        file.write("cd ..\n")
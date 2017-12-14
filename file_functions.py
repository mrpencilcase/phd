from shutil import copyfile
from os import listdir
from os.path import isfile, join, exists
from os import path, makedirs
from cleave_from_poscar import cleave_cell
from class_cell import File


def create_singel_calc(path_create,poscar,incar,potcar,kpoints,submit):
    if not exists(path_create):
        makedirs(path_create)
    write_file(path_create, kpoints.filname, kpoints.data)
    write_file(path_create, incar.filename, incar.data)
    write_file(path_create, potcar.filename, potcar.data)
    write_file(path_create, poscar.filename, poscar.data)
    write_file(path_create, submit.filename, submit.data)


# Create file with data at path
def write_file(path,filename,data):
    with open(join(path,filename),"w") as file:
        for ent in data:
            file.write(ent)


def read_file(path,filename):
    with open(path,"r") as file:
        data = list(file)
    file_data = File(filename,path,data)
    return file_data
from shutil import copyfile
from os import listdir
from os.path import isfile, join, exists
from os import path, makedirs
from cleave_from_poscar import cleave_cell



def create_singel_calc(path_create,poscar,incar,potcar,kpoints,submit):
    if not exists(path_create):
        makedirs(path_create)
    write_file(path_create, kpoints.filename, kpoints.data)

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

class File:
    def __init__(self,filename,path,data):
        self.filename = filename
        self.path = path
        self.data = data

# add, change or delete flags from the incar file
def modifiy_incar(path_open, flag, value):
    with open(join(path_open,"INCAR"),"r") as file:
        incar = list(file)
        mod = False

        #Change or delete flag
        for i in range(len(incar)):
            if flag in incar[i]:
                if value != "":
                    incar[i] = flag + " = " + value + "\n"
                    mod = True
                else:
                    incar.pop(i)
                    mod = True
        if mod == False:
            incar.append(flag + " = " + value + "\n")

    with open(join(path_open,"INCAR"),"w") as file:
        for line in incar:
            file.write(line)


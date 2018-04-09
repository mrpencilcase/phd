from shutil import copyfile, copyfileobj
from os import listdir
from os.path import isfile, join, exists
from os import path, makedirs
from cleave_from_poscar import cleave_cell
import read_poscar as rp


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

# create POTCAR according to the POSCAR
def create_potcar(path_open,filename):
    poscar = read_file(join(path_open,filename))
    pot_files = ["POSCAR_"+atom for atom in poscar[5].split()]

    with open(join(path_open,"POTCAR"), 'w') as outfile:
        for fname in pot_files:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

# read a textfile and convert it to a list element
#def read_file(path_open):
#    with open(path_open,"r") as file:
#        data = list(file)
#    return data

def contegate_files(file_list,path_save):
    with open(path_save, 'wb') as wfd:
        for f in file_list:
            with open(f, 'rb') as fd:
                copyfileobj(fd, wfd, 1024 * 1024 * 10)

def cleave_cell(cleave_axis, cleave_d, cleave_pos, path_open):
    """
    Function to split the supercell at a certain postion
    :param cleave_axis: (a,b,c)
    :param cleave_d: Distance of the created gap
    :param cleave_pos: Postion of the gap
    :param path_xyz:  Path to the relaxed supercell
    :param path_save: Path where the file should be stored (incl. filename)
    :return: None!! A file is created at the postion of path_save
    """
    delta_c = 0.8

    poscar = rp.read_poscar(path_open,"base cell")

    if poscar.format == "Direct":
        poscar.switch_format()
    a_lattice = poscar.lattice.a
    b_lattice = poscar.lattice.b
    c_lattice = poscar.lattice.c
    ele_type = poscar.elements.element_type
    ele_num = poscar.elements.element_amount
    at_pos =[]
    for at in poscar.atoms:
        at_pos.append(at.position)


    if cleave_axis == "a":
        axis_index = 0
        a_lattice[axis_index] += cleave_d
    elif cleave_axis == "b":
        axis_index = 1
        b_lattice[axis_index] += cleave_d
    elif cleave_axis == "c":
        axis_index = 2
        c_lattice[axis_index] += cleave_d

    c_pos = []

    for pos in at_pos:
        if pos[axis_index] not in c_pos:
            c_pos.append(pos[axis_index])
    c_pos.sort()

    i = 0
    while i < len(c_pos)-1:
        if c_pos[i+1] <= c_pos[i]+delta_c:
            c_pos.pop(i+1)
            i = -1
        i += 1

    if cleave_pos > len(c_pos):
        print("The postion of the cleave is not in the super cell. \n"
              "Please change the postions and start the script again."
              )
        exit()

    for i in range(len(at_pos)):
        if at_pos[i][axis_index] > c_pos[cleave_pos - 1]+ delta_c:
            at_pos[i][axis_index] += cleave_d

    el_num_str = []
    for num in ele_num:
        el_num_str.append(str(num))

    file = []

    file.append("{}\n".format(poscar.info))
    file.append("{}\n".format(str(poscar.scale)))
    for vec in [a_lattice,b_lattice,c_lattice]:
        file.append("{:7.4f}  {:7.4f}  {:7.4f}\n".format(vec[0], vec[1], vec[2]))
    file.append(" ".join("{:3s}".format(t) for t in ele_type) + "\n")
    file.append(" ".join("{:3s}".format(t) for t in el_num_str) + "\n")
    file.append("Cartesian\n")
    for pos in at_pos:
        file.append("{:7.4f}  {:7.4f}  {:7.4f}\n".format(pos[0],pos[1],pos[2]))

    return file

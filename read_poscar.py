"""
Skript to read the data of a POSCAR or CONTCAR file and return the data in form
of a cell variable
"""

from class_cell import Cell
import os

def read_poscar(path_open,material):
    cell =  Cell
    with open(path_open,"r") as file:
        cell_data = list(file)

    cell.name = material
    cell.set_info(cell_data[0])
    cell.set_scale(cell_data[1])
    latt_a = [float(ent) for ent in cell_data[2].split()]
    latt_b = [float(ent) for ent in cell_data[3].split()]
    latt_c = [float(ent) for ent in cell_data[4].split()]
    cell.add_lattice(latt_a,latt_b,latt_c)
    cell.set_format(cell_data[5])



    return cell

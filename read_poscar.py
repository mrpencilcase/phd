"""
Skript to read the data of a POSCAR or CONTCAR file and return the data in form
of a cell variable
"""

from class_cell import Cell
from class_cell import Atom
import os

def read_poscar(path_open,material):
    cell =  Cell(material)
    with open(path_open,"r") as file:
        cell_data = list(file)

    cell.name = material
    cell.set_info(cell_data[0])
    cell.set_scale(cell_data[1])
    latt_a = [float(ent) for ent in cell_data[2].split()]
    latt_b = [float(ent) for ent in cell_data[3].split()]
    latt_c = [float(ent) for ent in cell_data[4].split()]
    cell.add_lattice(latt_a,latt_b,latt_c)

    cell.set_format(cell_data[7])
    line_el = [ent for ent in cell_data[5].split()]
    line_am = [ent for ent in cell_data[6].split()]
    for el , am in zip(line_el, line_am):
        cell.elements.add_element(el,am)
    j = 1
    k = 0
    at_amount = cell.elements.element_amount[k]
    element = cell.elements.element_type[k]
    for i in range(8,8+sum(cell.elements.element_amount)):
        pos = [float(ent) for ent in cell_data[i].split()]
        if j > at_amount:
            k += 1
            at_amount += cell.elements.element_amount[k]
            element = cell.elements.element_type[k]

        j += 1
        add_at = Atom(element,pos)
        cell.add_atom(add_at)

    return cell

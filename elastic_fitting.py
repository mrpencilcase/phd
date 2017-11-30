# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 14:44:45 2016
@author: Lukas

Script to calculate the stiffnes tensor along with the Young's Modulus, 
the Bulk Modulus, the Poison Ration and the Shear Modulus. It requires the lattice 
parameters of the initial cell, and of a set of deformed cells. 
"""

import os 
import string
import numpy as np
import time
import re
import postprocess_lukas as pp 



# Set the crystal structure of the material
# System = raw_input("Please enter the crystall symetrie (cubic, hexagonal, tetragonal, orthorombic, monoclin or triklin):")

#    path = "C:/Users/Lukas/Documents/Diplomarbeit/Results/Elastic/alpha_Al2O3_2/epsmax_2.0"
#    path = "C:\Users\Lukas\Documents\Diplomarbeit\Python_Scripts\elastic"
path = "/home/lukas/Documents/thesis/result_vasp/elastic/TiN/epsmax_2.0/"
path = "/home/lukas/Documents/thesis/result_vasp/elastic/af_CrN/epsmax_2.5/"
Symmetry = "orthogonal"


with open(os.path.join(path,"INCAR"),"r") as file:
    INCAR = list(file)

Name = INCAR[0]

folder = [ x[0] for x in os.walk(path) ]
folder.pop(0)

# Empty list for the stresses
stress= []
strain = []

# Read the lattice parameter and the remaining stressesof the relaxed base structure.
# Therfore the OUTCAR and CONTCAR files of the base structure are required.
# Get the relaxed lattice

with open(os.path.join(path,"CONTCAR")) as file:
    CONTCAR = list(file)

fscale=float(CONTCAR[1])
a_base=[fscale*float(x) for x in CONTCAR[2].split()]
b_base=[fscale*float(x) for x in CONTCAR[3].split()]
c_base=[fscale*float(x) for x in CONTCAR[4].split()]

a_base = np.asarray(a_base)
b_base = np.asarray(b_base)
c_base = np.asarray(c_base)

base = np.vstack((a_base,b_base,c_base))
# Get the stresses

with open(os.path.join(path,"OUTCAR"),"r") as file:
    OUTCAR = list(file)

i = len(OUTCAR)-1
while i >= 0 :

    if "FORCE on cell =-STRESS in cart. coord.  units (eV):" in OUTCAR[i]:
        line = OUTCAR[i+14]


        # the six entries are split and multipllied by -0.1 to correct the

        stress_rel = ([x for x in line.split()])
        stress_rel.pop(0)
        stress_rel.pop(0)
        stress_rel = [float(x)*-0.1 for x in stress_rel]
        stress_rel.append( stress_rel.pop(3) )
        stress_rel=np.asarray(stress_rel)
        i = -1

    i = i-1;

# Loop to read the stresses and lattices from the different OUTCAR files of the deformed
# cells in addititon the actual strain is calculated

for ent in folder:
    # Read the stresses from the OUTCAR file
    with open(os.path.join(ent,"OUTCAR"), "r") as file:
        OUTCAR = list(file)

    i = len(OUTCAR)-14

    if "General timing and accounting informations for this job:" in OUTCAR[i]:
        while i >= 0 :

            if "FORCE on cell =-STRESS in cart. coord.  units (eV):" in OUTCAR[i] :
                line = OUTCAR[i+14]
                stress_raw = ([x for x in line.split()])
                stress_raw.pop(0)
                stress_raw.pop(0)
                stress_raw = [float(x) * -0.1 for x in stress_raw]
                stress_raw.append(stress_raw.pop(3) )
                stress_raw = np.asarray(stress_raw)
                stress.append(np.subtract(stress_raw,stress_rel))
                #stress.append(stress_raw)
                i=-1
            i = i - 1

    # Read the lattice from the CONTCAR file
    with open(os.path.join(ent,"CONTCAR"), "r") as file:
        CONTCAR = list(file)
    fscale=float(CONTCAR[1])
    a_def=[fscale*float(x) for x in CONTCAR[2].split()]
    b_def=[fscale*float(x) for x in CONTCAR[3].split()]
    c_def=[fscale*float(x) for x in CONTCAR[4].split()]

    a_def = np.asarray(a_def)
    b_def = np.asarray(b_def)
    c_def = np.asarray(c_def)
    base_def = np.vstack((a_def,b_def,c_def))

    # calculate the strain using the relaxed and deformed lattices
    strain.append(pp.strain(base,base_def))

#    sig = np.asarray(stress)
#    eps = np.asarray(strain)

# Calculate the raw stiffnes tensor. Withe da strain and stress arrays.
C_raw = pp.stiffnes_tensor_calc(strain,stress)
print(str(np.asarray(C_raw)))
# Refine the raw stiffnes tensor according to the

C_ref = pp.project_Cij(C_raw,Symmetry)

S_ref = np.linalg.pinv(C_ref)

print(str(C_ref))


print(str(S_ref))
print("Young's Modul")
print(str(1/S_ref[0,0]))

# write data into a file
with open(os.path.join(path,"elastic_data.dat"),"w") as outfile:

    outfile.write("Name \n")
    outfile.write("\n")
    outfile.write("Created :"+ time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) +"\n\n")
    outfile.write("Stiffness Tensors (C) :\n\n")
    outfile.write("Raw Stiffenstensor from the calculation:\n")
    for ent in np.ndarray.tolist(C_raw):
        outfile.write("{:8.3f} {:8.3f} {:8.3f} {:8.3f} {:8.3f} {:8.3f}\n"
                      .format(ent[0], ent[1], ent[2], ent[3], ent[4], ent[5]))
    outfile.write("\n\n")
    outfile.write("Refined Stiffenstensor according to the crystal structure of the material ({}):\n".format(Symmetry))
    for ent in np.ndarray.tolist(C_ref):
        outfile.write("{:8.3f} {:8.3f} {:8.3f} {:8.3f} {:8.3f} {:8.3f}\n"
                      .format(ent[0], ent[1], ent[2], ent[3], ent[4], ent[5]))
    outfile.write("\n\n")

    case_nr = 1

    while case_nr <= len(strain):
        outfile.write("Deformation Case {}: \n".format(case_nr))
        outfile.write("Stresses in Voigth Notation: ")

        for ent in stress[case_nr-1]:
            outfile.write("%06.4f " % ent )

        outfile.write("\nStrain in Voigth Notation:   ")
        for ent in strain[case_nr-1]:
            outfile.write("%06.4f " % ent )

        outfile.write("\n")
        outfile.write("\n")
        case_nr += 1
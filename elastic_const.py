# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 11:25:32 2016

@author: Lukas
"""

import os
import numpy as np
import shutil
import preprocess_lukas as pp
from sys import exit

# Name and time for the job
Name = "alphaAlO_e2"
time = "02:00:00"
eps_min = 1
eps_max = 3
intervall = 0.5
# Set the number of sets of strain vectors that will be used (1-6)
# each set is composed of a singel strain vector and it's negative
# counterpart.
n = 6

CONTCAR = open("CONTCAR")
data = CONTCAR.readlines()
CONTCAR.close()

fscale = float(data[1])
a_base = [fscale * float(x) for x in data[2].split()]
b_base = [fscale * float(x) for x in data[3].split()]
c_base = [fscale * float(x) for x in data[4].split()]

path_skript = os.path.dirname(os.path.abspath(__file__))

eps = eps_min
while eps <= eps_max:
    path_eps = path_skript + "/" + "epsmax_" + str(eps)

    if not os.path.exists(path_eps):
        os.makedirs(path_eps)

    submit = open(path_skript + "/job_submit_" + str(eps) + ".sh", "w")

    shutil.copy("CONTCAR", path_eps)
    shutil.copy("POTCAR", path_eps)
    shutil.copy("KPOINTS", path_eps)
    shutil.copy("INCAR", path_eps)

    for x in range(0, 2 * n):

        # create folder for each deformation
        path = path_eps + "/" + Name + "_eps" + str(eps) + "_" + str(x + 1)
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path)
        # copy the POTCAR and POSCAR file from the parent foder to the sub folder
        shutil.copy("POTCAR", path)
        shutil.copy("KPOINTS", path)
        shutil.copy("INCAR", path)
        shutil.copy("OUTCAR", path)

        un = pp.ucls(x, eps)

        strain = np.matrix([[un[0], un[5] / 2, un[4] / 2],
                            [un[5] / 2, un[1], un[3] / 2],
                            [un[4] / 2, un[3] / 2, un[2]]])

        # Calculation of the new a vector

        dx = (
        a_base[0] * strain.item(0, 0) + a_base[1] * strain.item(0, 1) + a_base[
            2] * strain.item(0, 2))
        dy = (
        a_base[1] * strain.item(1, 1) + a_base[0] * strain.item(1, 0) + a_base[
            2] * strain.item(1, 2))
        dz = (
        a_base[2] * strain.item(2, 2) + a_base[0] * strain.item(2, 0) + a_base[
            1] * strain.item(2, 1))

        a_def = [a_base[0] + dx, a_base[1] + dy, a_base[2] + dz]

        # Calculation of the new b vector

        dx = (
        b_base[0] * strain.item(0, 0) + b_base[1] * strain.item(0, 1) + b_base[
            2] * strain.item(0, 2))
        dy = (
        b_base[1] * strain.item(1, 1) + b_base[0] * strain.item(1, 0) + b_base[
            2] * strain.item(1, 2))
        dz = (
        b_base[2] * strain.item(2, 2) + b_base[0] * strain.item(2, 0) + b_base[
            1] * strain.item(2, 1))

        b_def = [b_base[0] + dx, b_base[1] + dy, b_base[2] + dz]

        # Calculation of the new c vector

        dx = (
        c_base[0] * strain.item(0, 0) + c_base[1] * strain.item(0, 1) + c_base[
            2] * strain.item(0, 2))
        dy = (
        c_base[1] * strain.item(1, 1) + c_base[0] * strain.item(1, 0) + c_base[
            2] * strain.item(1, 2))
        dz = (
        c_base[2] * strain.item(2, 2) + c_base[0] * strain.item(2, 0) + c_base[
            1] * strain.item(2, 1))

        c_def = [c_base[0] + dx, c_base[1] + dy, c_base[2] + dz]
        #Open an old POSCAR to get the ion positions the unit cell vectors are
        #replaced with the deformed vectors from the base structure CONTCAR file

#       POSCAR = open("POSCAR")
#      data = POSCAR.readlines()
#        POSCAR.close()

        data[0] = Name + "\n"
        data[1] = "1\n"
        data[2] = str(a_def[0]) + " " + str(a_def[1]) + " " + str(
            a_def[2]) + " " + "\n"
        data[3] = str(b_def[0]) + " " + str(b_def[1]) + " " + str(
            b_def[2]) + " " + "\n"
        data[4] = str(c_def[0]) + " " + str(c_def[1]) + " " + str(
            c_def[2]) + " " + "\n"

        POSCAR = open(path + "/POSCAR", "w")
        POSCAR.writelines(data)
        POSCAR.close()

        submit.write("cd " + path + "\n")
        submit.write("qsub job_run.sh\n")

        run = open(path + "/job_run.sh", "w")
        run.write("#!bin/sh\n")
        run.write("#$ -N " + Name + "U_" + str(x) + "\n")
        run.write("#$ -pe mpich 16\n")
        run.write("#$ -V\n")
        run.write("#$ -l h_rt=" + time + "\n")
        run.write("#$ -q all.q\n")
        # run.write("#$ -M lukas.loefler@student.tuwien.ac.at\n")
        # run.write("#$ -m beas\n")
        run.write(
            "mpirun -machinefile $TMPDIR/machines -np $NSLOTS /opt/sw/vasp/5.3.1/vasp_impi4.1.0.024_sca_mkl_vtst3.0b\n")
        run.close()

    eps = eps + intervall
    submit.write("exit")
    submit.close()

exit()


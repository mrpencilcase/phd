#script to simplifie the process of finding the point of convergence
#TO DO BEFORE RUNNING THE SCRIPT
#set name, run time and the ranges of E_cutoff/k_points. 
#make sure that the lines for the KPOINT and INCAR are the 
#ones you desire add or remove lines as you please. The name of the directories
#may also be changed.

#RUNING THE SCRIPT
#the script has to be placed in a directory with the POTCAR and POSCAR 


import os
import shutil


#variables
Name = "CrTiN"
time = "24:00:00"

#parmeters for E_cutoff
E_cutoff_start =300
E_cutoff_end = 300
E_cutoff_step = 100

#parameters for k_points
k_points_start = 10
k_points_end = 70
k_points_step = 10

#get the path of the script
path_skript = os.path.dirname(os.path.abspath(__file__))

##############################################################################
# Create the directory and files for all combinations of Ecutoff and kpoints #
##############################################################################
f = open("filestructure","w")

#Loops over all cutoff engergies and k-Points
E_cutoff = E_cutoff_start

while (E_cutoff <= E_cutoff_end):
    k_points =  k_points_start
    while (k_points <= k_points_end):
        #create folder for each combination       
        path = path_skript + "/" + Name +"/" + Name + "_E" + str(E_cutoff) +"_k" + str(k_points)
        if not os.path.exists(path) :
            os.makedirs(path)     
        #copy the POTCAR and POSCAR file from the parent foder to the sub folder
        shutil.copy("POTCAR",path)
        shutil.copy("POSCAR",path)
        
        #create KPOINT in the subfolder
        k =open(path+"/KPOINTS","w")
        k.write("k_points\n")
        k.write("0\n")
        k.write("automatic\n")
        k.write(str(k_points))
        k.close()
        
        #create INCAR in the subfolder
        E = open(path+"/INCAR","w")
        E.write(Name+"\n")
        E.write("ENCUT = "+str(E_cutoff)+"\n")
        E.write("PREC = Med\n")
        E.write("EDIFF = 1E-04\n")
        E.write("ALGO = FAST\n")
        E.write("LWAVE = FALSE\n")
        E.write("LCHARGE = FALSE\n")
        E.write("LREAL = Auto\n")
        E.write("NPAR = 4\n")
        E.write("IBRION = 2\n")
        E.write("ISPIN = 2\n")
        E.write("LORBIT = 11\n")
        E.write("MAGMOM= 18*2 9*-2 27*0 54*0\n")
        E.write("ISIF = 0\n")
        E.write("NSW = 100\n")
        E.write("ISMEAR = 1\n")
        E.write("SIGMA = 0.1\n")
        E.close()
        
        #create job file
        J = open(path+"/job_run.sh","w")
        J.write("#!bin/sh\n")
        J.write("#$ -N " + Name + "_E" + str(E_cutoff/100) +"_k" + str(k_points/10)+"\n")
        J.write("#$ -pe mpich 16\n")
        J.write("#$ -V\n")
        J.write("#$ -l h_rt="+time+"\n")
        J.write("#$ -q all.q\n")
        #J.write("#$ -M lukas.loefler@student.tuwien.ac.at\n")
        #J.write("#$ -m beas\n")
        J.write("mpirun -machinefile $TMPDIR/machines -np $NSLOTS /opt/sw/vasp/5.3.1/vasp_impi4.1.0.024_sca_mkl_vtst3.0b\n")
        J.close()
       #document the directories for later analysis
        #the name and the corresponding E_Cutoff & k_points are stored
        f.write(Name + "_E" + str(E_cutoff) +"_k" + str(k_points) + "\n")
        f.write(str(E_cutoff) + "\n")
        f.write(str(k_points) + "\n")
        k_points = k_points + k_points_step
        
    E_cutoff = E_cutoff + E_cutoff_step
    
f.close()
##############################################################################
#             Create the script to submit all jobs to the queue              #
##############################################################################

submit = open(path_skript+"/"+Name+"/job_submit.sh","w")
d = open("filestructure","r")
# loop over the different directories stored in filestructure
line = d.readline()
line = line.rstrip()

submit.write("#!/bin/bash\n")
while (line != ""):
    submit.write("cd " + path_skript+"/" + Name +"/"+ line +"\n")
    submit.write("qsub job_run.sh\n")
    submit.write("echo `qstat | tail -1 | awk '{printf $1}'` "  "  `pwd`   >> /home/lv70379/liangcai/othermembers/directoryjobs\n")
    d.readline()
    d.readline()
    line = d.readline()
    line = line.rstrip()
submit.write("qstat\n")    
submit.close()
d.close()

#run bash script
#command = "sh job_submit.sh"
#subprocess.Popen(command)
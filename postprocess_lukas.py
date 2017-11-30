# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 10:48:02 2016

@author: Lukas
"""
import string
import numpy as np
from numpy import linalg as la
from math import sqrt

# calculates the strain of a deformed lattice
def strain(lattice_rel,lattice_def):
    
    eps_ten = np.linalg.solve(lattice_rel,lattice_def)
    eps_ten = eps_ten - np.eye(3)
    eps_vec_np = np.array( [eps_ten[0,0]        ,  
                            eps_ten[1,1]        , 
                            eps_ten[2,2]        , 
                            eps_ten[1,2] * 2    ,
                            eps_ten[0,2] * 2    ,
                            eps_ten[0,1] * 2     ])    

    return eps_vec_np
    
    
# calculates the stiffnestensor by using matrix multiplications
def stiffnes_tensor_calc(strains, stresses):
    
    strains_t = np.transpose(strains)
    stresses_t = np.transpose(stresses)
    
    #Calculate the inverse of stress_t
    strain_inv = np.linalg.pinv(strains_t)
    
    C_dot = np.dot(stresses_t,strain_inv)
    
    C_dot = 0.5 * (C_dot+ np.transpose(C_dot))
    
    
    return C_dot
"""    
 calculates the stiffnestensor by fitting it to an symetrie dependend
 equation system. 
 INPUT:
 stress: is matrix contians the voigts stress vectors in its rows
 strains: is matrix contians the voigts strains vectors in its rows
 symetry: defines the crystall system 
 n: is a integer that determins how many of the strain stress pairs are used for 
    the fit 
 OUTPUT:
"""    
def stiffnes_tensor_fit(stress, strain,symetry, n):
    
    if symetry == "cubic":
        from fitting_functions import fit_cubic    
        C,E_modul, G_modul, Pois_ratio, res =fit_cubic(stress,strain,n)
        
    elif  symetry == "hexagonal":
        from fitting_functions import fit_hex    
        C,E_modul, G_modul, Pois_ratio=fit_hex(stress,strain,n)   
        
    elif  symetry == "tetragonal":
        from fitting_functions import fit_tet    
        C=fit_tet(stress)
        
    elif  symetry == "orthogonal":
        from fitting_functions import fit_tet    
        C=fit_tet(stress)
        
        
    return C, E_modul, G_modul, Pois_ratio
    
# refines the calculated stiffnestensor and brings it to the adequate form for
# the given symetry. In addition the different material proberties are calculated 
# from C
# INPUT:
# C: stiffnes tensor
# symetry: name of the crystal system    
def stiffnes_tensor_ref(C,symetry):
    if symetry == "cubic":
        C11 = (C[0,0]+C[1,1]+C[2,2])/3
        C12 = (C[0,1]+C[0,2]+C[1,2]+C[1,0]+C[2,0]+C[2,1])/6
        C44 = (C[3,3]+C[4,4]+C[5,5])/3
        
        C_ref = np.array([
            [C11,C12,C12,  0,  0,  0] ,
            [C12,C11,C12,  0,  0,  0] ,
            [C12,C12,C11,  0,  0,  0] ,
            [  0,  0,  0,C44,  0,  0] ,
            [  0,  0,  0,  0,C44,  0] ,
            [  0,  0,  0,  0,  0,C44] ])
    
        
        Ex = 1/np.linalg.inv(C)[0,0]
        Gx = 1/np.linalg.inv(C)[3,3]
        E_modul = [Ex,Ex,Ex]
        G_modul = Gx
        Pois_ratio = -np.linalg.inv(C)[0,1]/E_modul        
        
    elif  symetry == "hexagonal":
        C11 = (C[0,0]+C[1,1])/2
        C12 = (C[0,1]+C[1,0])/2
        C13 = (C[2,0]+C[2,1]+C[0,2]+C[1,2])/4
        C33 = C[2,2]
        C44 = (C[3,3]+C[4,4])/2
        
        C_ref = np.array([
            [C11,C12,C13,  0,  0,          0] ,
            [C12,C11,C13,  0,  0,          0] ,
            [C13,C13,C33,  0,  0,          0] ,
            [  0,  0,  0,C44,  0,          0] ,
            [  0,  0,  0,  0,C44,          0] ,
            [  0,  0,  0,  0,  0,(C11-C12)/2] ])
            
        ET = (C11-C12)*(C11*C33+C12*C33-2*C13*C13)/(C11*C33-C13*C13)
        EL = C33-C13*C13/(C11+C12)
        E_modul = [ET,ET,EL] 
        G_modul = (C11-C12)/2
        Pois_ratio = C13/(C11+C12)         
        
    elif  symetry == "tetragonal":
        C11 = (C[0,0]+C[1,1])/2
        C12 = (C[0,1]+C[1,0])/2
        C13 = (C[2,0]+C[2,1]+C[0,2]+C[1,2])/4
        C16 = (C[5,0]-C[5,1]+C[0,5]-C[1,5])/4
        C33 = C[2,2]
        C44 = (C[3,3]+C[4,4]+C[5,5])/3
        
        C_ref = np.array([
            [C11, C12, C13,  0,  0,        C16] ,
            [C12, C11, C13,  0,  0,       -C16] ,
            [C13, C13, C33,  0,  0,          0] ,
            [  0,    0,  0,C44,  0,          0] ,
            [  0,    0,  0,  0,C44,          0] ,
            [C16, -C16,  0,  0,  0,(C11-C12)/2] ])
            
        ET = (C11-C12)*(C11*C33+C12*C33-2*C13*C13)/(C11*C33-C13*C13)
        EL = C33-C13*C13/(C11+C12)
        E_modul = [ET,ET,EL] 
        G_modul = (C11-C12)/2
        Pois_ratio = C13/(C11+C12)    
        
    elif  symetry == "orthrombic":
        C11 = (C[0,0]+C[1,1])/2
        C12 = (C[0,1]+C[1,0])/2
        C13 = (C[2,0]+C[2,1]+C[0,2]+C[1,2])/4
        C16 = (C[6,0]+C[6,1]+C[0,6]+C[1,6])/4
        C33 = C[3,3]
        C44 = (C[3,3]+C[4,4]+C[5,5])/3
        
        C_ref = np.array(
            [C11, C12, C13,  0,  0,        C16] ,
            [C12, C11, C13,  0,  0,       -C16] ,
            [C13, C13, C33,  0,  0,          0] ,
            [  0,    0,  0,C44,  0,          0] ,
            [  0,    0,  0,  0,C44,          0] ,
            [C16, -C16,  0,  0,  0,(C11-C12)/2] )
            
        ET = (C11-C12)*(C11*C33+C12*C33-2*C13*C13)/(C11*C33-C13*C13)
        EL = C33-C13*C13/(C11+C12)
        E_modul = [ET,ET,EL] 
        G_modul = (C11-C12)/2
        Pois_ratio = C13/(C11+C12)  


    
    elif  symetry == "triclin":
        C11 = C[0,0]
        C22 = C[1,1]
        C33 = C[2,2]
        C44 = C[3,3]
        C55 = C[2,2]
        C66 = C[3,3]
        C12 = (C[0,1]+C[1,0])/2
        C13 = (C[0,2]+C[2,0])/2
        C14 = (C[0,3]+C[3,0])/2
        C15 = (C[0,4]+C[4,0])/2
        C16 = (C[0,5]+C[5,0])/2
        C23 = (C[1,2]+C[2,1])/2
        C24 = (C[1,3]+C[3,1])/2
        C25 = (C[1,4]+C[4,1])/2
        C26 = (C[1,5]+C[5,1])/2
        C34 = (C[2,3]+C[3,2])/2
        C35 = (C[2,4]+C[4,2])/2
        C36 = (C[2,5]+C[5,2])/2
        C45 = (C[3,4]+C[4,3])/2
        C46 = (C[3,5]+C[5,3])/2
        C56 = (C[4,5]+C[5,4])/2

        
        C_ref = np.array([
            [C11, C12, C13, C14, C15, C16] ,
            [C12, C22, C23, C24, C25, C26] ,
            [C13, C23, C33, C34, C35, C36] ,
            [C14, C24, C34, C44, C45, C46] ,
            [C15, C25, C35, C45, C55, C56] ,
            [C16, C26, C36, C46, C56, C66] ] )
            
        ET = (C11-C12)*(C11*C33+C12*C33-2*C13*C13)/(C11*C33-C13*C13)
        EL = C33-C13*C13/(C11+C12)
        E_modul = [ET,ET,EL] 
        G_modul = (C11-C12)/2
        Pois_ratio = C13/(C11+C12)  
        
    
    return C_ref,E_modul, G_modul, Pois_ratio
    


def read_data(path,name,supercell):
    
    data = []
    data.append("Name: " + name)
    #read the total Energie from the OUTCAR
    OUTCAR = open(path + "/OUTCAR","r")
    out = list(OUTCAR) 
    index = len(out) - 14
      
    #check if vasp finished the calculation if true then get des last value
    #of the total energy if false skip this subfolder
    calc_end = out[index]
    calc_end=calc_end.lstrip()
    calc_end=calc_end.rstrip()
    if "General timing and accounting informations for this job:" ==calc_end:
        while index >= 0 :
            out_ele=out[index]             
            out_ele=out_ele.rstrip()
            out_ele=out_ele.lstrip()
            if out_ele == "FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)" :
                em=out[index+2]  
                em=em.translate(None,string.ascii_letters + "=")
                em=em.lstrip()
                em=em.rstrip()
                #set index to zero to end loop
                index=0
            index = index - 1     
    
    
    
    #read structure parameters from the CONTCAR
    CONTCAR=open(path +'/CONTCAR','r')
    CONTCAR.readline()
    aSc=float(CONTCAR.readline())
    a1In=[aSc*float(x) for x in CONTCAR.readline().split()]
    a2In=[aSc*float(x) for x in CONTCAR.readline().split()]
    a3In=[aSc*float(x) for x in CONTCAR.readline().split()]    
    data.append("Scaling_Factor: " + str(aSc))
    data.append("a: " + str(a1In[0]/supercell[0]) + " " + str(a1In[1]/supercell[1]) + " " + str(a1In[2]/supercell[2]))
    data.append("b: " + str(a2In[0]/supercell[0]) + " " + str(a2In[1]/supercell[1]) + " " + str(a2In[2]/supercell[2]))
    data.append("c: " + str(a3In[0]/supercell[0]) + " " + str(a3In[1]/supercell[1]) + " " + str(a3In[2]/supercell[2]))
    line=CONTCAR.readline().split()
    try:
        Natoms=sum([int(x) for x in line])
    except ValueError:
        line=CONTCAR.readline().split()
        Natoms=sum([int(x) for x in line])
    CONTCAR.close()
    # process lattice parameters
    a1 = la.norm(a1In)/supercell[0]
    a2 = la.norm(a2In)/supercell[1]
    a3 = la.norm(a3In)/supercell[2]
    alpha = (np.degrees(np.arccos(np.dot(a1In,a2In)/(la.norm(a1In)*la.norm(a2In)))))
    beta = (np.degrees(np.arccos(np.dot(a1In,a3In)/(la.norm(a1In)*la.norm(a3In)))))
    gamma = (np.degrees(np.arccos(np.dot(a2In,a3In)/(la.norm(a2In)*la.norm(a3In)))))
    V = (la.det([a1In, a2In, a3In])/Natoms)
    E = (float(em)/Natoms)
    data.append("Natoms: "      + str(Natoms))
    data.append("a: "           + str(a1))
    data.append("b: "           + str(a2))
    data.append("c: "           + str(a3))
    data.append("alpha: "       + str(alpha))
    data.append("beta: "        + str(beta))
    data.append("gamma: "       + str(gamma))    
    data.append("TotalEnergy: " + str(em))
    data.append("AtomEnergy: "  + str(E))
    data.append("CellVolume: "  + str(V*Natoms))
    data.append("AtomVolume: "  + str(V))
    data.append("Supercell: "   + str(supercell[0]) + " " +str(supercell[1]) + " " + str(supercell[2]))

    return data
# function to select a specific entry form the data set provided by read_data    
def select_data(signature,data):
    for ent in data:
        if signature+":" in ent:
            sdata = [x for x in ent.split()]
            sdata.pop(0)           
            sdata_float = [float(x) for x in sdata ]            
            np.asarray(sdata_float)            
            return sdata_float
    
# Reads magnetic data from the OUTCAR file at the given path and returns it 
# along with some valeus calculated from the raw data.
def magnetic_data(path):
    # Read the number of Atoms and the different Atom Types from the 
    # Contcar file
    with open(path + "CONTCAR","r") as data:
        lines = list(data)
        atom_groups = lines[5].split() 
        components = list(set(atom_groups))
        anum = [int(x) for x in lines[6].split()]
      #  anum = np.asarray(anum)
        natom = sum(anum)
        intervalls = []
    # create an intervalls of the ion positions as used in the contcar for
    # each atom type
    for ent in components:
        index = [i for i, x in  enumerate(atom_groups) if x == ent]
        intervall = []

        for x in index:
            i = 0   
            end_in = 0
            while i <= x:
                end_in = end_in + anum[i]
                i = i+1
            intervall.append(end_in-anum[x])        
            intervall.append(end_in-1)
        
        intervalls.append(intervall)    
    
    with open(path + "OUTCAR","r") as data:
        lines = list(data)
        index = []
        # search the outcar file for the phrase "magnetizatioin (x)" which indicates 
        # the list of magnetic moments and save the index
        for i, j in enumerate(lines):
            if "magnetization (x)" in j:
                index.append(i)
        
        tot_mean_singel_mom = [] 
        singel_asort_mom =[]
        total_mom = []
        for ent in index:
            i= ent + 4
            mag_mom = []
            while i <= ent +natom + 3:
                mag_mom.append(float(lines[i].split()[-1]))
                i = 1+i   
            
            for x in intervalls:
                 dummy = 0
                 j=0
                 while j < len(x):
                     dummy = dummy + sum(mag_mom[x[j]:x[j+1]])
                     j = j+2
                 singel_asort_mom.append(dummy)
            
            
            
            tot_mean_singel_mom.append(sum([abs(x) for x in mag_mom])/natom)
            total_mom.append(sum(mag_mom))
            
#    with open(path + "magneticmoments.dat", "w") as data:
#       i=1
#       for ent in total_mom:
#           data.write("Iteration {:d} :\n".format(i))
#           data.write("Toatl Magnetic Moment : {:.5f} \n".format(ent))
#           data.write("Mean Magnetic Moment : {:.5f} \n".format(tot_mean_singel_mom[i-1]))
#           data.write("Total Magnetic Moment of {} Atomes : {:.5f}\n".format(components[0],singel_asort_mom[2*i-2]))
#           data.write("Total Magnetic Moment of {} Atomes : {:.5f}\n".format(components[1],singel_asort_mom[2*i-1]))              
#           i =i +1 
    with open(path + "magnetic_moments.dat","w") as mag_dat:
        mag_dat.write("# Number of Iterations: {}".format(len(total_mom)))
        mag_dat.write("Mom total    Mom mean    Mom {}       Mom {} ".format(components[0],components[1]))
        



# Project the raw Cij tensor to the selected symmetry. 
def project_Cij(rawCij,Sym):
    
    
    projCij = np.zeros((6,6))    
    
    if Sym == "cubic":
        projCij[0,0] = np.round(np.mean([rawCij[i,i] for i in np.arange(3) ]),2)
        for i in np.arange(1,3):
          projCij[i,i] = projCij[0,0]
        projCij[3,3] = np.round(np.mean([rawCij[i,i] for i in np.arange(3,6) ]),2)
        for i in np.arange(4,6):
          projCij[i,i] = projCij[3,3]
        projCij[1,0] = np.round(np.mean([rawCij[1,0],rawCij[2,0],rawCij[2,1]]),2)
        projCij[2,0] = projCij[1,0]
        projCij[2,1] = projCij[1,0]
        projCij[0,1] = projCij[1,0]
        projCij[0,2] = projCij[1,0]
        projCij[1,2] = projCij[1,0]
        
    elif Sym == "hexagonal":
        # convert from Cij to Cijhat
        # Moakher & Norris, Eq. 7
        Cijhat = rawCij.copy()
        for j in range(3, 6):
            for i in range(3):
                Cijhat[i, j] *= sqrt(2)
                Cijhat[j, i] *= sqrt(2)
            for i in range(3, 6):
                Cijhat[i, j] *= 2
        
        # projecting on hexagonal symmetry
        # Moakher & Norris, Eq. A11a, A11b
        c11st = (3*Cijhat[0,0]+3*Cijhat[1,1]+2*Cijhat[0,1]+2*Cijhat[5,5])/8.
        c66st = (Cijhat[0,0]+Cijhat[1,1]-2*Cijhat[0,1]+2*Cijhat[5,5])/4.
        # Moakher & Norris, Eq. A15         
        projCij[0, 0] = np.round(c11st, 2)
        projCij[1, 1] = projCij[0, 0]
        projCij[2, 2] = np.round(Cijhat[2, 2], 2)
        projCij[3, 3] = np.round(np.mean([Cijhat[3, 3], Cijhat[4, 4]]), 2)
        projCij[4, 4] = projCij[3, 3]
        projCij[5, 5] = np.round(c66st, 2)
        projCij[1, 0] = np.round(c11st-c66st, 2)
        projCij[0, 1] = projCij[1, 0]
        projCij[2, 0] = np.round(np.mean([Cijhat[2, 0],Cijhat[2, 1]]), 2)
        projCij[2, 1] = projCij[2, 0]
        projCij[0, 2] = projCij[2, 0]
        projCij[1, 2] = projCij[2, 0]
        
        # convert back
        # Moakher & Norris, Eq. 7
        for j in range(3, 6):
            for i in range(3):
                projCij[i, j] /= sqrt(2)
                projCij[j, i] /= sqrt(2)
            for i in range(3, 6):
                projCij[i, j] /= 2
                
    elif Sym == "tetragonal":
        # convert from Cij to Cijhat
        # Moakher & Norris, Eq. 7
        Cijhat = rawCij.copy()
        for j in range(3, 6):
            for i in range(3):
                Cijhat[i, j] *= sqrt(2)
                Cijhat[j, i] *= sqrt(2)
            for i in range(3, 6):
                Cijhat[i, j] *= 2
        
        # projecting on tetragonal symmetry
        # Moakher & Norris, Eq. A16
        projCij = np.zeros((6, 6))
        projCij[0, 0] = np.mean([Cijhat[0, 0], Cijhat[1, 1]])
        projCij[1, 1] = projCij[0, 0]
        projCij[2, 2] = Cijhat[2, 2]
        projCij[3, 3] = np.mean([Cijhat[3, 3], Cijhat[4, 4]])
        projCij[4, 4] = projCij[3, 3]
        projCij[5, 5] = Cijhat[5, 5]
        projCij[1, 0] = Cijhat[1, 0]
        projCij[0, 1] = projCij[1, 0]
        projCij[2, 0] = np.mean([Cijhat[2, 0]+Cijhat[2, 1]])
        projCij[2, 1] = projCij[2, 0]
        projCij[0, 2] = projCij[2, 0]
        projCij[1, 2] = projCij[2, 0]
        projCij[0, 5] = (Cijhat[0, 5]-Cijhat[1, 5])/2.
        projCij[1, 5] = -projCij[0, 5]
        projCij[5, 0] = projCij[0, 5]
        projCij[5, 1] = projCij[1, 5]
        
        # convert back
        # Moakher & Norris, Eq. 7
        for j in range(3, 6):
            for i in range(3):
                projCij[i, j] /= sqrt(2)
                projCij[j, i] /= sqrt(2)
            for i in range(3, 6):
                projCij[i, j] /= 2
        projCij = np.around(projCij, 2)


    elif Sym == "orthogonal":
        # convert from Cij to Cijhat
        # Moakher & Norris, Eq. 7
        Cijhat = rawCij.copy()
        for j in range(3, 6):
            for i in range(3):
                Cijhat[i, j] *= sqrt(2)
                Cijhat[j, i] *= sqrt(2)
            for i in range(3, 6):
                Cijhat[i, j] *= 2


        projCij[0, 0] = Cijhat[0, 0]
        projCij[1, 1] = Cijhat[1, 1]
        projCij[2, 2] = Cijhat[2, 2]
        projCij[3, 3] = Cijhat[3, 3]
        projCij[4, 4] = Cijhat[4, 4]
        projCij[5, 5] = Cijhat[5, 5]

        projCij[0, 1] = Cijhat[0, 1]
        projCij[0, 2] = Cijhat[0, 2]
        projCij[1, 2] = Cijhat[1, 2]

        projCij[1, 0] = Cijhat[1, 0]
        projCij[2, 0] = Cijhat[2, 0]
        projCij[2, 1] = Cijhat[2, 1]


        # convert back
        # Moakher & Norris, Eq. 7
        for j in range(3, 6):
            for i in range(3):
                projCij[i, j] /= sqrt(2)
                projCij[j, i] /= sqrt(2)
            for i in range(3, 6):
                projCij[i, j] /= 2
        projCij = np.around(projCij, 2)

    return projCij
                
        
        
#def C_poly(C_mono,Symmetry):
#    if Symmetry == "cubic":
#        B0 = (C_mono[0,0]+ 2* C_mono[0,1])/3
#        Cx = (C_mono[0,0]-C_mono[0,1])/2
#        C44 = C_mono[3,3]
#        
#        B = B0
#        mu = np.linalg.solve([])
#          
#    elif Symmetry == "hexagonal":
#        
#        Kv = C_mono[2,2]+2*(C_mono[0,0]+C_mono[1,2])*4*C_mono[1,3]
#        M = C_mono[0,0] + C_mono[0,1] + 2*C_mono[2,2] - 4 * C_mono[0,3]
#        psi = C[0,0]+C[0,1]+2*C[2,2]-
#        
#    
#    
#    else:
#        c_poly = "The polycrystalin stiffnes tensor could not be calculatetd"
#        print(c_poly)
#        exit()
#        
#    E_poly = 9*B*mu/(3*B + mu )

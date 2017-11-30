# -*- coding: utf-8 -*-
"""
Created on Tue Aug 09 14:11:02 2016

@author: Lukas

Collection of functions which are applied before the calculations
"""

import os 
import string
import numpy as np
import textwrap
import sys


def deform_cell(lattice_relaxed, strain):
    
    
    strain_ten = np.array([[ strain[0]+1 ,strain[5]   ,strain[4]    ],
                           [ strain[5]   ,strain[1]+1 ,strain[3]    ],
                           [ strain[4]   ,strain[3]   ,strain[2]+1] ])
                          
    
    lattice_stressed = np.zeros((3,3),float)    
    i = 0
    for ent in lattice_relaxed:
        lattice_stressed[i,:]=np.dot(strain_ten,ent)
        i=i+1
                        
    return lattice_stressed
    
    
def ucls(num,max_def):
    
        un = np.array([ [ 1, 2, 3, 4, 5, 6] ,
                        [-1,-2,-3,-4,-5,-6] ,
                        [-2, 1, 4,-3, 6,-5] ,
                        [ 2,-1,-4, 3,-6, 5] ,
                        [ 3,-5,-1, 6, 2,-4] ,
                        [-3, 5, 1,-6,-2, 4] ,                    
                        [-4,-6, 5, 1,-3, 2] ,
                        [ 4, 6,-5,-1, 3,-2] ,                        
                        [ 5, 4, 6,-2,-1,-3] ,
                        [-5,-4,-6, 2, 1, 3] ,
                        [-6, 3,-2, 5,-4, 1] ,
                        [ 6,-3, 2,-5, 4,-1] ])
        
        strain = un[num, :]
        sf = float(max_def)/(100*max(abs(strain)))
        strain = strain * sf             
        return strain
        

# Get the lattice parameters from the OUTCAR or CONTCAR
def get_lattice(path,filename):
    base = []
    CONTCAR = open( path + "/" + filename )
    data = CONTCAR.readlines()
    CONTCAR.close()
    fscale=float(data[1])
    base.append([fscale*float(x) for x in data[2].split()])
    base.append([fscale*float(x) for x in data[3].split()])
    base.append([fscale*float(x) for x in data[4].split()])
    
    return base
    


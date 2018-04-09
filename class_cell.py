import numpy as np
from numpy import cos, sin, sqrt, square
import geometric_functions as gf

class Cell:

    def __init__(self,name):
        self.name = name
        self.lattice = Lattice()
        self.atoms = []
        self.elements = Elements()
        self.scale = 1
        self.info = ""
        self.format = ""

    def add_lattice(self,a,b,c):
        self.lattice.add_a(a)
        self.lattice.add_b(b)
        self.lattice.add_c(c)
        return self

    def add_atom(self,atom):
        self.atoms.append(atom)

    def set_scale(self,scaling_factor):
        self.scale = float(scaling_factor)

    def set_info(self,information):
        self.info = information.rstrip()

    def set_format(self,format):
        self.format = format.rstrip()

    def switch_format(self):

        a_len = np.linalg.norm(self.lattice.a)
        b_len = np.linalg.norm(self.lattice.b)
        c_len = np.linalg.norm(self.lattice.c)
        alpha = gf.angle_between(self.lattice.b,self.lattice.c)
        beta = gf.angle_between(self.lattice.a, self.lattice.c)
        gamma = gf.angle_between(self.lattice.a, self.lattice.b)
        omega = a_len*b_len*c_len*sqrt(1-square(cos(alpha))-square(cos(beta))-
                                       square(cos(gamma))+2*cos(alpha)*cos(beta)
                                       *cos(gamma))

        T = [[1/a_len, -cos(gamma)/(a_len*sin(gamma)), b_len*c_len*(
            cos(alpha)*cos(gamma)-cos(beta))/(omega*sin(gamma))],
             [0, 1/(b_len*sin(gamma)), a_len*c_len*(cos(beta)*cos(gamma)-
                                            cos(alpha))/(omega*sin(gamma))],
             [0, 0, (a_len*b_len*sin(gamma))/omega]]

        T_inv = np.linalg.pinv(T)
        if self.format == "Direct":
            for i in range(len(self.atoms)):
                self.atoms[i].position = np.dot(T_inv,self.atoms[i].position)
            self.format = "Cartesian"

        elif self.format == "Cartesian":
            for i in range(len(self.atoms)):
                self.atoms[i].position = np.dot(T,self.atoms[i].position)
            self.format = "Direct"

class Lattice:

    def __init__(self):
        self.a = []
        self.b = []
        self.c = []

    def add_a(self,v_lat):
        self.a = v_lat

    def add_b(self,v_lat):
        self.b = v_lat

    def add_c(self,v_lat):
        self.c = v_lat

class Atom:

    def __init__(self,element,position):
        self.element = element
        self.position = position

class Elements:

    def __init__(self):
        self.element_type = []
        self.element_amount = []

    def add_element(self,type,amount):
        self.element_type.append(type)
        self.element_amount.append(int(amount))

class File:
    def __init__(self,filename,path,data):
        self.filename = filename
        self.path = path
        self.data = data


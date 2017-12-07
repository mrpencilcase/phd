class Cell:

    def __init__(self,name):
        self.name = name
        self.lattice = Lattice
        self.atoms = []
        self.elements = []
        self.scale = 1
        self.info = ""
        self.format = ""

    def add_lattice(self,a,b,c):
        self.lattice.add_a(a)
        self.lattice.add_b(b)
        self.lattice.add_c(c)

    def add_atom(self,atom):
        self.atoms.append(atom)
        if atom.element not in self.elements:
            self.elements.append(atom.element)

    def set_scale(self,scaling_factor):
        self.scale = float(scaling_factor)

    def set_info(self,information):
        self.info = information.rstrip()

    def set_format(self,format):
        self.info = format.rstrip()

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
        self.position = element

class Elements:
    def __init__(self):
        self.element_type = []
        self.element_amount = []

    def add_element(self,type,amount):
        self.element_type.append(type)
        self.element_amount.append(int(amount))

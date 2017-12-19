import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from os.path import join

def main():
    path = "/home/lukas/documents/thesis/result_vasp/cleave/TiN/16sheets/1/"
    path = join(path,"e_cleave.dat")
    with open(path,"r") as file:
        data = list(file)

    e_dif = []
    e_cleave = []
    x = []

    for line in data:
        if "#" not in line:
            line_split = line.split()
            x.append(float(line_split[0]))
            e_cleave.append(float(line_split[1]))
            e_dif.append(float(line_split[2])*16.0218)


    print(x)
    print(e_dif)
    fit = curve_fit(E_x, x, e_dif)
    e_c = fit[0][0]
    l = fit[0][1]
    print(fit)
    x_plt = np.linspace(0,5,100)
    y_plt =  E_x(x_plt,e_c,l)
    E_crit = E_x(l,e_c,l)
    E_cleave = [e_c] * 100
    print(E_crit)

    plt.xlabel("")
    plt.plot()
    plt.plot(x_plt,y_plt,label = "Fit")
    plt.plot(x,e_dif,"+k",label = "DFT")
    plt.plot(l,E_crit,"+r")
    plt.plot(x_plt,E_cleave)
    plt.legend()
    plt.xlabel(r"Gap Distance [$\AA$]")
    plt.ylabel(r"Energy [J/$m²$]")
    plt.show()
def E_x(x,E_c,l):
    return E_c*(1-(1+x/l)*np.exp(-x/l))

if __name__ =="__main__":
    main()
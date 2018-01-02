import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from os.path import join

def main():
    path = "/home/lukas/documents/thesis/result_vasp/cleave/TiN/12sheets_2/plane_1/"
    path_open = join(path,"e_cleave.dat")
    with open(path_open,"r") as file:
        data = list(file)

    e_dif = []
    e_cleave = []
    x = []

    for line in data:
        if "#" not in line:
            line_split = line.split()
            x.append(float(line_split[0]))
            e_cleave.append(float(line_split[1]))
            e_dif.append(float(line_split[2]))
    fit = curve_fit(E_x, x, e_dif)
    e_c = fit[0][0]
    l = fit[0][1]
    print(fit)
    x_plt = np.linspace(0,5,100)
    y_plt =  E_x(x_plt,e_c,l)
    d_y = []
    d_y_x = []
    for i in range(1,len(y_plt)):
        d_y.append((y_plt[i]-y_plt[i-1])/(y_plt[i]-x_plt[i-1]))
        d_y_x.append((y_plt[i]+x_plt[i-1])/2)


    E_crit = E_x(l,e_c,l)
    E_cleave = [e_c] * 100
    L_crit = [l] * len(e_dif)
    s_c = e_c/(l*np.e)


    path_save = join(path,"fit.dat")
    with open(path_save,"w") as file:
        file.write("# Results of the fit\n")
        file.write("Cleave energy   = {:6.4f} []\n".format(e_c))
        file.write("Critical length = {:6.4f} []\n".format(l))
        file.write("Critical stress = {:6.4f} []\n".format(s_c))
    print("Ecleave: {}".format(e_c))
    print("lcrit: {}".format(l))
    print("Scrit: {}".format(e_c/(l*np.e)))



    # Plot

    lw = 1
    fig, ax = plt.subplots()
    ax.plot(L_crit,e_dif,"--k",linewidth = lw)

    ax.plot(x_plt,y_plt,"-k", linewidth = lw,label = "Fit")
    ax.plot(x,e_dif,"+k",label = "DFT")

    #plt.plot(l,E_crit,"+r", label = "E")
    plt.title(r"E$_{\mathrm{cleave}}$ (1$\bar{1}$0) TiN")
    ax.legend()
    ax.set_xlabel(r"Gap Distance [$\AA$]")
    ax.set_ylabel(r"E$_{\mathrm{Strain}}$ [eV/$\AA²$]")
    ax.text(l+0.1*l,0.83*max(e_dif),r"l$_{\mathrm{crit}}$"+" = {}".format(np.around(l,3)))
#    ax.set_xticks(list(ax.get_xticks()) + extraticks)
    ax.set_xlim([0,max(x_plt)*1.05])
    ax.set_ylim([0,max(e_dif)*1.05])
    ax.grid(linestyle = "--")
#    ax1 = ax.twinx()
#   ax1.plot(d_y_x, d_y)
    plt.savefig("/home/lukas/documents/thesis/presentation/group_21_12_17/fit1.png")
    plt.show()
    plt.close()



def E_x(x,E_c,l):
    return E_c*(1-(1+x/l)*np.exp(-x/l))

if __name__ =="__main__":
    main()
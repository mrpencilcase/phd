import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from os.path import join

def main():
    path = "/home/lukas/documents/thesis/result_vasp/cleave/TiN/16sheets/1/"
    path = "/home/lukas/documents/thesis/result_vasp/cleave/TiN/12sheets_2/plane_1/"
    path = "/home/lukas/documents/thesis/result_vasp/cleave/afCrN_TiN_1-10/plane_6/"
    path_open = join(path,"e_cleave.dat")
    with open(path_open,"r") as file:
        data = list(file)

    e_dif = []
    e_cleave = []
    x = []
    scale_unit = 16.0218/2
    for line in data:
        if "#" not in line:
            line_split = line.split()
            x.append(float(line_split[0]))
            e_cleave.append(float(line_split[1]))
            e_dif.append(float(line_split[2]))
    fit = curve_fit(E_x, x, e_dif)
    e_c = fit[0][0]*scale_unit
    l = fit[0][1]
    print(fit)
    x_plt = np.linspace(0,5,100)
    y_plt =  E_x(x_plt,e_c,l)
    d_y = []
    d_y_x = []
    for i in range(1,len(y_plt)):
        d_y.append((y_plt[i]-y_plt[i-1])/(x_plt[i]-x_plt[i-1]))
        d_y_x.append((x_plt[i]+x_plt[i-1])/2)


    E_crit = E_x(l,e_c,l)
    E_cleave = [e_c] * 100
    L_crit = [l] * len(e_dif)
    s_c = e_c/(l*np.e)
    e_dif_plot = [i* scale_unit for i in e_dif]





    path_save = join(path,"fit.dat")
    with open(path_save,"w") as file:
        file.write("# Results of the fit\n")
        file.write("Cleave energy   = {:6.4f} [J/m²]\n".format(e_c))
        file.write("Critical length = {:6.4f} [ang]\n".format(l))
        file.write("Critical stress = {:6.4f} [GPa]\n".format(s_c))
    print("Ecleave: {}".format(e_c))
    print("lcrit: {}".format(l))
    print("Scrit: {}".format(e_c/(l*np.e)))


    # Plot
    lw = 1
    fig, ax = plt.subplots()
    ax.plot(L_crit,e_dif_plot,"--k",linewidth = lw)
    lns2 = ax.plot(x,e_dif_plot,"+k",label = r"$E_x$ DFT")
    lns1 = ax.plot(x_plt,y_plt,"-k", linewidth = lw,label = r"$E_x$ fit")

    #plt.plot(l,E_crit,"+r", label = "E")
    plt.title(r"E$_{\mathrm{cleave}}$ (1$\bar{1}$0) TiN (12 sheets)")
    ax.set_xlabel(r"Gap Distance [$\AA$]")
    ax.set_ylabel(r"E$_{\mathrm{Strain}}$ [$J/m²$]")
    ax.text(l+0.1*l,0.83*max(e_dif),r"l$_{\mathrm{crit}}$"+" = {}".format(np.around(l,3)))
#    ax.set_xticks(list(ax.get_xticks()) + extraticks)
    ax.set_xlim([0,max(x_plt)*1.05])
    ax.set_ylim([0,max(e_dif_plot)*1.05])
    ax.grid(linestyle = "--")
    ax1 = ax.twinx()
    lns3 = ax1.plot(d_y_x, d_y,"-.k",linewidth = lw, label = r"$\sigma_{x}$")
    ax1.set_ylabel(r"$\sigma$ [GPa]")
    lns4 = ax1.plot(l,s_c,"ok", label = r"$\sigma_{\mathrm{crit}}$")
    lns = lns2 + lns1 + lns3 +lns4
    labs = [l.get_label() for l in lns]
    leg = ax.legend(lns, labs,bbox_to_anchor=(1,0.35))
    leg.get_frame().set_alpha(1)
    plt.savefig(join(path,"fit.pdf"))
    plt.show()
    plt.close()



def E_x(x,E_c,l):
    return E_c*(1-(1+x/l)*np.exp(-x/l))

if __name__ =="__main__":
    main()
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from os.path import join

V = [76333, 76691, 77072, 77485, 77901, 78307, 78703, 79091]
T = [0, 200.3 ,400.3, 601.6, 799.7, 1000.7, 1200.5, 1398]
V_s = [23.6, 12.1, 19.7, 16.6, 26.5, 21.5, 30.7, 24.8]


V = [ 76691, 77072, 77485, 77901, 78307, 78703, 79091]
T = [ 200.3 ,400.3, 601.6, 799.7, 1000.7, 1200.5, 1398]
V_s = [12.1, 19.7, 16.6, 26.5, 21.5, 30.7, 24.8]



a_lin_lit = 8.9/1000000
a_v_lit = 3*a_lin_lit


p_fit = np.polyfit(T,V,1)
print(a_v_lit)
print(p_fit[0]/min(V))
x_calc = np.linspace(0,max(T)-min(T),100)

x = np.linspace(min(T),max(T),100)
print(min(V))
V_lit = min(V)+ a_v_lit*x_calc *min(V)
V_fit = p_fit[1] + p_fit[0]*x


# Plot
lw = 1
fig = plt.figure()
ax = fig.add_subplot(111)
ax.errorbar(T,V,yerr=V_s,fmt="-+k",linewidth = lw,label = "Molecular Dynamics")
ax.plot(x,V_fit,"-r",linewidth = lw,label = "Fit")
ax.plot(x,V_lit,"-g",linewidth = lw,label = "Literature")
ax.set_ylabel(r"Volume ($\AA³$)")
ax.set_xlabel("Temperature (K)")
plt.legend()
plt.show()
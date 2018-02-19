import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from os.path import join




V = [ 76701, 77103, 77474, 77904, 78313]
T = [ 200 ,400, 600, 800, 1000]

V = [76337, 76701, 77103, 77474, 77904, 78313]
T = [0, 200 ,400, 600, 800, 1000]
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
ax.plot(T,V,"-+k",linewidth = lw,label = "Molecular Dynamics")
ax.plot(x,V_fit,"-r",linewidth = lw,label = "Fit")
ax.plot(x,V_lit,"-g",linewidth = lw,label = "Literature")
ax.set_ylabel("Volume")
ax.set_xlabel("Temperature [K]")
ax.text(400, 77474, "test text")
plt.legend()
plt.show()
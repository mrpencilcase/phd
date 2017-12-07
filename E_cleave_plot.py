import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

path_open = ""
e_relaxed = 3
n_at = 3
x = []
e_cleave = []

with open(path_open,"r") as file:
    data = list(file)



lw = 1
y_lable1 = "label 1"
y_lable2 = "label 2"
Ec_bulk1 = 1
Ec_bulk2 = 2
fig, ax1 = plt.subplots()
fig.set_size_inches(12, 5, forward=True)
ax1.plot(x,E_cleave,"+-k",mfc='none',linewidth = lw)
ax1.xaxis.grid(linestyle="--")
ax1.set_xticks(x)
ax1.xaxis.tick_top()
ax1.set_ylabel(ylable1)

ax2 = ax1.twinx()
ax2.plot(x,d1,"o-r",mfc='none',linewidth = lw)
ax2.plot(x,d2,"o-b",mfc='none',linewidth = lw)
ax2.set_ylabel(ylable2)
plt.show()

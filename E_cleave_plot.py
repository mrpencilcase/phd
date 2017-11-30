import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


E_cleave = 10*np.random.random_sample(11)+10
d1 = 1*np.random.random_sample(11)+1
d2 = 1*np.random.random_sample(11)+1
x =  []
x.extend(range(-5,6))

lw = 1
ylable1 = "label 1"
ylable2 = "label 2"

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

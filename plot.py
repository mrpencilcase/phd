import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




E_mod = [58,59,60]
E_mot_lit_ex = [64, 58]
E_mod_lit_ab = [63, 62]

Emods = [E_mod,E_mot_lit_ex,E_mod_lit_ab]
fig, ax = plt.subplots()

i = 1
for y in Emods:
    x = [i] * len(y)
    ax.scatter(x,y)
    i += 1

plt.show()
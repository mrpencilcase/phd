import os
import numpy as np

a = np.array([[4.25528], [0], [0]])
b = np.array([[0], [4.25528], [0]])
c = np.array([[0], [0], [4.25528]])

a_orth = [np.linalg.norm(a + b), 0, 0]
b_orth = [0, np.linalg.norm((a - b) / 2), 0]
c_orth = [0, 0, c[2][0]]


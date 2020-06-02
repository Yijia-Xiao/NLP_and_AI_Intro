from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)

X = list()
Y = list()
Z = list()

ax.set_xlabel('Emit exp()')
ax.set_ylabel('Freq exp()')
ax.set_zlabel('Line Correct')
# ax.set_zlabel('Char Correct')

with open('400_250_100.txt', 'r') as f:
    for l in f.readlines():
        X.append(int(l.split()[0]))
        Y.append(int(l.split()[1]))
        Z.append(float(l.split()[2]))
        # Z.append(float(l.split()[3]))

Z_val = set(Z)
print(Z_val)


X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)

ax.scatter(X, Y, Z)

# 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

plt.show()
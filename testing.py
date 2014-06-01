import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import re
import time
import datetime





T = np.arange(0., 40., 1.)

GER1 = 1/(1330.1 - 116.19*T + 2.6256*T**2)
GER2 = 1/(133.01 - 116.19*T + 2.6256*T**2)

INC1 = 1/(24*(45.1 - 3.45*T + 0.073*T**2))
INC2 = 1/(24*(59.9 - 4.55*T + 0.095*T**2))

p1, = plt.plot(T, GER1, 'r--')
p2, = plt.plot(T, GER2, 'b--')

plt.axvline(x=10, ymin=0, ymax=1, hold=None)
plt.axvline(x=30, ymin=0, ymax=1, hold=None)


plt.legend([p1, p2], ["INC'(T)", "INC''(T)"])
plt.show()

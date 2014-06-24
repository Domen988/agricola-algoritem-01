import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import re
import time
import datetime


import matplotlib
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
rect1 = matplotlib.patches.Rectangle((-200,-100), 400, 200, color='yellow')
rect2 = matplotlib.patches.Rectangle((0,150), 300, 20, color='red')
rect3 = matplotlib.patches.Rectangle((-300,-50), 40, 200, color='#0099FF')
circle1 = matplotlib.patches.Circle((-200,-250), radius=90, color='#EB70AA')
ax.add_patch(rect1)
ax.add_patch(rect2)
ax.add_patch(rect3)
ax.add_patch(circle1)
plt.xlim([-400, 400])
plt.ylim([-400, 400])
plt.show()


T = np.arange(5, 20, 0.01)

GER1 = 1/(1330.1 - 116.19*T + 2.6256*T**2)
GER2 = 1/(133.01 - 116.19*T + 2.6256*T**2)
rel = np.exp((-1.022 + 19.634)/T)

INC1 = 1/(24*(45.1 - 3.45*T + 0.073*T**2))
INC2 = 1/(24*(59.9 - 4.55*T + 0.095*T**2))

p1, = plt.plot(T, GER1, 'r--')
p2, = plt.plot(T, GER2, 'b--')

plt.axvline(x=10, ymin=0, ymax=1, hold=None)
plt.axvline(x=30, ymin=0, ymax=1, hold=None)


plt.legend([p1, p2], ["INC'(T)", "INC''(T)"])
plt.show()

plt.plot(T, rel)
plt.show()

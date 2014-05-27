import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import re
import time
import datetime
import ReadWrite as RW

# folder izvajanega skripta
scriptLokacija = (os.path.dirname(os.path.abspath(__file__)))

RHLokacija = scriptLokacija + '\Novo mesto RH   2013-01-01 - 2013-07-31.txt'
TLokacija = scriptLokacija + '\Novo mesto T   2013-01-01 - 2013-07-31.txt'
RLokacija = scriptLokacija + '\Novo mesto R   2013-01-01 - 2013-07-31.txt'

# inputi za program
RH, R, T, time = RW.readInput(RHLokacija, TLokacija, RLokacija)

i = 0
while i < len(time):

    #zacel bomo kar z MMO in racunanjem od tu naprej. DOY se upo?steva ?ze z seznamom vrednosti.

    # MMO
    SVP = []
    VPD = []
    SVP[i] = 610.7 * 10**( 7.5*T[i] / (237.3 + T[i]) )    # saturated vapour pressure
    VPD[i] = (1 - (RH[i]/100))*SVP[i]                     # vapour pressure deficit
    if R[i] > 0. or VPD[i] <= 4.5:
        M[i] = 1
    else:
        M[i] = 0

    HT[i] = 0.
    while k <= i:
        if T[k] > 0.:
            HT[i] = HT[i] + M[k]/(1330.1 - 116.19*T[k] + 2.6256*T[k]**2) 







pltRH = plt.figure('RH - relative humiditiy')
plt.plot(time, RH)
pltR = plt.figure('R - rainfall')
plt.plot(time, R)
pltT = plt.figure('T - temperature')
plt.plot(time, T)
plt.show()

'''
T = np.arange(0., 40., 1.)

INC1 = 1/(24*(45.1 - 3.45*T + 0.073*T**2))
INC2 = 1/(24*(59.9 - 4.55*T + 0.095*T**2))

p1, = plt.plot(T, INC1, 'r--')
p2, = plt.plot(T, INC2, 'b--')

plt.axvline(x=10, ymin=0, ymax=1, hold=None)
plt.axvline(x=30, ymin=0, ymax=1, hold=None)


plt.legend([p1, p2], ["INC'(T)", "INC''(T)"])
plt.show()
'''


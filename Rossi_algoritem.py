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

h = 0
MMO = []          # morphologically mature oospores
SVP = []          # saturated vapour pressure
VPD = []          # vapour pressure deficit
DOR = []          # progress of dormancy breaking
PMO = []          # physiologically mature oospores


while h < len(time):                                      # iteracija po urah

    #zacel bomo kar z MMO=1 in racunanjem od tu naprej. SOD in DOY se uposteva ze s seznamom vrednosti.

    MMO[h] = 1


    SVP[h] = 610.7 * 10**( 7.5*T[h] / (237.3 + T[h]) )   
    VPD[h] = (1 - (RH[h]/100))*SVP[h]                    
    if R[h] > 0. or VPD[h] <= 4.5:
        M[h] = 1
    else:
        M[h] = 0

    HT[h] = 0.
    while k <= h:
        if T[k] > 0.:
            HT[h] = HT[h] + M[k]/(1330.1 - 116.19*T[k] + 2.6256*T[k]**2) 

    DOR[h] =  exp(-15.891 * exp(-0.653*(HT[h] + 1)))                                       

    if HT[h] >= 1.3 and HT[h] <= 8.6:
        PMO[h] = MMO[h] * DOR[h]







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


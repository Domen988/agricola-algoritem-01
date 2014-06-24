import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.patches as pt
import os
import re
import time
import datetime
import random

import ReadWrite as RW
import cohort


# folder izvajanega skripta
scriptLokacija = (os.path.dirname(os.path.abspath(__file__)))

RHLokacija = scriptLokacija + '\Novo mesto RH   2013-01-01 - 2013-07-31.txt'
TLokacija = scriptLokacija + '\Novo mesto T   2013-01-01 - 2013-07-31.txt'
RLokacija = scriptLokacija + '\Novo mesto R   2013-01-01 - 2013-07-31.txt'

# inputi za program
RH, R, T, time = RW.readInput(RHLokacija, TLokacija, RLokacija)

# ad hoc leaf wetness ocena:
W = [None for i in range(len(time))]
i = 0
wCount = 0

while i < len(time):
    W[i] = 0
    if R[i] > 0.1 or RH[i] > 95:                             # list je moker, ko pade nekaj dezja ali je zrancna vlaga vecja od x
        W[i] = 1
        wCount = 5                            # simulira susenje lista v x urah
    elif R[i] <= 0.1 and wCount != 0:
        W[i] = 1
        wCount -= 1
    i += 1
    

h = 0
MMO = [None for i in range(len(time))]          # morphologically mature oospores
SVP = [None for i in range(len(time))]          # saturated vapour pressure
VPD = [None for i in range(len(time))]          # vapour pressure deficit
DOR = [None for i in range(len(time))]          # progress of dormancy breaking
PMO = [None for i in range(len(time))]          # physiologically mature oospores
M = [None for i in range(len(time))]            # moisture of the leaf filter
HT = [None for i in range(len(time))]           # hydro-thermal time
ltCohorts = []                                  # a list of cohorts


germinationList = []
germination = False
leafLitterMoisture = []
HTsum = 0

while h < len(time):                                      # iteracija po urah

    MMO[h] = 1                                                #zacel bomo kar z MMO=1 in racunanjem od tu naprej. SOD in DOY se uposteva ze s seznamom vrednosti.

    SVP[h] = 610.7 * 10**( 7.5*T[h] / (237.3 + T[h]) )   
    VPD[h] = (1 - (RH[h]/100))*SVP[h]                                      # VPD

    if R[h] > 0. or VPD[h] <= 4500:
        M[h] = 1                                                           # moisture of the leaf litter
    else:
        M[h] = 0
 
    if HTsum < 8.6:
        if T[h] > 0.:
            HTsum = HTsum + M[h]/(1330.1 - 116.19*T[h] + 2.6256*T[h]**2)
    HT[h] = HTsum                                                         # Hydro-thermal time

    DOR[h] =  np.exp(-15.891 * np.exp(-0.653*(HT[h] + 1)))                # progress of dormancy breaking                       
    
    if HT[h] >= 1.3 and HT[h] <= 8.6:                                      # primary inoculum season meje
        PMO[h] = MMO[h] * DOR[h]                                           # PMO - physiologically mature oospores

        if R[h] >= 0.2 and germination == False:
            germination = True
            ltCohorts.append(cohort.Cohort(h))                             # doda novo kohorto
            ltCohorts[-1].GERstart = h
    if W[h] == 0:                                                          # interrups oospores germination cohort creation event 
        germination = False

    if T[h] > 0. and cohort.Cohort.cohCount:                               # level of germination of current cohort
        for i in range(cohort.Cohort.cohCount):
            if ltCohorts[i].GER < 1:
                ltCohorts[i].set_GER(ltCohorts[i].GER + M[h]/(1330.1 - 116.19*T[h] + 2.6256*T[h]**2))
            if ltCohorts[i].GER >= 1 and ltCohorts[i].fi == 0:                   
                ltCohorts[i].fi = h
                ltCohorts[i].GEO = PMO[h]
                ltCohorts[i].GEOstage = True

# from here on we treat each cohort separately
    cohI = 0
    while cohI < cohort.Cohort.cohCount :

        if ltCohorts[cohI].GEOstage == True:
            ltCohorts[cohI].SUS = ltCohorts[cohI].SUS + (1 / (24*(5.67 - 0.47*(T[h]*(1 - RH[h]/100)) + 0.01*(T[h]*(1 - RH[h]/100))**2)))

            ltCohorts[cohI].WD = ltCohorts[cohI].WD + W[h]                         # wetness duration. Sumation starts with end of germination
            ltCohorts[cohI].Tsum = ltCohorts[cohI].Tsum + T[h]

            if ltCohorts[cohI].WD != 0:
                ltCohorts[cohI].TWD = ltCohorts[cohI].Tsum/ltCohorts[cohI].WD      # average T of the wet period
        
                if ltCohorts[cohI].TWD > 0:
                    if ltCohorts[cohI].WD >= np.exp((-1.022 + 19.634)/ltCohorts[cohI].TWD) and ltCohorts[cohI].ro == 0:
                        ltCohorts[cohI].REL = 1
                        ltCohorts[cohI].ro = h
                        ltCohorts[cohI].ZRE = ltCohorts[cohI].GEO
            if ltCohorts[cohI].REL == 1 and ltCohorts[cohI].SUS <= 1:
                if ltCohorts[cohI].GEOstage == True and ltCohorts[cohI].ZREstage == False:
                    ltCohorts[cohI].ZREstage = True

        if ltCohorts[cohI].ZREstage == True and ltCohorts[cohI].ZDIstage == False:
            SUZdenominator = 0
            for i in range (ltCohorts[cohI].ro, h+1):
                SUZdenominator = SUZdenominator + W[h]
            if SUZdenominator != 0:
                ltCohorts[cohI].SUZ = (h - ltCohorts[cohI].ro + 1)/SUZdenominator

            else:
                ltCohorts[cohI].SUZ = 0

            if R[h] >= 0.2:
                ltCohorts[cohI].delta = h
                ltCohorts[cohI].ZDI = ltCohorts[cohI].ZRE

            if ltCohorts[cohI].SUZ <= 1 and R[h] >= 0.2:
                ltCohorts[cohI].ZDIstage = True

        if ltCohorts[cohI].ZDIstage == True and ltCohorts[cohI].ZINstage == False:

            if h >= ltCohorts[cohI].delta:
                ltCohorts[cohI].WDZIN = ltCohorts[cohI].WDZIN + W[h]
                ltCohorts[cohI].TsumZIN = ltCohorts[cohI].TsumZIN + T[h]

            if ltCohorts[cohI].WDZIN != 0:
                ltCohorts[cohI].TWDZIN = ltCohorts[cohI].TsumZIN/ltCohorts[cohI].WDZIN

            if ltCohorts[cohI].WDZIN*ltCohorts[cohI].TWDZIN >= 60:
                ltCohorts[cohI].alfa = h
                ltCohorts[cohI].ZINstage = True                                     # Zoospores causing infection

        if ltCohorts[cohI].ZINstage == True:# and ltCohorts[cohI].OSLstage == False:
            ltCohorts[cohI].INC1 = ltCohorts[cohI].INC1 + 1/(24* (45.1 - 3.45*T[h] + 0.073*T[h]**2))
            ltCohorts[cohI].INC2 = ltCohorts[cohI].INC2 + 1/(24* (59.9 - 4.55*T[h] + 0.095*T[h]**2))

            if ltCohorts[cohI].INC1 >= 1 and ltCohorts[cohI].tau1 == 0:
                ltCohorts[cohI].tau1 = h
                ltCohorts[cohI].OSLstage = True

            if ltCohorts[cohI].INC2 >= 1 and ltCohorts[cohI].tau2 == 0:
                ltCohorts[cohI].tau2 = h

        cohI += 1

    print(time[h])
    h += 1

    



"""
pltRH = plt.figure('RH - relative humiditiy')
plt.plot(time, RH)
pltR = plt.figure('R - rainfall')
plt.plot(time, R)
pltT = plt.figure('T - temperature')
"""
#plt.plot(time, T)

fig = plt.figure('testni graf')
ax = fig.add_subplot(111)



rect = pt.Rectangle((time[ltCohorts[12].tau1],1), (ltCohorts[13].tau2-ltCohorts[13].tau1)/24, 0.1, color='yellow')
#ax.add_patch(rect1)
#plt.show()

#plt.axhspan(ymin=1, ymax=2, xmin=time[ltCohorts[13].tau1], xmax=time[ltCohorts[13].tau2])#, hold=None, **kwargs)

#plt.plot(time, DOR)
#ppl.plot(time, germinationList, 'g', time, M, 'y', time, W) #time, HT

colors = cm.rainbow(np.linspace(0, 1, cohort.Cohort.cohCount))
for i in range(0, cohort.Cohort.cohCount): #zip((0, cohort.Cohort.cohCount), colors):
    x = []
    y = []
    xZRE = []
    yZRE = []
    xZDI = []
    yZDI = []
    xZIN = []
    yZIN = []
    xOSL = []
    yOSL = []
    c = random.choice(colors)
    
    plt.annotate(str(i+1), xy=(time[ltCohorts[i].GERstart], -0.07))
    if i == 0:
        plt.annotate('# of cohorts = ' + str(cohort.Cohort.cohCount), xy=(time[ltCohorts[i].GERstart], -0.16), size='large')
                                                 

    for j in range(len(ltCohorts[i].GERhistory)):
        x.append(time[ltCohorts[i].GERstart + j])
        y.append(ltCohorts[i].GERhistory[j])

    if ltCohorts[i].ZREstage == True:
        xZRE.append(time[ltCohorts[i].GERstart + len(ltCohorts[i].GERhistory)])
        yZRE.append(1.08)
    if  ltCohorts[i].ZDIstage == True:
        xZDI.append(time[ltCohorts[i].GERstart + len(ltCohorts[i].GERhistory)])
        yZDI.append(1.16)
    if ltCohorts[i].ZINstage == True:
        xZIN.append(time[ltCohorts[i].GERstart + len(ltCohorts[i].GERhistory)])
        yZIN.append(1.24)
        xZIN.append(time[ltCohorts[i].alfa])
        yZIN.append(1.5)
    if ltCohorts[i].OSLstage == True:
        #xOSL.append(time[ltCohorts[i].GERstart + len(ltCohorts[i].GERhistory)])
        rect = pt.Rectangle((time[ltCohorts[i].tau1],1.3), (ltCohorts[i].tau2-ltCohorts[i].tau1)/24, 0.06, edgecolor=c, fill=False)
        ax.add_patch(rect)
        #xOSL.append(time[ltCohorts[i].tau1])
        #yOSL.append(1.32)
    
    plt.scatter(x,y, s=40, marker='o', color=c)                                             #http://blog.olgabotvinnik.com/post/58941062205/prettyplotlib-painlessly-create-beautiful-matplotlib
    plt.scatter(xZRE, yZRE, s=100, marker='o', color=c)
    plt.scatter(xZDI, yZDI, s=100, marker='d', color=c)
    plt.scatter(xZIN, yZIN, s=100, marker='v', color=c)
    plt.scatter(xOSL, yOSL, s=100, marker='s', color=c)
    
plt.show()
print('fin')
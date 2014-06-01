import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import re
import time
import datetime
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
    if R[i] > 0.1:
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
ltCohorts = []                                # a list of cohorts




cohortGER = []
germinationList = []
germination = False
leafLitterMoisture = []
HTsum = 0
while h < len(time):                                      # iteracija po urah

    #zacel bomo kar z MMO=1 in racunanjem od tu naprej. SOD in DOY se uposteva ze s seznamom vrednosti.

    MMO[h] = 1


    SVP[h] = 610.7 * 10**( 7.5*T[h] / (237.3 + T[h]) )   
    VPD[h] = (1 - (RH[h]/100))*SVP[h]                                      # VPD

    if R[h] > 0. or VPD[h] <= 4500:
        M[h] = 1
    else:
        M[h] = 0
 
    if T[h] > 0.:
        HTsum = HTsum + M[h]/(1330.1 - 116.19*T[h] + 2.6256*T[h]**2)
    HT[h] = HTsum
  
    DOR[h] =  np.exp(-15.891 * np.exp(-0.653*(HT[h] + 1)))                                       
    
    
    if HT[h] >= 1.3 and HT[h] <= 8.6:                                      # primary inoculum season meje
        PMO[h] = MMO[h] * DOR[h]                                           # PMO

        if R[h] >= 0.2 and germination == False:
            germination = True
            ltCohorts.append(cohort.Cohort(h))
            ltCohorts[-1].GERstart = h
            cohortGER.append([])
    if W[h] == 0:
        germination = False
                                                                             ## testing
    if germination == True:                                                  ## testing
        germinationList.append(1)                                            ## testing
    else:                                                                    ## testing
        germinationList.append(0)                                            ## testing

    #if germination == True:
    if T[h] > 0. and len(ltCohorts):
        for i in range(len(ltCohorts)):
            if ltCohorts[i].GER < 1:
                transfer = ltCohorts[i].GER + M[h]/(1330.1 - 116.19*T[h] + 2.6256*T[h]**2)
                ltCohorts[i].set_GER(ltCohorts[i].GER + M[h]/(1330.1 - 116.19*T[h] + 2.6256*T[h]**2))
                cohortGER[i].append(ltCohorts[i].GER)

    if len(ltCohorts) and ltCohorts[-1].GER >= 1:                                     
        ltCohorts[-1].fi = h
        ltCohorts[-1].PMO = PMO[h]


    """
    cohI = 0
    while cohI < len(ltCohorts):
        ltCohorts[i].SUS = ltCohorts[i].SUS + 1 / (24*(5.67 - 0.47*(T[h]*(1 - RH[h]/100)) + 0.01*(T[h]*(1 - RH[h]/100))**2))
        if h > ltCohorts[i].fi:
            ltCohorts[i].WD = ltCohorts[i].WD + W[h]

        ltCohorts[i].Tsum = ltCohorts[i].Tsum + T[h]
        if ltCohorts[i].WD != 0:
            ltCohorts[i].TWD = ltCohorts[i].Tsum/ltCohorts[i].WD
        
            if ltCohorts[i].WD >= np.exp((-1.022 + 19.634)/ltCohorts[i].TWD):
                ltCohorts[i].REL = 1
                ltCohorts[i].ro = h

        if ltCohorts[i].SUS <= 1 and ltCohorts[i].REL == 1:
            ltCohorts[i].ZREstage = True

        if ltCohorts[i].ZREstage == True:
            i = 0
            SUZnumerator = 0
            SUZdenominator = 0
            while i <= h:
                SUZnumerator = SUZnumerator + (h - ltCohorts[i].ro)
                i += 1
            i = 0
            for i in range (ltCohorts[i].ro + 1, h+1):
                SUZdenominator = SUZdenominator + W[h]
            
            SUZ = SUZnumerator/SUZdenominator

            if SUZ <= 1 and R[h] >= 0.2:
                ltCohorts[i].delta = h
                ltCohorts[i].ZDIstage = True

            if ltCohorts[i].ZDIstage == True:
                if ltCohorts[i].WD*ltCohorts[i].TWD >= 60:
                    ltCohorts[i].alfa = h
                    ltCohorts[i].ZINstage = True                                     # Zoospores causing infection

                if ltCohorts[i].ZINstage == True:
                    ltCohorts[i].INC1 = ltCohorts[i].INC1 + 1/(24* (45.1 - 3.45*T[h] + 0.073*T[h]**2))
                    ltCohorts[i].INC2 = ltCohorts[i].INC2 + 1/(24* (59.9 - 4.55*T[h] + 0.095*T[h]**2))

                    if ltCohorts[i].INC1 >= 1:
                        ltCohorts[i].tau = h
                        ltCohorts[i].OSLstage = True







        cohI += 1
        """
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


pltTest = plt.figure('testni graf')
plt.plot(time, HT, time, germinationList, 'g', time, M, 'y')
pltTest = plt.figure('germination, cohortGER')
for i in range(0, len(cohortGER)):
    plt.plot(ltCohorts[i].GERhistory, 'o')
for i in range(0, len(cohortGER)):
    plt.plot(cohortGER[i], )
plt.show()
print('fin')



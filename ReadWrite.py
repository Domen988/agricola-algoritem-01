import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import re
import time
import datetime

def readInput(RHLokacija, TLokacija, RLokacija):
    time = []
    RH = []
    with open(RHLokacija) as f:
        for line in f:
            words = line.split()
            minutes = int(words[1].split(':')[1])
            if (minutes != 30):
                year = int(words[0].split('-')[0])
                month = int(words[0].split('-')[1])
                day = int(words[0].split('-')[2])
                hour = int(words[1].split(':')[0])
                thisDate = datetime.date(year, month, day)
                thisTime = datetime.time(hour, minutes)
                thisDateTime = datetime.datetime.combine(thisDate, thisTime)
                time.append(thisDateTime)
                if (len(words) == 3):
                    RH.append(float(words[2]))
                else:
                    RH.append(0.)

    T = []
    try:
        with open(TLokacija) as f:
            for line in f:
                words = line.split()
                minutes = int(words[1].split(':')[1])
                if (minutes != 30):
                    if (len(words) == 3):
                        T.append(float(words[2]))
                    else:
                        T.append(0.)
    except:
        print('Check T file')
        exit()

    R = []
    halfHour = 0.
    try:
        with open(RLokacija) as f:
            for line in f:
                words = line.split()
                minutes = int(words[1].split(':')[1])
                if (len(words) == 3):
                    if (minutes != 30):
                        R.append(float(words[2]) + halfHour)
                    elif (minutes == 30):
                        halfHour = float(words[2])
                else:
                    if (minutes != 30):
                        R.append(0.)
    except:
        print('Check R file.')
        exit()
    return RH, R, T, time



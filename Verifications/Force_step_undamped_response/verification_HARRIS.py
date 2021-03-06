# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 18:50:24 2012

@author: snexus
"""
import matplotlib.pyplot as plt
import numpy as np
from math import *
t=np.linspace(0,10,1000)
Fc=3.0
k=16.0
wn=4.0
plt.figure()
plt.plot(t,Fc/k*(1-np.cos(wn*t)))
plt.xlabel('time [sec]')
plt.ylabel('Amplitude [m]')
plt.title("Force step function response")
plt.show()
'''
Created on Jan 21, 2012

@author: snexus
'''
import matplotlib.pyplot as plt
import numpy as np
from math import *
t=np.linspace(0,5,1000)
k=121.0
m=1.0

wn=sqrt(k/m)
# -------- Velocity Step Function
udot_c=1.0
x=udot_c/wn*(wn*t-np.sin(wn*t))
plt.figure()
plt.plot(t,x)
plt.xlabel('time [sec]')
plt.ylabel('Amplitude [m]')
plt.title("Velocty step function response")
plt.grid(True)
# -------- Velocity Step Function
u2dot_c=1.0
x_u2dot=u2dot_c/(wn**2)*((wn**2)*(t**2)/2-(1-np.cos(wn*t)))
plt.figure()
plt.plot(t,x_u2dot)
plt.xlabel('time [sec]')
plt.ylabel('Amplitude [m]')
plt.title("Acceleration step function response")
plt.grid(True)

# -------- Pulse Response -------------
tau=0.01
input_f=2
t1=np.linspace(0,tau,1000)
resp1=input_f*(1-np.cos(wn*t1))
t2=np.linspace(tau,tau*5,1000)
T_1=1/(wn/2/pi)
resp2=input_f*(2*sin(pi*tau/T_1))*np.sin(wn*(t2-tau/2))
plt.figure()
plt.plot(t1,resp1)
plt.plot(t2,resp2)
plt.grid(True)
plt.xlabel('time [sec]')
plt.ylabel('Amplitude [m]')
plt.title("Square displacement function response")

plt.show()
import numpy as np
import matplotlib.pyplot as plt
import math 

#initial conditions
k = 10
m = 5.97219e24
r = 6771e3
G = 6.6743 * 10**(-11)
dt = 100
n=600
T=2*math.pi/math.sqrt(G*m/r**3)

a_0 = 7660
x_0 = 0


def a(a_old, x_old):
    return a_old - (G * m / (r**3)) * x_old * dt

def x(a_old, x_old):
    return x_old + a_old*dt

a_old = a_0
x_old = x_0

closestVZero = 10e24
closestPos = 0
real_time = 0 
exp=[]
theo=[]
num=[]
peak_time = []
peak=[]
real_peak = []
peak_error=[]
linearized_error = []

#EXPERIMENTAL
for i in range(n):
    a_new = a(a_old, x_old)
    x_new = x(a_old, x_old)

    a_old = a_new
    x_old = x_new
    exp.append(x_old)
    if (abs(a_new) < closestVZero):
        closestVZero = abs(a_new)
        closestPos = x_new
    num.append(i*dt)
    print(i, "Velocity:", a_new, "Position:", x_new)

#plt.scatter(num, exp,c="red")

#THEORETICAL
an_x=0
for k in range(n):
    an_x=r*math.sin(math.sqrt(G*m/r**3)*k*dt)
  
    theo.append(an_x)
print(closestVZero,closestPos)

#plt.scatter(num,theo,c="blue")

#ERROR
error=abs(theo[-1]-exp[-1])


for i in range(20):
    peak.append(abs(exp[13+28*i]))
    peak_time.append((13+28*i)*dt)
    real_peak.append(theo[13+28*i])
    peak_error.append(abs(exp[13+28*i]-theo[13+28*i]))
    
    #PURPLE

#plt.scatter(peak_time,peak_error,c="purple")    

for i in range(len(peak)):
    linearized_error.append(math.log(peak[i], math.e))
    print("Peak time:", peak_time[i], "Peak:", linearized_error[i])

trendline = np.polyfit(peak_time,linearized_error,1)
print("Trendline:",trendline)

#GREEN
plt.scatter(peak_time,linearized_error,c="green")

plt.legend(["y=0.0063t"],loc="upper left")
plt.title("Linearized Error (timestep of 100s)")
plt.xlabel("Time (seconds)")
plt.ylabel("X-value (m)")
plt.show()

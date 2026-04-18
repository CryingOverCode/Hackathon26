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

error_trendlines = []

a_old = a_0
x_old = x_0

real_time = 0 
exp=[]
theo=[]
error=[]
peak_time = []
peak=[]
real_peak = []
peak_error=[]
linearized_error = []
varied_timesteps = [0.1,0.5,1,5,10,25,35,50,60,75,90,100,120,140,160,180]


for i in varied_timesteps:
    exp=[]
    theo=[]
    peak_time = []
    peak=[]
    real_peak = []
    peak_error=[]
    linearized_error = []
    def a(a_old, x_old):
        return a_old - (G * m / (r**3)) * x_old * i

    def x(a_old, x_old):
        return x_old + a_old*i 

    #EXPERIMENTAL
    for k in range(n):
        a_new = a(a_old, x_old)
        x_new = x(a_old, x_old)

        a_old = a_new
        x_old = x_new
        exp.append(x_old)
        print(i, "Velocity:", a_new, "Position:", x_new)


    #THEORETICAL
    an_x=0
    for k in range(n):
        an_x=r*math.sin(math.sqrt(G*m/r**3)*k*i)
        theo.append(an_x)
    """
    #ERROR            
    error.append(abs(theo[-1]-exp[-1]))
    theo=[]
    exp=[]
"""
    for k in range(20):
        peak.append(abs(exp[13+28*k]))
        peak_time.append(13+28*k)
        real_peak.append(theo[13+28*k])
        peak_error.append(abs(exp[13+28*k]-theo[13+28*k]))

    for k in range(len(peak)):
        linearized_error.append(math.log(peak[k], math.e))
        print("Peak time:", peak_time[k], "Peak:", linearized_error[k])

    trendline = np.polyfit(peak_time,linearized_error,1)
    error.append(trendline[0])
    print(trendline)

print("Error", error)
plt.scatter(varied_timesteps,error)
plt.title("Error Coefficients in Relation to Timesteps")
plt.ylabel("Error Coefficient")
plt.xlabel("Timestep(s)")
plt.legend(["Trendline: y=(1.9*10^-2)x"])
plt.show()
        
from eulerMethod import *
from numpy import *
import matplotlib.pyplot as plt

#initial conditions
k = 10
m = 5.97219e24
r = 6771e3
G = 6.6743 * 10**(-11)
dt = 100

a_0 = 7660
x_0 = 6771000


def a(a_old, x_old):
    return a_old - (G * m / (r**3)) * x_old * dt

def x(a_old, x_old):
    return x_old + a_old*dt

a_old = a_0
x_old = x_0

closestVZero = 10e24
closestPos = 0

for i in range(100):
    a_new = a(a_old, x_old)
    x_new = x(a_old, x_old)

    a_old = a_new
    x_old = x_new

    if (abs(a_new) < closestVZero):
        closestVZero = abs(a_new)
        closestPos = x_new
    plt.scatter(i, a_new)
    print("Velocity:", a_new, "Position:", x_new)
plt.show()
    
print(closestVZero,closestPos)
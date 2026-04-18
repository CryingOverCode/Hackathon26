from numpy.typing import NDArray
from typing import Callable

def eulerSolve(f: Callable, 
               initialCondition: NDArray,
               t: float,
               dt: float,
               *args 
               )-> NDArray:
    return f(t, initialCondition, *args) + f(t + dt, initialCondition, *args)*dt
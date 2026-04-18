import math

# Parameters
r = 400000
m = 5.97e24
G = 6.6743e-11

dt = 5


def next_pos(initial_conditions):
    # initial_conditions = [v_0, x_0, u_0, y_0]

    v_old = initial_conditions[0]
    x_old = initial_conditions[1]
    u_old = initial_conditions[2]
    y_old = initial_conditions[3]

    r = math.sqrt(x_old**2 + y_old**2)

    v_next = v_old - G*m/r**3 * x_old*dt
    u_next = u_old - G*m/r**3 * y_old*dt

    x_next = x_old + v_old * dt
    y_next = y_old + u_old * dt

    return [v_next, x_next, u_next, y_next, r]
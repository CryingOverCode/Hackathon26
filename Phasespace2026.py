import numpy as np
import matplotlib.pyplot as plt

g, L = 9.81, 1.0
w0sq = g / L

def euler(theta0, omega0, dt=0.01, n=123456):
    thetas = [theta0]
    omegas = [omega0]
    for _ in range(n):
        th = thetas[-1]
        om = omegas[-1]
        # Euler step: x_{n+1} = x_n + dt * f(x_n)
        th_next = th + dt * om
        om_next = om + dt * (-w0sq * np.sin(th))
        thetas.append(th_next)
        omegas.append(om_next)
    return np.array(thetas), np.array(omegas)

fig, ax = plt.subplots(figsize=(9, 6))
ax.set_xlabel("θ (rad)")
ax.set_ylabel("θ' (rad/s)")
ax.set_title("Pendulum Phase Space")
ax.set_xlim(-2 * np.pi, 2 * np.pi)
ax.set_ylim(-8, 8)


for theta0 in np.linspace(-3, 3, 3):
    for omega0 in np.linspace(-4, 4, 5):
        th, om = euler(theta0, omega0)
        ax.plot(th, om, color="blue", lw=0.8, alpha=0.7)
        
for theta0 in np.linspace(-3.0, 3.0, 6):
    for omega0 in np.linspace(-8, 8, 6):
        if abs(omega0) > 4:  
            th, om = euler(theta0, omega0)
            ax.plot(th, om, color="steelblue", lw=0.8, alpha=0.9)
'''     
bases  = [(0.5, 0.0), (1.5, 0.0), (2.5, 0.0), (0.5, 3.0), (1.0, 5.5)]
colors = ["blue", "green", "purple", "orange", "brown"]
n = 3000

for (th0, om0), color in zip(bases, colors):
    th, om = euler(th0, om0, n=n)
    ax.plot(th, om, color=color, lw=0.8, alpha=0.4) 
    ax.scatter(th[0],  om[0],  color=color, s=80, marker="o", zorder=5)  # start
    ax.scatter(th[-1], om[-1], color=color, s=80, marker="X", zorder=5)  # end

'''
def triangle_area(p1, p2, p3):
    # Shoelace formula
    return 0.5 * abs(
        (p2[0] - p1[0]) * (p3[1] - p1[1]) -
        (p3[0] - p1[0]) * (p2[1] - p1[1])
    )

# Draw Triangles
starts = [(0.5, 0.0), (1.0, 0.0), (0.75, 0.5)]
colors = ["blue", "green", "purple"]
n = 50

start_pts = []
end_pts   = []

for (th0, om0), color in zip(starts, colors):
    th, om = euler(th0, om0, n=n)
    ax.plot(th, om, color=color, lw=0.8, alpha=0.3)
    ax.scatter(th[0],  om[0],  color=color, s=80, marker="o", zorder=5)
    ax.scatter(th[-1], om[-1], color=color, s=80, marker="X", zorder=5)
    start_pts.append((th[0],  om[0]))
    end_pts.append(  (th[-1], om[-1]))

from matplotlib.patches import Polygon
tri_start = Polygon(start_pts, fill=True, facecolor="blue",   alpha=0.15, edgecolor="blue",   lw=1.5)
tri_end   = Polygon(end_pts,   fill=True, facecolor="red",    alpha=0.15, edgecolor="red",    lw=1.5)
ax.add_patch(tri_start)
ax.add_patch(tri_end)

area_before = triangle_area(*start_pts)
area_after  = triangle_area(*end_pts)

ax.text(-5.5, 8.5, f"Area before: {area_before:.4f}", fontsize=10, color="blue")
ax.text(-5.5, 7.5, f"Area after:  {area_after:.4f}",  fontsize=10, color="red")



plt.tight_layout()
plt.show()

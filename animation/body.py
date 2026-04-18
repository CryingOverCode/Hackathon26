import math
import pygame

G = 6.6743e-11

class Body():
    def __init__(self, parameters, initial_conditions, dt=0.1, trail=True, color="white"):
        self.params = parameters
        # Parameters: [m]

        self.init_cond = initial_conditions
        # Initial_conditions: [v_0, x_0, u_0, y_0]
        self.current_conditions = self.init_cond
        self.dt = dt

        self.i = 0
        self.trail = trail
        self.trail_points_x = []
        self.trail_points_y = []
        self.color = color

    def update_position(self, external_body, centered = False):
        # current_conditions = [v_old, x_old, u_old, y_old]
        v_old = self.current_conditions[0]
        x_old = self.current_conditions[1]
        u_old = self.current_conditions[2]
        y_old = self.current_conditions[3]

        x_external_body = external_body.current_conditions[1]
        y_external_body = external_body.current_conditions[3]

        dx = x_old-x_external_body
        dy = y_old-y_external_body

        m = external_body.params[0]

        r = math.sqrt(dx**2 + dy**2)

        v_next = v_old - G*m/r**3 * dx*self.dt
        u_next = u_old - G*m/r**3 * dy*self.dt

        x_next = x_old + v_old * self.dt
        y_next = y_old + u_old * self.dt

        if centered:
            self.current_conditions = self.current_conditions
        else:
            self.current_conditions = [v_next, x_next, u_next, y_next, r]

        if self.trail:
            self.i += 1
            if self.i % 7 == 0:
                self.trail_points_x.append(x_next)
                self.trail_points_y.append(y_next)

        return self.current_conditions

    def draw(self, screen, scaling):
        pygame.draw.circle(screen, self.color, (1280/2 + self.current_conditions[1]*scaling, 720/2 + self.current_conditions[3]*scaling), radius=max(self.params[0]**0.27*scaling,2))

        if self.trail:
            for i in range(len(self.trail_points_x)):
                pygame.draw.circle(screen, self.color, (1280/2 + self.trail_points_x[i]*scaling, 720/2 + self.trail_points_y[i]*scaling), 1)

    def reset(self):
        self.current_conditions = self.init_cond
        self.trail_points_x = []
        self.trail_points_y = []
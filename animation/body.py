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
    
    def update_position_3body_euler(self, body1, body2, centered = False):
        
        v_old = self.current_conditions[0]
        x_old = self.current_conditions[1]
        u_old = self.current_conditions[2]
        y_old = self.current_conditions[3]

        x_body1 = body1.current_conditions[1]
        y_body1 = body1.current_conditions[3]
        x_body2 = body2.current_conditions[1]
        y_body2 = body2.current_conditions[3]

        dx1 = x_old - x_body1
        dy1 = y_old - y_body1

        dx2 = x_old - x_body2
        dy2 = y_old - y_body2

        m_self = self.params[0]
        m_body1 = body1.params[0]
        m_body2 = body2.params[0]

        r_1 = math.sqrt(dx1**2 + dy1**2)
        r_2 = math.sqrt(dx2**2 + dy2**2)
        
        self_dv_x = (-G * m_body1  * dx1 / (r_1**3)) - (G * m_body2 * dx2 / (r_2**3)) 
        self_dv_y = (-G * m_body1  * dy1 / (r_1**3)) - (G * m_body2 * dy2 / (r_2**3)) 
        #ts was too confusing so i seperated the calculation for the derivative of v
        
        v_next = v_old + self_dv_x * self.dt
        u_next = u_old + self_dv_y * self.dt

        x_next = x_old + v_old * self.dt
        y_next = y_old + u_old * self.dt

        if centered:
            self.current_conditions = self.current_conditions
        else:
            self.current_conditions = [v_next, x_next, u_next, y_next, r_1, r_2]#wut is the implementation of this


        x_center_of_mass = (m_self*x_old + m_body1*body1.current_conditions[1] 
                            + m_body2*body2.current_conditions[1]) / (m_self + m_body1 + m_body2)
        y_center_of_mass = (m_self*y_old + m_body1*body1.current_conditions[3]
                            + m_body2*body2.current_conditions[3]) / (m_self + m_body1 + m_body2)
        self.center_of_mass = [x_center_of_mass, y_center_of_mass]
        
        if self.trail:
            self.i += 1

            self.trail_points_x.append(x_next)
            self.trail_points_y.append(y_next)

        return self.current_conditions


    def update_position(self, external_body, stationary = False, method="Euler"):
        # current_conditions = [v_old, x_old, u_old, y_old]
        v_old = self.current_conditions[0]
        x_old = self.current_conditions[1]
        u_old = self.current_conditions[2]
        y_old = self.current_conditions[3]

        x_external_body = external_body.current_conditions[1]
        y_external_body = external_body.current_conditions[3]

        dx = x_old-x_external_body
        dy = y_old-y_external_body

        m_self = self.params[0]
        m_ext = external_body.params[0]

        r = math.sqrt(dx**2 + dy**2)

        if method == "Euler":
            v_next = v_old - G*m_ext/r**3 * dx*self.dt
            u_next = u_old - G*m_ext/r**3 * dy*self.dt

            x_next = x_old + v_old * self.dt
            y_next = y_old + u_old * self.dt

        if stationary:
            self.current_conditions = self.current_conditions
        else:
            self.current_conditions = [v_next, x_next, u_next, y_next, r]

        # Center of mass of the system
        x_center_of_mass = (m_self*x_old + m_ext*external_body.current_conditions[1]) / (m_self + m_ext)
        y_center_of_mass = (m_self*y_old + m_ext*external_body.current_conditions[3]) / (m_self + m_ext)
        self.center_of_mass = [x_center_of_mass, y_center_of_mass]

        if self.trail:
            self.i += 1

            self.trail_points_x.append(x_next)
            self.trail_points_y.append(y_next)

        return self.current_conditions

    def draw(self, screen, scaling, offsets, highlight=False):
        if self.trail:
            if highlight:
                color = "white"
                size = 3
            else:
                color = self.color
                size = 1
            for i in range(len(self.trail_points_x)):
                pygame.draw.circle(screen, color, (1280/2 + self.trail_points_x[i]*scaling + offsets[0], 720/2 + self.trail_points_y[i]*scaling + offsets[1]), size)
            
        if highlight:
            pygame.draw.circle(
            screen, 
            "white", 
            (1280/2 + self.current_conditions[1]*scaling + offsets[0], 720/2 + self.current_conditions[3]*scaling + offsets[1]), 
            radius=max(self.params[0]**0.27*scaling*0.2,2) + 4
            )

        pygame.draw.circle(
            screen, 
            self.color, 
            (1280/2 + self.current_conditions[1]*scaling + offsets[0], 720/2 + self.current_conditions[3]*scaling + offsets[1]), 
            radius=max(self.params[0]**0.27*scaling*0.2,2
            ))

    def get_center_of_system(self):
        return self.center_of_mass

    def reset(self):
        self.current_conditions = self.init_cond
        self.trail_points_x = []
        self.trail_points_y = []

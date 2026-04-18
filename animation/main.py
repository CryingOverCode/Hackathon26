import pygame
from orbit import next_pos

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

center = (1280/2,720/2)
x_data_points = []
y_data_points = []


# Parameters
r = 6771000
m = 3.285e23
G = 6.6743e-11

scaling = 200/r

# Initial Conditions
initial_x = r
initial_v = 0
initial_y = 0
initial_u = 9000

x_old = initial_x
v_old = initial_v
y_old = initial_y
u_old = initial_u

old_pos = [v_old, x_old, u_old, y_old]

i = 0

while running:
    i+=1

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "blue", (1280/2,720/2), 637100*scaling)

    new_pos = next_pos(old_pos)
    
    x_data_points.append(new_pos[1])
    y_data_points.append(new_pos[3])

    for i in range(len(x_data_points)):
        pygame.draw.circle(screen, "grey", (1280/2 + x_data_points[i]*scaling, 720/2 + y_data_points[i]*scaling), 1)

    pygame.draw.circle(screen, "white", (1280/2 + new_pos[1]*scaling, 720/2 + new_pos[3]*scaling), 4)
    
    old_pos = new_pos

    print(new_pos[4])

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

pygame.quit()
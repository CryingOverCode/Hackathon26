import pygame
from body import Body

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
m_earth = 5.97219e23 * 1.6
G = 6.6743e-11

scaling = 200/r

# Initial Conditions
initial_x = r
initial_v = 0
initial_y = 2000000
initial_u = 1525

DT = 20

earth = Body(
    parameters=[m_earth],
    initial_conditions=[initial_v, initial_x, 0, initial_y],
    dt = DT,
    color = "red"
)

earth2 = Body(
    parameters=[m_earth],
    initial_conditions=[initial_v, -initial_x, 0, -initial_y],
    dt = DT,
    color = "green"
)

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", (1280/2,720/2), 2)

    earth.update_position(earth2)
    earth2.update_position(earth)

    earth.draw(screen, scaling)
    earth2.draw(screen, scaling)


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

pygame.quit()
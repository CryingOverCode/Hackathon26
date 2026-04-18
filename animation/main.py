import pygame
from body import Body
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

center = (1280/2,720/2)

# Parameters
r = 6771000
m_earth = 5.97219e23
G = 6.6743e-11

m_sattelite = 100

scaling = 300/r

# Initial Conditions
initial_x = r
initial_v = 0
initial_y = 0
initial_u = 2500

DT = 20

earth = Body(
    parameters=[m_earth],
    initial_conditions=[0, 0, 0, 0],
    dt = DT,
    color = (127, 222, 255)
)

satellite = Body(
    parameters=[m_sattelite],
    initial_conditions=[initial_v, initial_x, initial_u, initial_y],
    dt = DT,
    color = "white"
)

def reset_all():
    earth.reset()
    satellite.reset()

def display_graph_1():
    pass

reset_btn = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    10,  # X-coordinate of top left corner
    10,  # Y-coordinate of top left corner
    60,  # Width
    25,  # Height
    inactiveColour=(237, 28, 36),
    text="Reset",
    onClick=lambda: reset_all()
)
graph1_btn = Button(
    screen,  # Surface to place button on
    80,  # X-coordinate of top left corner
    10,  # Y-coordinate of top left corner
    70,  # Width
    25,  # Height
    inactiveColour=(241, 211, 2),
    text="Graph 1",
    onClick=lambda: display_graph_1()
)

zoom_slider = Slider(
    screen, 
    10, 
    45, 
    5, 
    500, 
    min=0, 
    max=600, 
    step=1, 
    valueColour=(35, 87, 137),
    handleColour=(255,255,255), 
    initial=300,
    handleRadius=5,
    vertical=True,
)

while running:
    screen.fill((2, 1, 0))
    scaling = zoom_slider.getValue()/r

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.circle(screen, "white", (1280/2,720/2), 2)

    earth.update_position(satellite)
    satellite.update_position(earth)

    earth.draw(screen, scaling)
    satellite.draw(screen, scaling)

    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    pygame.display.update()
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

pygame.quit()
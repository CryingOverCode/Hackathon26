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

WIDTH = 1280
HEIGHT = 720

center = (WIDTH/2,HEIGHT/2)

# Parameters
r = 54.6e5
m_earth = 5.97219e23
G = 6.6743e-11

m_sattelite = 100

scaling = 300/r

# Initial Conditions
initial_x = r
initial_v = 0
initial_y = 0
initial_u = 5000

DT = 55

planets = []
centering = False

current_system = 0

for i in range(10):
    earth = Body(
        parameters=[m_earth],
        initial_conditions=[initial_v, -initial_x, -initial_u, initial_y],
        dt = DT-i*5,
        color = (0,250-20*i,0)
    )

    random_planet = Body(
        parameters=[m_earth],
        initial_conditions=[initial_v, initial_x, initial_u, initial_y],
        dt = DT-i*5,
        color = (0,0,250-10*i)
    )

    planets.append(earth)
    planets.append(random_planet)

def reset_all():
    for planet in planets:
        planet.reset()

def display_graph_1():
    pass

def pause_simulation():
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

offsets=[0,0]


while running:
    screen.fill((2, 1, 0))
    scaling = zoom_slider.getValue()/r

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if current_system < len(planets)/2 - 1:
                    centering = True
                    current_system += 1
                elif current_system == len(planets)/2 - 1:
                    current_system = 0


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        offsets[0] += 10
    if keys[pygame.K_RIGHT]:
        offsets[0] -= 10
    if keys[pygame.K_DOWN]:
        offsets[1] -= 10
    if keys[pygame.K_UP]:
        offsets[1] += 10
    
    if keys[pygame.K_ESCAPE]:
        centering=False

    if centering:
        center_of_system = planets[current_system*2].get_center_of_system()
        offsets = [center_of_system[0]*-scaling, center_of_system[1]*-scaling]

    for i in range(0, len(planets), 2):
        earth = planets[i]
        random_planet = planets[i+1]

        earth.update_position(random_planet)
        random_planet.update_position(earth)

        if i/2 == current_system and centering:
            earth.draw(screen, scaling, offsets, highlight=True)
            random_planet.draw(screen, scaling, offsets, highlight=True)
        else:
            earth.draw(screen, scaling, offsets)
            random_planet.draw(screen, scaling, offsets)

    pygame.draw.circle(screen, "white", center, 2)

    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    pygame.display.update()
    pygame.display.flip()


    clock.tick(30)  # limits FPS to 60

pygame.quit()
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
initial_u = 1800

N = 10
DT = 5*N
time_steps = []

planets = []
center_cam = False

current_system = 0

# Generate Bodies
for i in range(N):
    time_step = DT-i*5
    earth = Body(
        parameters=[m_earth*10],
        initial_conditions=[initial_v, -initial_x, 0, initial_y],
        dt = time_step,
        color = (0,255/N*i,0)
    )

    random_planet = Body(
        parameters=[m_earth],
        initial_conditions=[initial_v, initial_x, initial_u, initial_y],
        dt = time_step,
        color = (0,0,255/N*i),
    )

    time_steps.append(time_step)
    planets.append(earth)
    planets.append(random_planet)

simulating = True
# Reset simulation
def reset_all():
    global simulating
    simulating = False
    for planet in planets:
        planet.reset()
        planet.dt = 0

# Start simulation if stopped
def start_simulation():
    global simulating
    simulating = True
    for i in range(len(time_steps)):
        planets[i].dt = time_steps[i]
    


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
start_btn = Button(
    screen,
    80,
    10,
    60,
    25,
    inactiveColour=(35,226,0),
    text="Start",
    onClick=lambda: start_simulation()
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

blue_x_speed_slider = Slider(
    screen, 
    WIDTH-20, 
    45, 
    5, 
    500, 
    min=-5000, 
    max=5000, 
    step=150, 
    valueColour="blue",
    handleColour=(255,255,255), 
    initial=initial_v,
    handleRadius=5,
    vertical=True,
)
blue_y_speed_slider = Slider(
    screen, 
    WIDTH-10, 
    45, 
    5, 
    500, 
    min=-5000, 
    max=5000, 
    step=150, 
    valueColour="blue",
    handleColour=(255,255,255), 
    initial=initial_u,
    handleRadius=5,
    vertical=True,
)
green_x_speed_slider = Slider(
    screen, 
    WIDTH-30, 
    45, 
    5, 
    500, 
    min=-5000, 
    max=5000, 
    step=150, 
    valueColour="green",
    handleColour=(255,255,255), 
    initial=initial_v,
    handleRadius=5,
    vertical=True,
)
green_y_speed_slider = Slider(
    screen, 
    WIDTH-40, 
    45, 
    5, 
    500, 
    min=-5000, 
    max=5000, 
    step=150, 
    valueColour="green",
    handleColour=(255,255,255), 
    initial=0,
    handleRadius=5,
    vertical=True,
)

offsets=[0,0]

while running:
    screen.fill((2, 1, 0))
    scaling = zoom_slider.getValue()/r

    if not simulating:
        for i in range(len(planets)):
            if i % 2 != 0:
                planets[i].current_conditions[0] = blue_x_speed_slider.getValue()
                planets[i].current_conditions[2] = blue_y_speed_slider.getValue()
            else:
                planets[i].current_conditions[0] = green_x_speed_slider.getValue()
                planets[i].current_conditions[2] = green_y_speed_slider.getValue()

        start_x = 1280/2 + planets[0].current_conditions[1]*scaling + offsets[0]
        start_y = 720/2 + planets[0].current_conditions[3]*scaling + offsets[1]
        end_x = start_x + planets[0].current_conditions[0] * scaling * 500
        end_y = start_y + planets[0].current_conditions[2] * scaling * 500

        pygame.draw.line(screen, "white", (start_x, start_y) , (end_x, end_y) , width=1)
        
        start_x = 1280/2 + planets[1].current_conditions[1]*scaling + offsets[0]
        start_y = 720/2 + planets[1].current_conditions[3]*scaling + offsets[1]
        end_x = start_x + planets[1].current_conditions[0] * scaling * 500
        end_y = start_y + planets[1].current_conditions[2]* scaling * 500

        pygame.draw.line(screen, "white", (start_x, start_y) , (end_x, end_y) , width=3)

        

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if current_system < len(planets)/2 - 1:
                    center_cam = True
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
        center_cam=False

    if center_cam:
        center_of_system = planets[current_system*2].get_center_of_system()
        offsets = [center_of_system[0]*-scaling, center_of_system[1]*-scaling]

    # Update and draw every planet
    for i in range(0, len(planets), 2):
        earth = planets[i]
        random_planet = planets[i+1]

        earth.update_position(random_planet)
        random_planet.update_position(earth)

        if i/2 == current_system and center_cam:
            earth.draw(screen, scaling, offsets, highlight=True)
            random_planet.draw(screen, scaling, offsets, highlight=True)
        else:
            earth.draw(screen, scaling, offsets)
            random_planet.draw(screen, scaling, offsets)

    pygame.draw.circle(screen, "red", center, 2)

    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    pygame.display.update()
    pygame.display.flip()


    clock.tick(30)  # limits FPS to 60

pygame.quit()
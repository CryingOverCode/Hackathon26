import pygame
from body import Body
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from matplotlib import pyplot
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
m_earth = 9.5e24
G = 6.67e-11

m_sattelite = 100

scaling = 300/r

# Initial Conditions
initial_x = r
initial_v = 0
initial_y = 0
initial_u = 5000

DT = 10

planets = []
centering = False

current_system = 0

body1x = []
body1y = []
body1vx = []
body1vy = []
body2x = []
body2y = []
body2vx = []
body2vy = []
body3x = []
body3y = []
body3vx = []
body3vy = []
t = []
counter = 0


earth1 = Body(
         # Initial_conditions: [v_0, x_0, u_0, y_0]
        parameters=[m_earth],
        initial_conditions=[0, 0, 0, 0], 
        dt = DT,
        color = (0,250,0) #green
    )
earth2 = Body(
        parameters=[m_earth],
        initial_conditions=[0,54.6e5, 1.49e4, 0],
        dt = DT,
        color = (250,0,0) #red
    )
earth3 = Body(
        parameters=[m_earth],
        initial_conditions=[0, -54.6e5, -1.49e4, 0],
        dt = DT,
        color = (0,0,250) #blue
    )

planets.append(earth1)
planets.append(earth2)
planets.append(earth3)


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

    #update position for three planets 
    body1 = planets[0]
    body2 = planets[1]
    body3 = planets[2]

    body1.update_position_3body_euler(body2, body3)
    body2.update_position_3body_euler(body1, body3)
    body3.update_position_3body_euler(body2, body1)

    body1x.append(body1.current_conditions[1])
    body1y.append(body1.current_conditions[3])
    body1vx.append(body1.current_conditions[0])
    body1vy.append(body1.current_conditions[2])
    body2x.append(body2.current_conditions[1])
    body2y.append(body2.current_conditions[3])
    body2vx.append(body2.current_conditions[0])
    body2vy.append(body1.current_conditions[2])
    body3x.append(body3.current_conditions[1])
    body3y.append(body3.current_conditions[3])
    body3vx.append(body3.current_conditions[0])
    body3vy.append(body1.current_conditions[2])
    t.append(DT * counter)
    counter += 1
    body1.draw(screen, scaling, offsets)
    body2.draw(screen, scaling, offsets)
    body3.draw(screen, scaling, offsets)


    # for i in range(0, len(planets), 2):
    #     earth = planets[i]
    #     random_planet = planets[i+1]

    #     earth.update_position(random_planet)
    #     random_planet.update_position(earth)

    #     if i/2 == current_system and centering:
    #         earth.draw(screen, scaling, offsets, highlight=True)
    #         random_planet.draw(screen, scaling, offsets, highlight=True)
    #     else:
    #         earth.draw(screen, scaling, offsets)
    #         random_planet.draw(screen, scaling, offsets)

    pygame.draw.circle(screen, "white", center, 2)

    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    pygame.display.update()
    pygame.display.flip()


    clock.tick(30)  # limits FPS to 60

pygame.quit()
pyplot.title("Motion of three bodies numerically calculated using Euler's Method with dt = 10")
fig, axs = pyplot.subplots(3)
axs[0].set_title("X coordinates of motion")
axs[0].plot(t, body1x, 'green', label='Green Body')
axs[0].plot(t, body2x, 'blue', label='Blue Body')
axs[0].plot(t, body3x, 'red', label='Red Body')
axs[0].xaxis.set_units("position of bodies (m)")
axs[0].yaxis.set_units("number of time step (x * dt)")

axs[1].set_title("Y coordinates of motion")
axs[1].plot(t, body1y, 'green', label='Green Body')
axs[1].plot(t, body2y, 'blue', label='Blue Body')
axs[1].plot(t, body3y, 'red', label='Red Body')
axs[1].xaxis.set_units("position of bodies (m)")
axs[1].yaxis.set_units("number of time step (x * dt)")

axs[1].set_title("X-Y coordinates of motion")
axs[2].plot(body1y, body1x, 'green', label='Green Body')
axs[2].plot(body2y, body2x, 'blue', label='Blue Body')
axs[2].plot(body3y, body3x, 'red', label='Red Body')

pyplot.legend() 
pyplot.show()
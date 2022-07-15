import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 800 #game window size in pixels
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Displaying on specified window size
pygame.display.set_caption("Planets Rotation") #Window Title

# COLORS
GRAY = (128, 128, 128) #mercury
YELLOWISH = (165, 124, 27) #venus
BLUE = (0, 0, 225) #earth
RED = (198, 123, 92) #mars
BROWN = (144, 97, 77) #jupiter
CARMEL = (195, 161, 113) #saturn
DARK_BLUE = (79, 208, 231) #uranus
WHITE = (255, 255, 255) #text
YELLOW = (255, 255, 0) #sun
DARK_GRAY = (80, 78, 81) #orbit

# FONT
FONT = pygame.font.SysFont("Arial Rounded MT Bold", 16)

class Planets:
    # AU - Astronomical Unit, * 1000 to convert into meters
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 10 / AU # 1AU = 100 Px
    TIMESTEP = 3600*24 # To see the planet with the time frame of 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        #To draw things at the center of the screen
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            update_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                update_points.append((x, y))

            pygame.draw.lines(win, self.color, False, update_points, 2)

        pygame.draw.circle(win, self.color, (x,y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))

    def attraction (self, other):
        # other = planets
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x, force_y

    def update_position(self, planets):
        # total forces exerted on the planet from planet which are not in self
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # calculate velocity
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

        # this will give ellipltical beacause when distance and angle
        # change the force will be negative or positive

def main (): #Main Function
    run = True #to start the loop to keep it running
    clock = pygame.time.Clock() #to keep running the simulation on specified time

    sun = Planets(0,0,20, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    mercury = Planets(0.387 * Planets.AU, 0, 8, GRAY, 3.30 * 10**24)
    mercury.y_vel = 47.4 * 1000 #Kilometer * 1000 = meter

    venus = Planets(0.723 * Planets.AU, 0, 14, YELLOWISH, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000 #Kilometer * 1000 = meter
    
    earth = Planets(-1 * Planets.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000 #Kilometer * 1000 = meter

    mars = Planets(-1.524 * Planets.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000 #Kilometer * 1000 = meter

    jupiter = Planets(5.203 * Planets.AU, 0, 16, BROWN, 1898.13 * 10**24)
    jupiter.y_vel = 13.06 * 1000 #Kilometer * 1000 = meter

    saturn = Planets(9.537 * Planets.AU, 0, 16, CARMEL, 568.32 * 10**24)
    saturn.y_vel = 9.68 * 1000 #Kilometer * 1000 = meter

    uranus = Planets(19.191 * Planets.AU, 0, 16, DARK_BLUE, 86.81 * 10**24)
    uranus.y_vel = 6.80 * 1000 #Kilometer * 1000 = meter

    neptune = Planets(30.068 * Planets.AU, 0, 16, BLUE, 102.498 * 10**24)
    neptune.y_vel = 5.43 * 1000 #Kilometer * 1000 = meter

    pluto = Planets(39.281 * Planets.AU, 0, 16, BROWN, 0.01303 * 10**24)
    pluto.y_vel = 4.67 * 1000 #Kilometer * 1000 = meter

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

    while run:
        clock.tick(60) #Changes will occur at 60 tick rate
        WIN.fill((0,0,0)) #Window Bg

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update() #To update the display with newly added codes

    pygame.quit()

main()
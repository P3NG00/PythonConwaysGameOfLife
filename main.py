import pygame
from pygame import Color
from pygame import Vector2


# constants
SURFACE_SIZE = Vector2(800, 600)
CLOCK = pygame.time.Clock()
FPS = 65.0
COLOR_BG = Color(0, 0, 0)
COLOR_CLICK = Color(255, 0, 0)

# variables
running = True
clicked = False

# initialize pygame
pygame.init()

# create surface
surface = pygame.display.set_mode(SURFACE_SIZE)


# loop
while running:

    # handle input
    for event in pygame.event.get():

        match event.type:

            case pygame.QUIT:

                # end script
                running = False

            case pygame.KEYDOWN:

                match event.key:

                    case pygame.K_END:

                        # end script
                        running = False

                    case pygame.K_PAGEDOWN:

                        # minimize display
                        pygame.display.iconify()

            case pygame.MOUSEBUTTONDOWN:

                match event.button:

                    case pygame.BUTTON_LEFT:

                        # left mouse held
                        clicked = True

            case pygame.MOUSEBUTTONUP:

                match event.button:

                    case pygame.BUTTON_LEFT:

                        # left mouse released
                        clicked = False

    # draw
    surface.fill(COLOR_BG)

    if clicked:
        pygame.draw.circle(surface, COLOR_CLICK, pygame.mouse.get_pos(), 5)

    # update display
    pygame.display.flip()

    # tick fps clock
    CLOCK.tick(FPS)

    # loops again if running is true


# quit pygame
pygame.quit()

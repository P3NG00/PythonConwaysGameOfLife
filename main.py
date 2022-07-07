import pygame
from pygame import Color
from pygame import Surface
from pygame import Vector2


# constants
WINDOW_TITLE = "C.G.O.L"
CLOCK = pygame.time.Clock()
FPS = 65.0
COLOR_BG = Color(128, 128, 128)
COLOR_UNIT_INACTIVE = Color(0, 0, 0)
COLOR_UNIT_ACTIVE = Color(255, 255, 255)
UNIT_ARRAY_SQUARE_SIZE = 10
UNIT_SIZE = 25
UNIT_SIZE_VECTOR = Vector2(UNIT_SIZE)


class Unit:

    def __init__(self, position: Vector2):
        self.active = False
        self.position = position

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface,
                         COLOR_UNIT_ACTIVE if self.active else COLOR_UNIT_INACTIVE,
                         (self.position, UNIT_SIZE_VECTOR))


# variables
running = True
# TODO figure out why there is no space between each unit
unit_array = [Unit(Vector2(x * UNIT_SIZE,
                           y * UNIT_SIZE))
                            for y in range(UNIT_ARRAY_SQUARE_SIZE)
                            for x in range(UNIT_ARRAY_SQUARE_SIZE)]
dirty_array = unit_array.copy()
surface_size = (800, 600)

# initialize pygame
pygame.init()

# create surface
surface = pygame.display.set_mode(surface_size, pygame.RESIZABLE)
surface.fill(COLOR_BG)
pygame.display.set_caption(WINDOW_TITLE)


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

                        # toggle state of selected unit
                        mouse_pos = pygame.mouse.get_pos()
                        mouse_pos = (int(mouse_pos[0] / UNIT_SIZE),
                                     int(mouse_pos[1] / UNIT_SIZE))
                        if mouse_pos[0] < UNIT_ARRAY_SQUARE_SIZE and \
                           mouse_pos[1] < UNIT_ARRAY_SQUARE_SIZE:
                            mouse_unit = unit_array[(mouse_pos[1] * UNIT_ARRAY_SQUARE_SIZE) + mouse_pos[0]]
                            mouse_unit.active = not mouse_unit.active
                            dirty_array.append(mouse_unit)

            case pygame.VIDEORESIZE:

                # update surface size
                surface_size = (event.w, event.h)
                # redraw every unit
                dirty_array = unit_array.copy()

    # draw
    for unit in dirty_array:
        unit.draw(surface)
    dirty_array.clear()

    # update display
    pygame.display.flip()

    # tick fps clock
    CLOCK.tick(FPS)

    # loops again if running is true


# quit pygame
pygame.quit()

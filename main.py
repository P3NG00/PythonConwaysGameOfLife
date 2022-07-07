import pygame
from pygame import Color
from pygame import Surface
from pygame import Vector2


# constants
WINDOW_TITLE = "C.G.O.L"
CLOCK = pygame.time.Clock()
FPS = 65.0
COLOR_BG = Color(64, 64, 64)
COLOR_UNIT_INACTIVE = Color(0, 0, 0)
COLOR_UNIT_ACTIVE = Color(255, 255, 255)
UNIT_ARRAY_SQUARE_SIZE = 20
UNIT_SIZE = 24
UNIT_SIZE_VECTOR = Vector2(UNIT_SIZE)
UNIT_BORDER_SPACE = 1
TOTAL_UNIT_SIZE = UNIT_SIZE + UNIT_BORDER_SPACE
TOTAL_UNIT_SIZE_VECTOR = Vector2(TOTAL_UNIT_SIZE)


class Unit:

    def __init__(self, position: Vector2):
        self.active = False
        self.position = position

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface,
                         COLOR_UNIT_ACTIVE if self.active else COLOR_UNIT_INACTIVE,
                         (self.position, TOTAL_UNIT_SIZE_VECTOR if simulating else UNIT_SIZE_VECTOR))


def redraw_all():
    global dirty_array
    # refill surface
    surface.fill(COLOR_BG)
    # mark all units dirty
    dirty_array = unit_array.copy()


# variables
running = True
simulating = False
unit_array = [Unit(Vector2((x * TOTAL_UNIT_SIZE) + UNIT_BORDER_SPACE,
                           (y * TOTAL_UNIT_SIZE) + UNIT_BORDER_SPACE))
                            for y in range(UNIT_ARRAY_SQUARE_SIZE)
                            for x in range(UNIT_ARRAY_SQUARE_SIZE)]
# dirty array starts with copy of reference to the created units
dirty_array = unit_array.copy()
surface_size = (TOTAL_UNIT_SIZE_VECTOR * UNIT_ARRAY_SQUARE_SIZE) + Vector2(UNIT_BORDER_SPACE)

# create surface
pygame.init()
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

                    case pygame.K_SPACE:

                        # toggle simulation
                        simulating = not simulating
                        redraw_all()

            case pygame.MOUSEBUTTONDOWN:

                match event.button:

                    case pygame.BUTTON_LEFT:

                        if not simulating:
                            # toggle active state of selected unit
                            mouse_pos = pygame.mouse.get_pos()
                            mouse_pos = (int(mouse_pos[0] / TOTAL_UNIT_SIZE),
                                         int(mouse_pos[1] / TOTAL_UNIT_SIZE))
                            if mouse_pos[0] < UNIT_ARRAY_SQUARE_SIZE and \
                               mouse_pos[1] < UNIT_ARRAY_SQUARE_SIZE:
                                mouse_unit = unit_array[(mouse_pos[1] * UNIT_ARRAY_SQUARE_SIZE) + mouse_pos[0]]
                                mouse_unit.active = not mouse_unit.active
                                dirty_array.append(mouse_unit)

            case pygame.VIDEORESIZE:

                # update surface size
                surface_size = (event.w, event.h)
                redraw_all()

    # draw
    if len(dirty_array) is not 0:
        for unit in dirty_array:
            unit.draw(surface)
        pygame.display.flip()
        dirty_array.clear()

    # tick fps clock
    CLOCK.tick(FPS)

    # loops again if running is true


# quit pygame
pygame.quit()

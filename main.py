import pygame
from pygame import Color
from pygame import Surface
from pygame import Vector2


# changable constants
WINDOW_TITLE = "C.G.O.L"
FPS = 65.0
COLOR_BG = Color(64, 64, 64)
COLOR_UNIT_INACTIVE = Color(0, 0, 0)
COLOR_UNIT_ACTIVE = Color(255, 255, 255)
UNIT_ARRAY_SQUARE_SIZE = 20
UNIT_SIZE = 24
UNIT_BORDER_SPACE = 1

# dependent constants
CLOCK = pygame.time.Clock()
UNIT_SIZE_HALF = UNIT_SIZE / 2
UNIT_SIZE_VECTOR = Vector2(UNIT_SIZE)
UNIT_SIZE_VECTOR_HALF = UNIT_SIZE_VECTOR / 2
TOTAL_UNIT_SIZE = UNIT_SIZE + UNIT_BORDER_SPACE
TOTAL_UNIT_SIZE_VECTOR = Vector2(TOTAL_UNIT_SIZE)
TOTAL_UNIT_SIZE_VECTOR_HALF = TOTAL_UNIT_SIZE_VECTOR / 2


class Unit:

    def __init__(self, position: Vector2):
        self.active = False
        self.position = position

    def draw(self, surface: Surface) -> None:
        if draw_mode:
            pygame.draw.rect(surface, self._get_color(), (self.position,
                             TOTAL_UNIT_SIZE_VECTOR if simulating else UNIT_SIZE_VECTOR))
        else:
            pygame.draw.circle(surface, self._get_color(), self.position +
                              (TOTAL_UNIT_SIZE_VECTOR_HALF if simulating else
                               UNIT_SIZE_VECTOR_HALF), UNIT_SIZE_HALF)

    def _get_color(self) -> Color:
        return COLOR_UNIT_ACTIVE if self.active else COLOR_UNIT_INACTIVE


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
surface_size = (TOTAL_UNIT_SIZE_VECTOR * UNIT_ARRAY_SQUARE_SIZE) + Vector2(UNIT_BORDER_SPACE)
draw_mode = True

# create surface
pygame.init()
pygame.display.set_caption(WINDOW_TITLE)
surface = pygame.display.set_mode(surface_size)
redraw_all()


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

                    case pygame.K_F1:

                        # toggle draw mode
                        draw_mode = not draw_mode
                        redraw_all()

            case pygame.MOUSEBUTTONDOWN:

                match event.button:

                    case pygame.BUTTON_LEFT:

                        if not simulating:
                            # toggle active state of selected unit
                            mouse_pos = pygame.mouse.get_pos()
                            mouse_pos = (int(mouse_pos[0] / TOTAL_UNIT_SIZE),
                                         int(mouse_pos[1] / TOTAL_UNIT_SIZE))
                            # check click was in bounds
                            if mouse_pos[0] < UNIT_ARRAY_SQUARE_SIZE and \
                               mouse_pos[1] < UNIT_ARRAY_SQUARE_SIZE:
                                # add selected unit to dirty list
                                mouse_unit = unit_array[(mouse_pos[1] * UNIT_ARRAY_SQUARE_SIZE) + mouse_pos[0]]
                                mouse_unit.active = not mouse_unit.active
                                dirty_array.append(mouse_unit)

    # draw
    if len(dirty_array) != 0:
        for unit in dirty_array:
            unit.draw(surface)
        pygame.display.flip()
        dirty_array.clear()

    # tick fps clock
    CLOCK.tick(FPS)

    # loops again if running is true


# quit pygame
pygame.quit()

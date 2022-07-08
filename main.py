import math
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
SIMULATION_TIMER_SECONDS = 0.25
UNIT_ARRAY_SQUARE_SIZE = 50
UNIT_SIZE = 14
UNIT_BORDER_SPACE = 1


def seconds_to_frames(seconds: float) -> int:
    """returns the amount of frames equivalent to the given seconds"""
    return math.ceil(seconds * FPS)


# dependent constants
CLOCK = pygame.time.Clock()
UNIT_SIZE_HALF = math.ceil(UNIT_SIZE / 2)
UNIT_SIZE_VECTOR = Vector2(UNIT_SIZE)
UNIT_SIZE_VECTOR_HALF = UNIT_SIZE_VECTOR / 2
UNIT_ARRAY_SQUARE_SIZE_RANGE = range(UNIT_ARRAY_SQUARE_SIZE)
SIMULATION_TIMER_FRAMES = seconds_to_frames(SIMULATION_TIMER_SECONDS)
TOTAL_UNIT_SIZE = UNIT_SIZE + UNIT_BORDER_SPACE
TOTAL_UNIT_SIZE_VECTOR = Vector2(TOTAL_UNIT_SIZE)


class Unit:

    def __init__(self, position: Vector2):
        self.active = False
        self.active_last = self.active
        self.position = position

    def draw(self, surface: Surface) -> None:
        """draws the unit to the given surface at its position"""
        match draw_mode:
            case 0:
                pygame.draw.rect(surface, self._get_color(), (self.position, UNIT_SIZE_VECTOR))
            case 1:
                pygame.draw.rect(surface, self._get_color(), (self.position, TOTAL_UNIT_SIZE_VECTOR))
            case 2:
                pygame.draw.circle(surface, self._get_color(), self.position + UNIT_SIZE_VECTOR_HALF, UNIT_SIZE_HALF)

    def _get_color(self) -> Color:
        """returns the appropriate color for this unit's active state"""
        return COLOR_UNIT_ACTIVE if self.active else COLOR_UNIT_INACTIVE


def redraw_all() -> None:
    """clears screen and adds all units to dirty_array to be redrawn"""
    global dirty_array
    # refill surface
    surface.fill(COLOR_BG)
    # mark all units dirty
    dirty_array.clear()
    for _unit in unit_array:
        for unit in _unit:
            dirty_array.append(unit)

def update_units() -> None:
    """handles updating all units"""
    for y in UNIT_ARRAY_SQUARE_SIZE_RANGE:
        for x in UNIT_ARRAY_SQUARE_SIZE_RANGE:
            # check for neighbors
            unit_neighbors = 0
            for offset_y in range(3):
                for offset_x in range(3):
                    # skip check if offset is centered
                    if offset_x == 1 and offset_y == 1:
                        continue
                    # neighbor coordinates
                    check_x = x + (offset_x - 1)
                    check_y = y + (offset_y - 1)
                    # skip check if check if out of bounds
                    if check_x < 0 or check_y < 0 or \
                       check_x > UNIT_ARRAY_SQUARE_SIZE - 1 or \
                       check_y > UNIT_ARRAY_SQUARE_SIZE - 1:
                        continue
                    # if unit at check position was active, increment neighbor count
                    if unit_array[check_y][check_x].active_last:
                        unit_neighbors += 1
            # get current unit
            unit = unit_array[y][x]
            # if unit is active and has too few or too many neighbors
            if unit.active:
                if unit_neighbors < 2 or unit_neighbors > 3:
                    # make unit inactive
                    unit.active = False
                    dirty_array.append(unit)
            # if unit is not active and has exactly three neighbors
            else:
                if unit_neighbors == 3:
                    # make unit active
                    unit.active = True
                    dirty_array.append(unit)


# variables
running = True
simulating = False
simulation_timer = 0
unit_array = [[Unit(Vector2((x * TOTAL_UNIT_SIZE) + UNIT_BORDER_SPACE,
                            (y * TOTAL_UNIT_SIZE) + UNIT_BORDER_SPACE))
                             for x in UNIT_ARRAY_SQUARE_SIZE_RANGE]
                             for y in UNIT_ARRAY_SQUARE_SIZE_RANGE]
dirty_array = []
surface_size = (TOTAL_UNIT_SIZE_VECTOR * UNIT_ARRAY_SQUARE_SIZE) + Vector2(UNIT_BORDER_SPACE)
draw_mode = 0
input_shift = False

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

                        # step through one unit update
                        update_units()

                    case pygame.K_RETURN:

                        # toggle simulation
                        simulating = not simulating
                        simulation_timer = 0

                    case pygame.K_F1:

                        # toggle draw mode
                        if input_shift:
                            draw_mode -= 1
                            if draw_mode == -1:
                                draw_mode = 2
                        else:
                            draw_mode += 1
                            if draw_mode == 3:
                                draw_mode = 0
                        # redraw all units
                        redraw_all()

                    case pygame.K_LSHIFT | pygame.K_RSHIFT:

                        # mark shift as held
                        input_shift = True

            case pygame.KEYUP:

                match event.key:

                    case pygame.K_LSHIFT | pygame.K_RSHIFT:

                        # mark shift as released
                        input_shift = False

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
                                # find selected unity, modify active state, and add to dirty list
                                mouse_unit = unit_array[mouse_pos[1]][mouse_pos[0]]
                                mouse_unit.active = not mouse_unit.active
                                dirty_array.append(mouse_unit)

    # check if handling simulation
    if simulating:

        # decrease simulation_timer
        simulation_timer -= 1

        # check if next simulation update
        if simulation_timer == -1:

            # reset timer and handle step
            simulation_timer = SIMULATION_TIMER_FRAMES
            update_units()

    # draw
    if len(dirty_array) != 0:
        for unit in dirty_array:
            # redraw dirty units
            unit.draw(surface)
            # update dirty units last active state
            unit.active_last = unit.active
        # clear dirty unit array
        dirty_array.clear()
        # update display
        pygame.display.flip()

    # tick fps clock
    CLOCK.tick(FPS)

    # loops again if running is true


# quit pygame
pygame.quit()

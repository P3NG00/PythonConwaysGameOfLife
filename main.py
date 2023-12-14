import json
import math
import pygame
from pygame import Color
from pygame import Surface
from pygame import Vector2


# changeable constants
WINDOW_TITLE = "C.G.o.L"
FPS = 60.0
COLOR_BG = Color(64, 64, 64)
UNIT_COLORS = [Color(0, 0, 0),
               Color(255, 255, 255)]
UNIT_ARRAY_SIZE = (50, 50)
UNIT_SIZE = 14
UNIT_BORDER = 1


def seconds_to_frames(seconds: float) -> int:
    """returns the amount of frames equivalent to the given seconds"""
    return math.ceil(seconds * FPS)


# dependent constants
CLOCK = pygame.time.Clock()
UNIT_SIZE_HALF = math.ceil(UNIT_SIZE / 2)
UNIT_SIZE_VECTOR = Vector2(UNIT_SIZE)
UNIT_SIZE_VECTOR_HALF = UNIT_SIZE_VECTOR / 2
UNIT_ARRAY_SIZE_RANGE = (range(UNIT_ARRAY_SIZE[0]),
                         range(UNIT_ARRAY_SIZE[1]))
UNIT_BORDER_VECTOR = Vector2(UNIT_BORDER)
TOTAL_UNIT_SIZE = UNIT_SIZE + UNIT_BORDER
TOTAL_UNIT_SIZE_VECTOR = Vector2(TOTAL_UNIT_SIZE)


class Unit:

    def __init__(self, position: Vector2):
        self.active = False
        self.active_last = False
        self.position = position

    def draw(self, surface: Surface) -> None:
        """draws the unit to the given surface at its position"""
        color = UNIT_COLORS[1] if self.active else UNIT_COLORS[0]
        match draw_mode:
            case 0:
                pygame.draw.rect(surface, color, (self.position, UNIT_SIZE_VECTOR))
            case 1:
                pygame.draw.rect(surface, color, (self.position, TOTAL_UNIT_SIZE_VECTOR))
            case 2:
                pygame.draw.circle(surface, color, self.position + UNIT_SIZE_VECTOR_HALF, UNIT_SIZE_HALF)


def redraw_all() -> None:
    """clears screen and adds all units to dirty_array to be redrawn"""
    # refill surface
    surface.fill(COLOR_BG)
    # mark all units dirty
    dirty_array.clear()
    for _unit in unit_array:
        for unit in _unit:
            dirty_array.append(unit)


def update_units() -> None:
    """handles updating all units"""
    for y in UNIT_ARRAY_SIZE_RANGE[1]:
        for x in UNIT_ARRAY_SIZE_RANGE[0]:
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
                    # skip check if out of bounds
                    if check_x < 0 or check_y < 0 or \
                       check_x > UNIT_ARRAY_SIZE[0] - 1 or \
                       check_y > UNIT_ARRAY_SIZE[1] - 1:
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


def deactivate_all_units() -> None:
    """iterates through and deactivates all units"""
    for _unit in unit_array:
        for unit in _unit:
            unit.active = False
            unit.active_last = False
    redraw_all()


def handle_slot(slot: int) -> None:
    """handles saving/loading to a file"""
    save_name = f"save_{slot}.json"
    # if holding shift, save to slot
    if input_shift:
        with open(save_name, "w") as file:
            json.dump([[1 if unit.active else 0 for unit in _unit] for _unit in unit_array], file, indent = 2)
    # if not holding shift, load slot
    else:
        try:
            with open(save_name) as file:
                unit_active_list = json.load(file)
            for y in UNIT_ARRAY_SIZE_RANGE[1]:
                for x in UNIT_ARRAY_SIZE_RANGE[0]:
                    unit = unit_array[y][x]
                    try:
                        unit_active = unit_active_list[y][x] == 1
                        unit.active = unit_active
                        unit.active_last = unit_active
                    except:
                        unit.active = False
                        unit.active_last = False
            global simulating
            simulating = False
            redraw_all()
        except:
            deactivate_all_units()


# variables
running = True
simulating = False
unit_array = [[Unit(Vector2((x * TOTAL_UNIT_SIZE) + UNIT_BORDER,
                            (y * TOTAL_UNIT_SIZE) + UNIT_BORDER))
                             for x in UNIT_ARRAY_SIZE_RANGE[0]]
                             for y in UNIT_ARRAY_SIZE_RANGE[1]]
dirty_array = []
surface_size = TOTAL_UNIT_SIZE_VECTOR.copy()
surface_size.x *= UNIT_ARRAY_SIZE[0]
surface_size.y *= UNIT_ARRAY_SIZE[1]
surface_size += Vector2(UNIT_BORDER)
draw_mode = 0
input_shift = False
color_swap = False

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
                        if not simulating:
                            update_units()

                    case pygame.K_RETURN | pygame.K_KP_ENTER:

                        # toggle simulation
                        simulating = not simulating

                    case pygame.K_TAB:

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

                    case pygame.K_ESCAPE:

                        # clear screen
                        deactivate_all_units()

                    case pygame.K_BACKQUOTE:

                        # swap units color scheme
                        _color_hold = UNIT_COLORS[0]
                        UNIT_COLORS[0] = UNIT_COLORS[1]
                        UNIT_COLORS[1] = _color_hold
                        redraw_all()

                    # handle saving and loading slots with function keys
                    case pygame.K_F1:
                        handle_slot(1)
                    case pygame.K_F2:
                        handle_slot(2)
                    case pygame.K_F3:
                        handle_slot(3)
                    case pygame.K_F4:
                        handle_slot(4)
                    case pygame.K_F5:
                        handle_slot(5)
                    case pygame.K_F6:
                        handle_slot(6)
                    case pygame.K_F7:
                        handle_slot(7)
                    case pygame.K_F8:
                        handle_slot(8)
                    case pygame.K_F9:
                        handle_slot(9)
                    case pygame.K_F10:
                        handle_slot(10)
                    case pygame.K_F11:
                        handle_slot(11)
                    case pygame.K_F12:
                        handle_slot(12)

            case pygame.KEYUP:

                match event.key:

                    case pygame.K_LSHIFT | pygame.K_RSHIFT:

                        # mark shift as released
                        input_shift = False

            case pygame.MOUSEBUTTONDOWN:

                match event.button:

                    case pygame.BUTTON_LEFT:

                        # disable simulation
                        if simulating:
                            simulating = False
                        # toggle active state of selected unit
                        mouse_pos = pygame.mouse.get_pos()
                        mouse_pos = (int(mouse_pos[0] / TOTAL_UNIT_SIZE),
                                     int(mouse_pos[1] / TOTAL_UNIT_SIZE))
                        # check click was in bounds
                        if mouse_pos[0] < UNIT_ARRAY_SIZE[0] and \
                           mouse_pos[1] < UNIT_ARRAY_SIZE[1]:
                            # find selected unity, modify active state, and add to dirty list
                            mouse_unit = unit_array[mouse_pos[1]][mouse_pos[0]]
                            mouse_unit.active = not mouse_unit.active
                            dirty_array.append(mouse_unit)

    # update units if simulating
    if simulating:
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

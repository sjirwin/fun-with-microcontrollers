import board
import collections
import displayio
import math
import time

import adafruit_itertools as itertools

from adafruit_display_shapes.arc import Arc
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle

import my_display
import my_rtc
import sun_events
import event_durations

from location import Location


# Brooklyn, NY, USA
LOCATION = Location(40.6928, -73.9903, 'America/New_York')

# number of seconds in a day
TOTAL_SECONDS = 24 * 60 * 60

# colors used
WHITE = 0xFFFFFF
LIGHT_GREY = 0xAAAAAA
GREY = 0x888888
DARK_GREY = 0x333333
BLACK = 0x000000
NEAR_BLACK = 0x111111
BLUE = 0x0000FF

IndicatorPoints = collections.namedtuple(
    'IndicatorPoints',
    ('x0', 'y0', 'x1', 'y1', 'x2', 'y2')
)


def now_angle() -> float:
    '''
    Calculate the angle around the clock face (in radians) for the current time

    Midnight is pi/2 radians
    '''
    now = my_rtc.current_time(board.I2C())
    secs_now = now.tm_sec + 60 * (now.tm_min + (60 * now.tm_hour))
    return (2 * math.pi * secs_now / TOTAL_SECONDS) - (math.pi / 2)


def now_pts(angle: float, radius: float) -> IndicatorPoints:
    x0 = int((0.9 * radius) * math.cos(angle)) + w2
    y0 = int((0.9 * radius) * math.sin(angle)) + h2
    x1 = int((0.2 * radius) * math.cos(angle + math.pi + .05)) + w2
    y1 = int((0.2 * radius) * math.sin(angle + math.pi + .05)) + h2
    x2 = int((0.2 * radius) * math.cos(angle + math.pi - .05)) + w2
    y2 = int((0.2 * radius) * math.sin(angle + math.pi - .05)) + h2
    return IndicatorPoints(x0, y0, x1, y1, x2, y2)


def create_arcs(date, location: Location, radius: float):
    # time of each solar day event for date and location
    events = sun_events.sunevents(date, location)

    # calculate duration (in secs) of each solar day event
    durations = event_durations.durations(events)

    # data needed to calculate arc paramters
    arc_start_pts = list(itertools.accumulate([0]+durations, func=lambda x, y: x + y))
    arc_mid_pts = [d // 2 for d in durations]

    # calculate parameters needed to draw the arcs
    arc_colors = [BLACK, DARK_GREY, GREY, LIGHT_GREY, WHITE, LIGHT_GREY, GREY, DARK_GREY, BLACK]
    arc_directions = [
        (360 * (start + mid) / TOTAL_SECONDS) + 90
        for start, mid
        in zip(arc_start_pts, arc_mid_pts)
    ]
    arc_angles = [360 * dur / TOTAL_SECONDS for dur in durations]

    arcs = [
        Arc(
            x=w2,
            y=h2,
            radius=radius,
            arc_width=radius,
            angle=angle,
            direction=direction,
            fill=color,
            segments=min(10, int(5 * angle))
        )
        for color, direction, angle
        in zip(arc_colors, arc_directions, arc_angles)
    ]

    return arcs


# ----------------------------------------------------

# Release any resources currently in use for the displays
displayio.release_displays()

# connect to the display
display = my_display.get_display(board)

# center of the display
w2 = display.width // 2
h2 = display.height // 2

radius = 0.9 * h2

# create group for display
group = displayio.Group()
display.root_group = group

# background
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = NEAR_BLACK
bg = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
group.append(bg)

# ----------------------------------------------------

# current date
date = my_rtc.current_date(board.I2C())

# arcs for each solar day events
arcs = create_arcs(date, LOCATION, radius)

# add arcs to display group
for arc in arcs:
    group.append(arc)

# sun dial time indicator
angle = now_angle()
pts = now_pts(angle=angle, radius=radius)

indicator = Triangle(pts.x0, pts.y0, pts.x1, pts.y1, pts.x2, pts.y2, fill=BLUE, outline=BLUE)
group.append(indicator)

# decorative dot in the center
center_dot = Circle(w2, h2, 5, fill=WHITE, outline=BLACK, stroke=3)
group.append(center_dot)

previous_date = date
previous_arcs = arcs
previous_pts = pts
previous_indicator = indicator

while True:
    # wait a minute
    time.sleep(60.0)

    date = my_rtc.current_date(board.I2C())

    # if new date, update the arcs
    if date > previous_date:
        arcs = create_arcs(date, LOCATION, radius)

        for new_arc, prev_arc in zip(arcs, previous_arcs):
            indx = group.index(prev_arc)
            group[indx] = new_arc
            del prev_arc

        previous_date = date
        previous_arcs = arcs

    angle = now_angle()
    pts = now_pts(angle=angle, radius=radius)

    # if the pts have changed, update the indicator
    if pts != previous_pts:
        indicator = Triangle(pts.x0, pts.y0, pts.x1, pts.y1, pts.x2, pts.y2, fill=BLUE, outline=BLUE)
        indx = group.index(previous_indicator)
        group[indx] = indicator
        del previous_indicator

        previous_pts = pts
        previous_indicator = indicator

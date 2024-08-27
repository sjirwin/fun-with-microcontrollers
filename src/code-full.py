import board
import displayio
import math

import adafruit_itertools as itertools

from adafruit_display_shapes.arc import Arc
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle

import my_display
from location import Location
import my_rtc
import sun_events
import event_durations


# number of seconds in a day
TOTAL_SECONDS = 24 * 60 * 60

# display colors
WHITE = 0xFFFFFF
LIGHT_GREY = 0xAAAAAA
GREY = 0x808080
DARK_GREY = 0x555555
NEAR_BLACK = 0x333333
BLACK = 0x000000
BLUE = 0x0000FF

date = my_rtc.current_date(board.I2C())

# Brooklyn, NY, USA
loc = Location(40.6928, -73.9903, 'America/New_York')

# time of each solar day event for the supplied date and location
events = sun_events.sunevents(date, loc)

# calculate duration (in secs) of each solar day event
durations = event_durations.durations(events)

# ----------------------------------------------------

# Release any resources currently in use for the displays
displayio.release_displays()

# connect to the display
display = my_display.get_display(board)

# center of the display
w2 = display.width // 2
h2 = display.height // 2

# data needed to calculate arc paramters
arc_start_pts = list(itertools.accumulate([0]+durations, func=lambda x, y: x + y))
arc_mid_pts = [d // 2 for d in durations]

# calculate parameters needed to draw the arcs
radius = 0.9 * h2
arc_colors = [BLACK, DARK_GREY, GREY, LIGHT_GREY, WHITE, LIGHT_GREY, GREY, DARK_GREY, BLACK]
arc_directions = [
    360 * (start + mid) / TOTAL_SECONDS
    for start, mid
    in zip(arc_start_pts, arc_mid_pts)
]
arc_angles = [360 * dur / TOTAL_SECONDS for dur in durations]

# ----- build the graphic elements -----

group = displayio.Group()
display.root_group = group

# background
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = NEAR_BLACK
bg = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
group.append(bg)

# arcs for each solar day events
for color, direction, angle in zip(arc_colors, arc_directions, arc_angles):
    arc = Arc(
        x=w2,
        y=h2,
        radius=radius,
        arc_width=radius,
        angle=angle,
        direction=direction,
        fill=color,
        segments=min(10, int(5 * angle))
    )
    group.append(arc)

# hand to indicate time on the sun dial
now = my_rtc.current_time(board.I2C())
secs_now = now.tm_sec + 60 * (now.tm_min + 60 * now.tm_hour)
now_angle = 2 * math.pi * secs_now / TOTAL_SECONDS # radians
x0 = int((0.9 * radius) * math.cos(now_angle)) + w2
y0 = int((0.9 * radius) * math.sin(now_angle)) + h2
x1 = int((0.2 * radius) * math.cos(now_angle + math.pi + .05)) + w2
y1 = int((0.2 * radius) * math.sin(now_angle + math.pi + .05)) + h2
x2 = int((0.2 * radius) * math.cos(now_angle + math.pi - .05)) + w2
y2 = int((0.2 * radius) * math.sin(now_angle + math.pi - .05)) + h2
hand = Triangle(x0, y0, x1, y1, x2, y2, fill=BLUE, outline=BLUE)
group.append(hand)

# decorative dot in the center
center_dot = Circle(w2, h2, 5, fill=WHITE, outline=BLACK, stroke=3)
group.append(center_dot)

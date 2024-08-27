import board
import displayio
import math

import adafruit_datetime as datetime
import adafruit_itertools as itertools

from adafruit_display_shapes.arc import Arc
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.line import Line

import my_display
from location import Location
import my_rtc
import sun_events


date = my_rtc.current_date(board.I2C())

# Brooklyn, NY, USA
loc = Location(40.6928, -73.9903, 'America/New_York')

events = sun_events.sunevents(date, loc)

# ---- calculate the arc parameters of each portion of the solar day

dawn = events.dawn
twilight = events.twilight

TOTAL_SECONDS = 24 * 60 * 60

midnight_today = dawn.astronomical_begin.replace(hour=0, minute=0, second=0)
midnight_tomorrow = midnight_today + datetime.timedelta(days=1)

td_mid2astrodawn = dawn.astronomical_begin - midnight_today
td_astrotwltend2mid = midnight_tomorrow - twilight.astronomical_end

secs_astrodawn = (dawn.nautical_begin - dawn.astronomical_begin).total_seconds()
secs_nautdawn = (dawn.civil_begin - dawn.nautical_begin).total_seconds()
secs_civildawn = (events.sunrise - dawn.civil_begin).total_seconds()

secs_day = events.day_length

secs_civiltwilight = (twilight.civil_end - events.sunset).total_seconds()
secs_nauttwilight = (twilight.nautical_end - twilight.civil_end).total_seconds()
secs_astrotwilight = (twilight.astronomical_end - twilight.nautical_end).total_seconds()

secs_night = (td_mid2astrodawn + td_astrotwltend2mid).total_seconds()

# put the various durations in sequence
durations = [
    td_mid2astrodawn.total_seconds(),
    secs_astrodawn,
    secs_nautdawn,
    secs_civildawn,
    secs_day,
    secs_civiltwilight,
    secs_nauttwilight,
    secs_astrotwilight,
    td_astrotwltend2mid.total_seconds()
]

# ----------------------------------------------------

# display colors
WHITE = 0xFFFFFF
LIGHT_GREY = 0xAAAAAA
GREY = 0x808080
DARK_GREY = 0x555555
NEAR_BLACK = 0x333333
BLACK = 0x000000
BLUE = 0x0000FF

arc_colors = [BLACK, DARK_GREY, GREY, LIGHT_GREY, WHITE, LIGHT_GREY, GREY, DARK_GREY, BLACK]

# Release any resources currently in use for the displays
displayio.release_displays()

# connect to the display
display = my_display.get_display(board)

# center of the display
w2 = display.width // 2
h2 = display.height // 2
radius = 0.9 * h2

# data needed to calculate arc paramters
arc_start_pts = list(itertools.accumulate([0]+durations, func=lambda x, y: x + y))
arc_mid_pts = [d // 2 for d in durations]

# calculate parameters for the arcs
arc_directions = [360 * (start + mid) / TOTAL_SECONDS for start, mid in zip(arc_start_pts, arc_mid_pts)]
arc_angles = [360 * dur / TOTAL_SECONDS for dur in durations]

# ---- build and show the graphic elements

group = displayio.Group()
display.root_group = group

# background
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = NEAR_BLACK
bg = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
group.append(bg)

# arcs
for color, direction, angle in zip(arc_colors, arc_directions, arc_angles):
    arc = Arc(
        x=w2,
        y=h2,
        radius=radius,
        arc_width=radius,
        angle=angle,
        direction=direction,
        fill=color,
        segments=min(10, int(3 * angle))
    )
    group.append(arc)

now = my_rtc.current_time()
secs_now = now.tm_sec + 60 * (now.tm_min + 60 * now.tm_hour)
now_angle = 2 * math.pi * secs_now / TOTAL_SECONDS # radians
x0 = int((0.9 * radius) * math.cos(now_angle)) + w2
y0 = int((0.9 * radius) * math.sin(now_angle)) + h2
x1 = int((0.2 * radius) * math.cos(now_angle + math.pi)) + w2
y1 = int((0.2 * radius) * math.sin(now_angle + math.pi)) + h2
hand = Line(x0, y0, x1, y1, color=BLUE)
group.append(hand)

center_dot = Circle(w2, h2, 5, fill=WHITE, outline=BLACK, stroke=3)
group.append(center_dot)

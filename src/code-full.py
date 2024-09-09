import board
import collections
import displayio
import math
import rtc
import time

from tzdb import timezone

import adafruit_itertools as itertools

from adafruit_datetime import datetime
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


def localtime(tzid: str = LOCATION.tzid) -> datetime:
    utc_now_dt = datetime.fromtimestamp(time.time())
    return utc_now_dt + timezone(tzid).utcoffset(utc_now_dt)


def now_angle() -> float:
    '''
    Calculate the angle around the clock face (in radians) for the current time

    Midnight is 3π/2 radians
    '''
    now = localtime()
    secs_now = now.second + 60 * (now.minute + (60 * now.hour))
    return (2 * math.pi * secs_now / TOTAL_SECONDS) + (3 * math.pi / 2)


def now_pts(angle: float, radius: float) -> IndicatorPoints:
    x0 = int((0.9 * radius) * math.cos(angle)) + w2
    y0 = int((0.9 * radius) * math.sin(angle)) + h2
    x1 = int((0.2 * radius) * math.cos(angle + math.pi + .05)) + w2
    y1 = int((0.2 * radius) * math.sin(angle + math.pi + .05)) + h2
    x2 = int((0.2 * radius) * math.cos(angle + math.pi - .05)) + w2
    y2 = int((0.2 * radius) * math.sin(angle + math.pi - .05)) + h2
    return IndicatorPoints(x0, y0, x1, y1, x2, y2)


def create_arcs(date, location: Location, radius: float) -> list[Arc]:
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
        ((360 * (start + mid) / TOTAL_SECONDS) + 90) % 360
        for start, mid
        in zip(arc_start_pts, arc_mid_pts)
    ]
    arc_angle_lens = [360 * dur / TOTAL_SECONDS for dur in durations]

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
        in zip(arc_colors, arc_directions, arc_angle_lens)
    ]

    return arcs


def arc_group(arcs: list[Arc]) -> displayio.Group:
    group = displayio.Group()
    for arc in arcs:
        group.append(arc)
    return group


def indicator_group(pts: IndicatorPoints, x: float, y: float) -> displayio.Group:
    group = displayio.Group()
    indicator = Triangle(pts.x0, pts.y0, pts.x1, pts.y1, pts.x2, pts.y2, fill=BLUE, outline=BLUE)
    group.append(indicator)
    center_dot = Circle(x, y, 5, fill=WHITE, outline=BLACK, stroke=3)
    group.append(center_dot)
    return group


# ----------------------------------------------------

# use the external real-time clock (RTC) initialize the local RTC
rtc.RTC().datetime = my_rtc.current_utc_time(i2c=board.I2C())

# Release any resources currently in use for the displays
displayio.release_displays()

# connect to the display
display = my_display.get_display(board)

# center of the display
w2 = display.width // 2
h2 = display.height // 2

radius = 0.95 * h2

# create group for display
group = displayio.Group()
display.root_group = group

# set the background
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = NEAR_BLACK
bg = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
group.append(bg)

# ----------------------------------------------------

# current date
date = localtime().date()

# arcs for each solar day events
arcs = create_arcs(date, LOCATION, radius)

# add arcs display group
group.append(arc_group(arcs))

# sun dial time indicator
angle = now_angle()
pts = now_pts(angle=angle, radius=radius)

# add indicator display group
group.append(indicator_group(pts, w2, h2))

previous_date = date
previous_pts = pts

while True:
    # wait a minute
    time.sleep(60.0)

    date = localtime().date()

    # if new date, update the arc display group
    if date > previous_date:
        print(f"{previous_date=} {date=}")
        arcs = create_arcs(date, LOCATION, radius)
        group[1] = arc_group(arcs)
        previous_date = date

    # calculate the coordinates for the indicator
    angle = now_angle()
    pts = now_pts(angle=angle, radius=radius)

    # if the pts have changed, update the indicator display group
    if pts != previous_pts:
        print(f"{angle=} ({previous_pts.x0}, {previous_pts.y0}) ({pts.x0}, {pts.y0})")
        group[2] = indicator_group(pts, w2, h2)
        previous_pts = pts

import board
import displayio

import display_ili9341
import rtc
import sun_events


WHITE = 0xFFFFFF
LIGHT_GREY = 0xD3D3D3
GREY = 0x808080
DARK_GREY = 0x555555
EERIE_BLACK = 0x1B1B1B
BLACK = 0x000000

# Release any resources currently in use for the displays
displayio.release_displays()

# connect to the display
display = display_ili9341.get_display(board)

# center of the display
w2 = int(display.width / 2)
h2 = int(display.height / 2)

date = rtc.current_date(board.I2C())

from location import Location
# Brooklyn, NY, USA
loc = Location(40.6928, -73.9903, 'America/New_York')

events = sun_events.sunevents(date, loc)

# ---- calculate the arc length of each portion of the solar day

TOTAL_SECONDS = 24 * 60 * 60


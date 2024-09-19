import displayio
import adafruit_hx8357


def display(board):
    # board details needed to talk to the display
    spi = board.SPI() # Serial Peripheral Interface (used for synchronous serial communication)
    tft_cs = board.D9 # Chip Select pin for the display
    tft_dc = board.D10 # Data/Command pin for the display

    # connect to the display
    display_bus = displayio.FourWire(
        spi,
        command=tft_dc,
        chip_select=tft_cs,
    )

    width = 480
    height = 320

    display = adafruit_hx8357.HX8357(display_bus, width=width, height=height)

    return display


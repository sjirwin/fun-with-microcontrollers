import displayio
import adafruit_ili9341


def get_display(board):
    # board details needed to talk to the display
    spi = board.SPI() # Serial Peripheral Interface (used for synchronous serial communication)
    tft_cs = board.D9 # Chip Select pin for the display
    tft_dc = board.D10 # Data/Command pin for the display

    # connect to the dispaly
    display_bus = displayio.FourWire(
        spi,
        command=tft_dc,
        chip_select=tft_cs,
    )

    display_width = 320
    display_height = 240

    display = adafruit_ili9341.ILI9341(display_bus, width=display_width, height=display_height)

    return display


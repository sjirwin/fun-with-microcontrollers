import board
import os
import wifi

import adafruit_connection_manager
import adafruit_ds3231
import adafruit_ntp

wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

wifi.radio.connect(wifi_ssid, wifi_password)

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0, cache_seconds=3600)

ds3231 = adafruit_ds3231.DS3231(board.I2C())

ds3231.datetime = ntp.datetime

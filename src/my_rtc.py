# Real Time Clock (RTC)
import adafruit_ds3231

import adafruit_datetime as datetime

def current_utc_date(i2c):
    ds3231 = adafruit_ds3231.DS3231(i2c)
    current = ds3231.datetime
    return datetime.date(year=current[0], month=current[1], day=current[2])

def current_utc_time(i2c):
    ds3231 = adafruit_ds3231.DS3231(i2c)
    return ds3231.datetime

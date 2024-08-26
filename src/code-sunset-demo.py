try:
    import datetime
except:
    import adafruit_datetime as datetime

try:
    import board
    import adafruit_ds3231
    i2c = board.I2C()
    ds3231 = adafruit_ds3231.DS3231(i2c)
    current = ds3231.datetime
    date = datetime.date(year=current[0], month=current[1], day=current[2])
except:
    date = datetime.date.today()

print(f"\n{date=}")

from location import Location

# Brooklyn, NY, USA
loc = Location(40.6928, -73.9903, 'America/New_York')
print(f"\n{loc}")

import sun_events

events = sun_events.sunevents(date, loc)

day_length = events.day_length

dawn_astronomical_begin = events.dawn.astronomical_begin
dawn_nautical_begin = events.dawn.nautical_begin
dawn_civil_begin = events.dawn.civil_begin

sunrise = events.sunrise
solar_noon = events.solar_noon
sunset = events.sunset

twilight_civil_end = events.twilight.civil_end
twilight_nautical_end = events.twilight.nautical_end
twilight_astronomical_end = events.twilight.astronomical_end

print(f"")
print(f"{dawn_astronomical_begin}, {dawn_nautical_begin}, {dawn_civil_begin}")
print(f"{sunrise}, {solar_noon}, {sunset}")
print(f"{twilight_civil_end}, {twilight_nautical_end}, {twilight_astronomical_end}")

# representative output if static data is used
# >>> print(f"{dawn_astronomical_begin}, {dawn_nautical_begin}, {dawn_civil_begin}")
# yyyy-mm-dd 04:36:51-04:00 yyyy-mm-dd 05:13:06-04:00 yyyy-mm-dd 05:47:25-04:00
# >>> print(f"{sunrise}, {solar_noon}, {sunset}")
# yyyy-mm-dd 06:14:33-04:00 yyyy-mm-dd 12:58:08-04:00 yyyy-mm-dd 19:41:43-04:00
# >>> print(f"{twilight_civil_end}, {twilight_nautical_end}, {twilight_astronomical_end}")
# yyyy-mm-dd 20:08:51-04:00 yyyy-mm-dd 20:43:11-04:00 yyyy-mm-dd 21:19:26-04:00

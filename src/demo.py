import datetime

import sun_events

# Brooklyn
loc = sun_events.Location(40.6928, -73.9903, 'America/New_York')

date = datetime.date.fromisoformat('2024-08-24')

events = sun_events.sunevents(date, loc)

day_length = events.day_length

dawn_astronomical_twilight_begin = events.dawn.astronomical_twilight_begin
dawn_nautical_twilight_begin = events.dawn.nautical_twilight_begin
dawn_civil_twilight_begin = events.dawn.civil_twilight_begin

sunrise = events.sunrise
solar_noon = events.solar_noon
sunset = events.sunset

civil_twilight_end = events.twilight.civil_twilight_end
nautical_twilight_end = events.twilight.nautical_twilight_end
astronomical_twilight_end = events.twilight.astronomical_twilight_end

print(dawn_astronomical_twilight_begin, dawn_nautical_twilight_begin, dawn_civil_twilight_begin)
print(sunrise, solar_noon, sunset)
print(civil_twilight_end, nautical_twilight_end, astronomical_twilight_end)

# >>> print(dawn_astronomical_twilight_begin, dawn_nautical_twilight_begin, dawn_civil_twilight_begin)
# 2024-08-24 04:36:51-04:00 2024-08-24 05:13:06-04:00 2024-08-24 05:47:25-04:00
# >>> print(sunrise, solar_noon, sunset)
# 2024-08-24 06:14:33-04:00 2024-08-24 12:58:08-04:00 2024-08-24 19:41:43-04:00
# >>> print(civil_twilight_end, nautical_twilight_end, astronomical_twilight_end)
# 2024-08-24 20:08:51-04:00 2024-08-24 20:43:11-04:00 2024-08-24 21:19:26-04:00
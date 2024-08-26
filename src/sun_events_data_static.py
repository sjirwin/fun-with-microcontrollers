try:
    import datetime
except:
    import adafruit_datetime as datetime

from location import Location

def sunrise_sunset_json(date: datetime.date, loc: Location):

    # hard code results for date='2024-08-24' and location=Brooklyn
    api_results = {
        'astronomical_twilight_begin': '2024-08-24T04:36:51-04:00',
        'astronomical_twilight_end': '2024-08-24T21:19:26-04:00',
        'civil_twilight_begin': '2024-08-24T05:47:25-04:00',
        'civil_twilight_end': '2024-08-24T20:08:51-04:00',
        'day_length': 48430,
        'nautical_twilight_begin': '2024-08-24T05:13:06-04:00',
        'nautical_twilight_end': '2024-08-24T20:43:11-04:00',
        'solar_noon': '2024-08-24T12:58:08-04:00',
        'sunrise': '2024-08-24T06:14:33-04:00',
        'sunset': '2024-08-24T19:41:43-04:00'
    }
    return api_results

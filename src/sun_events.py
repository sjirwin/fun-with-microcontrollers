from dataclasses import dataclass
import datetime

# import requests

@dataclass
class Location():
    lat: float
    long: float
    tzid: str


@dataclass
class DawnTimes():
    astronomical_twilight_begin: datetime.datetime
    nautical_twilight_begin: datetime.datetime
    civil_twilight_begin: datetime.datetime


@dataclass
class TwilightTimes():
    civil_twilight_end: datetime.datetime
    nautical_twilight_end: datetime.datetime
    astronomical_twilight_end: datetime.datetime


@dataclass
class SunEvents():
    dawn: DawnTimes
    sunrise: datetime
    solar_noon: datetime
    sunset: datetime
    twilight: TwilightTimes
    day_length: int


def sunevents(date: datetime.date, loc: Location) -> SunEvents:
    data = _sunrise_sunset_json(date, loc)

    dawn = DawnTimes(
        datetime.datetime.fromisoformat(data['astronomical_twilight_begin']),
        datetime.datetime.fromisoformat(data['nautical_twilight_begin']),
        datetime.datetime.fromisoformat(data['civil_twilight_begin'])
    )

    twilight = TwilightTimes(
        datetime.datetime.fromisoformat(data['civil_twilight_end']),
        datetime.datetime.fromisoformat(data['nautical_twilight_end']),
        datetime.datetime.fromisoformat(data['astronomical_twilight_end'])
    )

    return SunEvents(
        dawn,
        datetime.datetime.fromisoformat(data['sunrise']),
        datetime.datetime.fromisoformat(data['solar_noon']),
        datetime.datetime.fromisoformat(data['sunset']),
        twilight,
        data['day_length']
    )


def _sunrise_sunset_json(date: datetime.date, loc: Location):
    # time_data = _call_api_sunrise_sunset_org(str(date), loc.lat, loc.long, loc.tzid)
    # api_results = time_data['results']

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


def _call_api_sunrise_sunset_org(date: str, lat: float, lng: float, tzid: str):
    r = requests.get(
        'https://api.sunrise-sunset.org/json',
        params={
            'lat': lat,
            'lng': lng,
            'tzid': tzid,
            'date': date,
            'formatted': 0
        }
    )

    if r.status_code == 200:
        time_data = r.json()
        api_status = time_data['status']
        if api_status == 'OK':
            return time_data
        else:
            raise RuntimeError(f"api.sunrise-sunset.org failure {api_status=}")
    else:
        raise RuntimeError(f"http request failure {r.status_code=} {r.reason=}")

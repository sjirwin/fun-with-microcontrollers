import datetime

import requests

from location import Location


def sunrise_sunset_json(date: datetime.date, loc: Location):
    time_data = _call_api_sunrise_sunset_org(str(date), loc.lat, loc.long, loc.tzid)
    return time_data['results']


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

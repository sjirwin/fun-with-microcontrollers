import os
import socketpool
import ssl
import wifi

import adafruit_datetime as datetime
import adafruit_requests

from location import Location

# connect to SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())


def sunrise_sunset_json(date: datetime.date, loc: Location):
    time_data = _call_api_sunrise_sunset_org(str(date), loc.lat, loc.long, loc.tzid)
    return time_data['results']


def _call_api_sunrise_sunset_org(date: str, lat: float, lng: float, tzid: str):
    url = f"https://api.sunrise-sunset.org/json?{lat=}&{lng=}&{tzid=}&{date=}&formatted=0"
    resp = requests.get(url)

    status_code = resp.status_code
    reason = resp.reason

    if status_code == 200:
        time_data = resp.json()
        api_status = time_data['status']
        resp.close()
        if api_status == 'OK':
            return time_data
        else:
            raise RuntimeError(f"api.sunrise-sunset.org failure {api_status=}")
    else:
        resp.close()
        raise RuntimeError(f"http request failure {status_code=} {reason=}")

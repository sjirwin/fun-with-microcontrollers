try:
    import datetime
except:
    import adafruit_datetime as datetime

from location import Location

try:
    import sun_events_data_board as events_data
except:
    import sun_events_data_static as events_data


class DawnTimes():
    def __init__(self, astronomical_begin, nautical_begin, civil_begin):
        self.astronomical_begin = astronomical_begin
        self.nautical_begin = nautical_begin
        self.civil_begin = civil_begin
    def __repr__(self):
        return f"{self.__class__.__name__}(astronomical_begin={self.astronomical_begin}, nautical_begin={self.nautical_begin}, civil_begin={self.civil_begin})"


class TwilightTimes():
    def __init__(self, civil_end, nautical_end, astronomical_end):
        self.civil_end = civil_end
        self.nautical_end = nautical_end
        self.astronomical_end = astronomical_end
    def __repr__(self):
        return f"{self.__class__.__name__}(civil_end={self.civil_end}, nautical_end={self.nautical_end}, astronomical_end={self.astronomical_end})"


class SunEvents():
    def __init__(self, dawn, sunrise, solar_noon, sunset, twilight, day_length):
        self.dawn = dawn
        self.sunrise = sunrise
        self.solar_noon = solar_noon
        self.sunset = sunset
        self.twilight = twilight
        self.day_length = day_length
    def __repr__(self):
        return f"{self.__class__.__name__}(dawn={self.dawn!r}, sunrise={self.sunrise}, solar_noon={self.solar_noon}, sunset={self.sunset}, twilight={self.twilight!r}, day_length={self.day_length})"


def sunevents(date: datetime.date, loc: Location) -> SunEvents:
    data = events_data.sunrise_sunset_json(date, loc)

    # short alias for datetime's fromisoformat() function
    fromisoformat = datetime.datetime.fromisoformat

    dawn = DawnTimes(
        fromisoformat(data['astronomical_twilight_begin']),
        fromisoformat(data['nautical_twilight_begin']),
        fromisoformat(data['civil_twilight_begin'])
    )

    twilight = TwilightTimes(
        fromisoformat(data['civil_twilight_end']),
        fromisoformat(data['nautical_twilight_end']),
        fromisoformat(data['astronomical_twilight_end'])
    )

    return SunEvents(
        dawn,
        fromisoformat(data['sunrise']),
        fromisoformat(data['solar_noon']),
        fromisoformat(data['sunset']),
        twilight,
        data['day_length']
    )

import adafruit_datetime as datetime


def durations(events):
    dawn = events.dawn
    twilight = events.twilight

    midnight_today = dawn.astronomical_begin.replace(hour=0, minute=0, second=0)
    midnight_tomorrow = midnight_today + datetime.timedelta(days=1)

    td_mid2astrodawn = dawn.astronomical_begin - midnight_today
    td_astrotwltend2mid = midnight_tomorrow - twilight.astronomical_end

    secs_astrodawn = (dawn.nautical_begin - dawn.astronomical_begin).total_seconds()
    secs_nautdawn = (dawn.civil_begin - dawn.nautical_begin).total_seconds()
    secs_civildawn = (events.sunrise - dawn.civil_begin).total_seconds()

    secs_day = events.day_length

    secs_civiltwilight = (twilight.civil_end - events.sunset).total_seconds()
    secs_nauttwilight = (twilight.nautical_end - twilight.civil_end).total_seconds()
    secs_astrotwilight = (twilight.astronomical_end - twilight.nautical_end).total_seconds()

    # put the various durations in sequence
    durations = [
        td_mid2astrodawn.total_seconds(),
        secs_astrodawn,
        secs_nautdawn,
        secs_civildawn,
        secs_day,
        secs_civiltwilight,
        secs_nauttwilight,
        secs_astrotwilight,
        td_astrotwltend2mid.total_seconds()
    ]

    return durations


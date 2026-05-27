import astral


def getDayLight(date):
    city_name = 'SunriverOR'
    l = astral.Location((city_name, 'USA', 43.8694, -121.4334, 'US/Pacific', 4164))
    return l.sun(date, local=True)
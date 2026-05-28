from astral import LocationInfo
from astral.sun import sun
import pytz


def getDayLight(date):
    location = LocationInfo('Sunriver', 'USA', 'US/Pacific', 43.8694, -121.4334)
    return sun(location.observer, date=date, tzinfo=pytz.timezone('US/Pacific'))

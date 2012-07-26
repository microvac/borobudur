"""
pretty

Formats dates, numbers, etc. in a pretty, human readable format.
"""
__author__ = "S Anand (sanand@s-anand.net)"
__copyright__ = "Copyright 2010, S Anand"
__license__ = "WTFPL"
__translator__ = "VP"

from datetime import datetime, date
from translationstring import TranslationString, TranslationStringFactory

_ = TranslationStringFactory("borobudur")

def _df(seconds, denominator=1, text='', past=True):
    value = str((seconds + denominator/2)/ denominator)
    msg_past = _("${value}${text} lalu", mapping={"value": value, "text": text})
    msg_future = _("${value}${text} lagi", mapping={"value": value, "text": text})
    if past:   return msg_past
    else:      return msg_future

def pretty_time(time, translator):
    '''Returns a pretty formatted date.
    Inputs:
        time is a datetime object or an int timestamp
        asdays is True if you only want to measure days, not seconds
        short is True if you want "1d ago", "2d ago", etc. False if you want
    '''
    result = None

    now = datetime.now()
    if type(time) is int:
        time = datetime.fromtimestamp(time)
    elif not time:
        time = now

    if time > now:
        past = False
        diff = time.__sub__(now)
    else:
        past = True
        diff = now.__sub__(time)
    seconds = diff.seconds
    days    = diff.days

    if days == 0:
        if seconds < 60:        result = _df(seconds, 1, " detik", past)
        elif seconds < 3600:    result = _df(seconds, 60, " menit", past)
        else:                   result = _df(seconds, 3600, " jam", past)
    else:
        date_format = _("%d %B")
        time_format = _("%H:%M")
        year_format = _("%d %B %Y")
        time_string = time.strftime(time_format)
        date_string = time.strftime(date_format)
        if past:
            one_day_msg = _("Kemarin pukul ${time}", mapping={"time": time_string})
        else:
            one_day_msg = _("Besok pukul ${time}", mapping={"time": time_string})
        a_year_msg = _("${date} pukul ${time}", mapping={"date": time.strftime(date_format), "time": time_string})
        more_year_msg = _("${date} pukul ${time}", mapping={"date": time.strftime(year_format), "time": time_string})

        if      days == 1:      result = one_day_msg
        elif    days  < 365:    result = a_year_msg
        else:                   result = more_year_msg

    return translator(result)
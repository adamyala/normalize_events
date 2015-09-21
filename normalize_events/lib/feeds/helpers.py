import sys  
import re
import HTMLParser


def clean_string(descrip):
    reload(sys)
    sys.setdefaultencoding('utf8')
    h = HTMLParser.HTMLParser()
    result = h.unescape(descrip)
    result = result.encode('utf-8').strip()
    result = re.sub('<[^>]*>', '', result)
    result = result.replace('\n', '')
    return result


def clean_address(source):
    if source is not None:
        return re.sub(re.compile("\ *?\((.*?)\)"), "", source)
    else:
        return source


def clean_city(source):
    if source is not None:
        return source.replace(',', '').rstrip()
    else:
        return source


def rows_to_dict(keys, rows):
    result = []
    for row in rows:
        temp_dict = {}
        for key in keys:
            temp_dict[key] = getattr(row, key)
        result.append(temp_dict)
    return result


import datetime
from decimal import *


def pretty_events(events):
    for event in events:
        for key in event:
            if type(event[key]) is datetime.datetime:
                event[key] = re.sub(r'( 0)', ' ', event[key].strftime('%A, %B %d %Y %I:%M %p'))
            if type(event[key]) is Decimal:
                event[key] = float(event[key])
            if key == 'category':
                event[key] = event[key].split(',')
    return events

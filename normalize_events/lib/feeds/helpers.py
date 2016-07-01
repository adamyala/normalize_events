import datetime
import html
import re
from decimal import Decimal


def clean_string(descrip):
    if not descrip:
        return descrip
    result = html.unescape(descrip)
    result = re.sub('<[^>]*>', '', result)
    result = result.replace('\n', '')
    if result is None:
        return ''
    return result


def clean_address(source):
    if source is not None:
        return re.sub(re.compile(" *?\((.*?)\)"), "", source)
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

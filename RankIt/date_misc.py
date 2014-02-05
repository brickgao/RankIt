# -*- coding: utf-8 -*-
import re, datetime

def check_date(s):
    _r = re.compile('^\d\d\d\d-\d\d-\d\d$')
    if not _r.match(s):
        return False, None
    try:
        _ = s.split('-')
        _date = datetime.date(int(_[0]), int(_[1]), int(_[2]))
    except Exception, e:
        return False
    return True, _date

def check_double_date(s1, s2):
    _b1, _date1 = check_date(s1)
    _b2, _date2 = check_date(s2)
    if _b1 and _b2 and _date1 <= _date2:
        return True
    else:
        return False
        
def date_range(s1, s2):
    _b1, _date1 = check_date(s1)
    _b2, _date2 = check_date(s2)
    _ret = []
    while True:
        _ret.append(_date1.strftime('%Y-%m-%d'))
        _date1 += datetime.timedelta(1)
        if _date1 >= _date2:
            break
    return _ret

def date_trans(s):
    _r = re.compile('^\d\d\d\d-\d\d-\d\d \d\d:\d\d$')
    if not _r.match(s):
        return None
    else:
        _date ,_time = s.split(' ')[0], s.split(' ')[1]
        _date = _date.split('-')
        _time = _time.split(':')
        try:
            _datetime = datetime.datetime(int(_date[0]), int(_date[1]), int(_date[2]), int(_time[0]), int(_time[1]))
        except Exception, e:
            return None
        return _datetime

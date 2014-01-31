# -*- coding: utf-8 -*-

import re

def check_time(s):
    _r = re.compile('^\d*:\d*$')
    if _r.match(s) and int(s.split(':')[0]) < 24 and int(s.split(':')[1]) < 60:
        return True
    else:
        return False

def check_double_time(s1, s2):
    if check_time(s1) and check_time(s2):
        _until1 = int(s1.split(':')[0]) * 60 + int(s1.split(':')[1])
        _until2 = int(s2.split(':')[0]) * 60 + int(s2.split(':')[1])
        if _until1 >= _until2:
            return False
        else:
            return True
    else:
        return False

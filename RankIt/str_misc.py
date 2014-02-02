# -*- coding: utf-8 -*-

def trans_str(_s, time_now, time_req=None, rank=None):
    ret = _s
    ret = ret.replace('$[time_now]', time_now)
    if time_req:
        ret = ret.replace('$[time_req]', time_req)
    if rank:
        ret = ret.replace('$[rank]', rank)
    return ret

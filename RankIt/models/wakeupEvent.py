# -*- coding: utf-8 -*-

from RankIt import db

class wakeupEvent(db.Model):
    
    id               = db.Column(db.Integer, primary_key=True)
    last_update_time = db.Column(db.String(80), unique=False)
    total            = db.Column(db.Integer, unique=False)
    switch           = db.Column(db.Integer, unique=False)
    early_ret        = db.Column(db.String(250), unique=False)
    late_ret         = db.Column(db.String(250), unique=False)
    off_ret          = db.Column(db.String(250), unique=False)
    acc_ret_part1    = db.Column(db.String(250), unique=False)
    acc_ret_part2    = db.Column(db.String(250), unique=False)


    def __init__(self, id, last_update_time, total, switch, early_ret, late_ret, off_ret, acc_ret_part1, acc_ret_part2):
        
        self.id               = id
        self.last_update_time = last_update_time
        self.total            = total
        self.switch           = switch
        self.early_ret        = early_ret
        self.off_ret          = off_ret
        self.acc_ret_part1    = acc_ret_part1
        self.acc_ret_part2    = acc_ret_part2

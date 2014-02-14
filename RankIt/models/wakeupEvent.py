# -*- coding: utf-8 -*-

from RankIt import db

class wakeupEvent(db.Model):
    
    id               = db.Column(db.Integer, primary_key=True)
    last_update_time = db.Column(db.String(80), unique=False)
    total            = db.Column(db.Integer, unique=False)
    last_total       = db.Column(db.Integer, unique=False)
    switch           = db.Column(db.Integer, unique=False)
    begin_time       = db.Column(db.String(80), unique=False)
    end_time         = db.Column(db.String(80), unique=False)
    early_ret        = db.Column(db.Text, unique=False)
    late_ret         = db.Column(db.Text, unique=False)
    off_ret          = db.Column(db.Text, unique=False)
    acc_ret          = db.Column(db.Text, unique=False)
    done_ret         = db.Column(db.Text, unique=False)


    def __init__(self, last_update_time, total, begin_time, end_time, early_ret, late_ret, off_ret, acc_ret, done_ret):
        
        self.id               = 1
        self.last_update_time = last_update_time
        self.total            = total
        self.last_total       = total
        self.switch           = 1
        self.begin_time       = begin_time
        self.end_time         = end_time
        self.early_ret        = early_ret
        self.late_ret         = late_ret
        self.off_ret          = off_ret
        self.acc_ret          = acc_ret
        self.done_ret         = done_ret

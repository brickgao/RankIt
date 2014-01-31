# -*- coding: utf-8 -*-

from RankIt import db

class normalEvent(db.Model):
    
    __tablename__   = 'normal_event'
    id              = db.Column(db.Integer, primary_key=True)
    early_ret       = db.Column(db.Text, unique=False)
    late_ret        = db.Column(db.Text, unique=False)
    acc_defualt_ret = db.Column(db.Text, unique=False)
    begin_time      = db.Column(db.DateTime, unique=False)
    end_time        = db.Column(db.DateTime, unique=False)

    
    def __init__(self, id, early_ret, late_ret, acc_defualt_ret, begin_time, end_time):

        self.id              = id
        self.early_ret       = early_ret
        self.late_ret        = late_ret
        self.acc_defualt_ret = acc_defualt_ret
        self.begin_time      = begin_time
        self.end_time        = end_time

# -*- coding: utf-8 -*-

from RankIt import db

class normalEvent(db.Model):
    
    __tablename__   = 'normal_event'
    id              = db.Column(db.Integer, primary_key=True)
    event_name      = db.Column(db.String(250), unique=False)
    early_ret       = db.Column(db.Text, unique=False)
    late_ret        = db.Column(db.Text, unique=False)
    acc_defualt_ret = db.Column(db.Text, unique=False)
    begin_time      = db.Column(db.DateTime, unique=False)
    end_time        = db.Column(db.DateTime, unique=False)

    
    def __init__(self, id, event_name, begin_time, end_time, early_ret, late_ret, acc_defualt_ret):

        self.id              = id
        self.event_name      = event_name
        self.begin_time      = begin_time
        self.end_time        = end_time
        self.early_ret       = early_ret
        self.late_ret        = late_ret
        self.acc_defualt_ret = acc_defualt_ret

# -*- coding: utf-8 -*-

from RankIt import db

class wakeupRec(db.Model):

    id             = db.Column(db.Integer, primary_key=True)
    rank           = db.Column(db.Integer, unique=False)
    lastUpdateTime = db.Column(db.String(80), unique=False)


    def __init__(self, id, rank, lastUpdateTime):
        
        self.id             = id
        self.rank           = rank
        self.lastUpdateTime = lastUpdateTime

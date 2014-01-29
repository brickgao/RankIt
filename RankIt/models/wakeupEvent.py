# -*- coding: utf-8 -*-

from RankIt import db

class wakeupEvent(db.Model):
    
    id             = db.Column(db.Integer, primary_key=True)
    lastUpdateTime = db.Column(db.String(80), unique=False)
    total          = db.Column(db.Integer, unique=False)
    switch         = db.Column(db.Integer, unique=False)
    earlyRet       = db.Column(db.String(250), unique=False)
    lateRet        = db.Column(db.String(250), unique=False)
    offRet         = db.Column(db.String(250), unique=False)
    accRetPart1    = db.Column(db.String(250), unique=False)
    accRetPart2    = db.Column(db.String(250), unique=False)


    def __init__(self, id, lastUpdateTime, total, switch, earlyRet, lateRet, offRet, accRetPart1, accRetPart2):
        
        self.id             = id
        self.lastUpdateTime = lastUpdateTime
        self.total          = total
        self.switch         = switch
        self.earlyRet       = earlyRet
        self.offRet         = offRet
        self.accRetPart1    = accRetPart1
        self.accRetPart2    = accRetPart2

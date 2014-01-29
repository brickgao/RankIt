# -*- coding: utf-8 -*-

from RankIt import db

class normalEvent(db.Model):
    
    __tablename__ = 'normal_event'
    id            = db.Column(db.Integer, primary_key=True)
    earlyRet      = db.Column(db.String(250), unique=False)
    lateRet       = db.Column(db.String(250), unique=False)
    accDefualtRet = db.Column(db.String(250), unique=False)
    beginTime     = db.Column(db.DateTime, unique=False)
    endTime       = db.Column(db.DateTime, unique=False)

    
    def __init__(self, id, earlyRet, lateRet, accDefualtRet, beginTime, endTime):

        self.id            = id
        self.earlyRet      = earlyRet
        self.lateRet       = lateRet
        self.accDefualtRet = accDefualtRet
        self.beginTime     = beginTime
        self.endTime       = endTime

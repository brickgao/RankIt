# -*- coding: utf-8 -*-

from RankIt import db

class normalEventRules(db.Model):

    __tablename__ = 'normal_event_rules'
    _id           = db.Column(db.Integer, primary_key=True)
    eventId       = db.Column(db.Integer, db.ForeignKey('normal_event.id'))
    normalEvent   = db.relationship('normal_event',
                                    primaryjoin='normal_event_rules.eventId == normal_event.id',
                                    backref=db.backref('normal_event_rules'))
    ruleType      = db.Column(db.Integer, unique=False)
    reg           = db.Column(db.String(250), unique=False) # reversed for Reg type
    rangeBegin    = db.Column(db.Integer, unique=False)
    rangeEnd      = db.Column(db.Integer, unique=False)


    def __init__(self, eventId, ruleType, reg, rangeBegin, rangeEnd):

        self.eventId    = eventId
        self.ruleType   = ruleType
        self.reg        = reg
        self.rangeBegin = rangeBegin
        self.rangeEnd   = rangeEnd

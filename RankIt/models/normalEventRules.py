# -*- coding: utf-8 -*-

from RankIt import db

class normalEventRules(db.Model):

    __tablename__ = 'normal_event_rules'
    _id           = db.Column(db.Integer, primary_key=True)
    event_id      = db.Column(db.Integer, db.ForeignKey('normal_event.id'))
    normal_event  = db.relationship('normalEvent',
                                    primaryjoin='normalEventRules.event_id == normalEvent.id',
                                    backref=db.backref('normal_event_rules'))
    rule_type     = db.Column(db.Integer, unique=False)
    reg           = db.Column(db.String(250), unique=False) # reversed for Reg type
    range_begin   = db.Column(db.Integer, unique=False)
    range_end     = db.Column(db.Integer, unique=False)


    def __init__(self, event_id, rule_type, reg, range_begin, range_end):

        self.event_id    = event_id
        self.rule_type   = rule_type
        self.reg         = reg
        self.range_begin = range_begin
        self.range_end   = range_end
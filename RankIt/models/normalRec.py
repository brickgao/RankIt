# -*- coding: utf-8 -*-

from RankIt import db

class normalRec(db.Model):

    __tablename__ = 'normal_rec'
    _id         = db.Column(db.Integer, primary_key=True)
    userId      = db.Column(db.Integer, db.ForeignKey('user.id'))
    eventId     = db.Column(db.Integer, db.ForeignKey('normal_event.id'))
    rank        = db.Column(db.Integer, unique=False)
    user        = db.relationship('user',
                                  primaryjoin='normal_rec.userId == user.id',
                                  backref=db.backref('normal_rec', order_by='normal_rec.userId'))
    normalEvent = db.relationship('normalEvent',
                                  primaryjoin='normal_rec.eventId == normal_event.id',
                                  backref=db.backref('normal_rec'))


    def __init__(self, userId, eventId, rank):
        
        self.userId  = userId
        self.eventId = eventId
        self.rank    = rank
        


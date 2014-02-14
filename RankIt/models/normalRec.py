# -*- coding: utf-8 -*-

from RankIt import db
import hashlib

class normalRec(db.Model):

    __tablename__  = 'normal_rec'
    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id       = db.Column(db.Integer, db.ForeignKey('normal_event.id'))
    rank           = db.Column(db.Integer, unique=False)
    create_time    = db.Column(db.DateTime, unique=False)
    user           = db.relationship('user',
                                     primaryjoin='normalRec.user_id == user.id',
                                     backref=db.backref('normal_rec', order_by='normalRec.user_id'))
    normal_event   = db.relationship('normalEvent',
                                     primaryjoin='normalRec.event_id == normalEvent.id',
                                     backref=db.backref('normal_rec'))


    def __init__(self, user_id, event_id, rank, create_time):
        
        self.user_id     = user_id
        self.event_id    = event_id
        self.rank        = rank
        self.create_time = create_time
        


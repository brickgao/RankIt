# -*- coding: utf-8 -*-

from RankIt import db
import hashlib

class wakeupRec(db.Model):

    __tablename__    = 'wakeup_rec'
    _id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('user.id'))
    rank             = db.Column(db.Integer, unique=False)
    create_date      = db.Column(db.String(80), unique=False)
    create_time      = db.Column(db.String(80), unique=False)
    user             = db.relationship('user',
                                       primaryjoin='wakeupRec.user_id == user.id',
                                       backref=db.backref('wakeup_rec'), order_by='wakeupRec.user_id')


    def __init__(self, user_id, create_date, create_time):
        
        self.user_id          = user_id
        self.create_time      = create_time
        self.create_date      = create_date

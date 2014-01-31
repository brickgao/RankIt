# -*- coding: utf-8 -*-

from RankIt import db
import hashlib

class wakeupRec(db.Model):

    __tablename__    = 'wakeup_rec'
    _id              = db.Column(db.String(250), primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('user.id'))
    rank             = db.Column(db.Integer, unique=False)
    create_time      = db.Column(db.String(80), unique=False)
    user             = db.relationship('user',
                                       primaryjoin='wakeupRec.user_id == user.id',
                                       backref=db.backref('wakeup_rec'), order_by='wakeupRec.user_id')


    def __init__(self, user_id, rank, create_time):
        
        self._id              = hashlib.sha512(create_time + 'and' + str(user_id)).hexdigest()
        self.user_id          = user_id
        self.rank             = rank
        self.create_time      = create_time

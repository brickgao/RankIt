# -*- coding: utf-8 -*-

from RankIt import db

class user(db.Model):
    
    id       = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True) # reversed for new API


    def __init__(self, id, nickname):

        self.id       = id
        self.nickname = nickname

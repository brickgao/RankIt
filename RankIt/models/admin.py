# -*- coding: utf-8 -*-

from RankIt import db

class admin(db.Model):
    
    username = db.Column(db.String(80), primary_key=True)
    passwd   = db.Column(db.String(250), unique=False)


    def __init__(self, username, passwd):
        
        self.username = username
        self.passwd   = passwd

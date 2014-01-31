# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from RankIt import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/RankIt'
app.config['SECRET_KEY'] = 'biubiubiuhaoyu'

db = SQLAlchemy(app)

from models.admin import admin
from models.normalRec import normalRec
from models.normalEvent import normalEvent
from models.normalEventRules import normalEventRules
from models.user import user
from models.wakeupEvent import wakeupEvent
from models.wakeupRec import wakeupRec

db.create_all()

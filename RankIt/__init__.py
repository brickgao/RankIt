# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from RankIt import *
from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)

app = Flask(__name__)

app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASS + '@' + MYSQL_HOST + ':' + str(MYSQL_PORT) + '/' + MYSQL_DB
app.config['SECRET_KEY'] = 'biubiubiuhaoyu'
app.config['SQLALCHEMY_POOL_SIZE'] = 1
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 720
app.config['SQLALCHEMY_POOL_RECYCLE'] = 5

db = SQLAlchemy(app)

from models.admin import admin
from models.normalRec import normalRec
from models.normalEvent import normalEvent
from models.normalEventRules import normalEventRules
from models.user import user
from models.wakeupEvent import wakeupEvent
from models.wakeupRec import wakeupRec

db.create_all()

# -*- coding: utf-8 -*-

from RankIt import *
from flask import Flask, render_template, request, flash, redirect
from models.admin import admin
import hashlib

@app.route('/', methods=['GET'])
def getMainIndex():
    return 'RankIt is running'

@app.route('/init', methods=['GET'])
def getInitIndex():
    adminInfo = admin.query.filter_by(username='admin').first()
    if not adminInfo:
        return render_template('init_begin.html')

@app.route('/init/step1', methods=['GET', 'POST'])
def initStepOne():
    if request.method == 'GET':
        return render_template('init_step_one.html')
    elif request.method == 'POST':
        if request.form['passwd'] != request.form['passwdagain']:
            flash(u'两次密码不一致', 'error')
            return redirect('/init/step1')
        else:
            _ = hashlib.sha512('trick' + request.form['passwd']).hexdigest()
            adminInfo = admin('admin', _)
            db.session.add(adminInfo)
            db.session.commit()
            return 'success'

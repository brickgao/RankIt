# -*- coding: utf-8 -*-

from RankIt import *
from flask import Flask, render_template
from models.admin import admin

@app.route('/manage', methods=['GET', 'POST'])
def get_manage_panel():
    adminInfo = admin.query.filter_by(username='admin').first()
    if not adminInfo:
        return render_template('setup_begin.html')

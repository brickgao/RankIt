# -*- coding: utf-8 -*-

from RankIt import *
from flask import Flask, render_template, request, flash, redirect, abort, session
from models.admin import admin
from models.wakeupEvent import wakeupEvent
from models.user import user
from models.wakeupRec import wakeupRec
import hashlib, time, time_misc, str_misc

@app.route('/', methods=['GET'])
def getMainIndex():
    adminInfo = admin.query.filter_by(username='admin').first()
    wakeupEventInfo = wakeupEvent.query.filter_by(id=1).first()
    if not adminInfo or not wakeupEventInfo:
        return redirect('/init')
    return 'RankIt is running'

@app.route('/init', methods=['GET'])
def getInitIndex():
    adminInfo = admin.query.filter_by(username='admin').first()
    wakeupEventInfo = wakeupEvent.query.filter_by(id=1).first()
    if not adminInfo or not wakeupEventInfo:
        return render_template('init_begin.html')
    else:
        return redirect('/')

@app.route('/init/step1', methods=['GET', 'POST'])
def initStepOne():
    adminInfo = admin.query.filter_by(username='admin').first()
    if adminInfo:
        return redirect('/init/step2')
    if request.method == 'GET':
        return render_template('init_step_one.html')
    elif request.method == 'POST':
        if request.form['passwd'] != request.form['passwdagain']:
            flash(u'两次密码不一致', 'error')
            return redirect('/init/step1')
        elif request.form['passwd'] == '':
            flash(u'请填写密码', 'error')
            return redirect('/init/step1')
        else:
            _ = hashlib.sha512('biu' + request.form['passwd']).hexdigest()
            adminInfo = admin('admin', _)
            db.session.add(adminInfo)
            db.session.commit()
            flash(u'密码设置成功', 'success')
            return redirect('/init/step2')

@app.route('/init/step2', methods=['GET', 'POST'])
def initStepTwo():
    adminInfo = admin.query.filter_by(username='admin').first()
    wakeupEventInfo = wakeupEvent.query.filter_by(id=1).first()
    if not adminInfo:
        flash(u'请先完成第一步，设置密码', 'error')
        return redirect('/init/step1')
    if wakeupEventInfo:
        return redirect('/')
    if request.method == 'GET':
        return render_template('init_step_two.html')
    elif request.method == 'POST':
        begin_time = request.form['begin_time']
        end_time   = request.form['end_time']
        early_ret  = request.form['early_ret']
        late_ret   = request.form['late_ret']
        off_ret    = request.form['off_ret']
        acc_ret    = request.form['acc_ret']
        done_ret   = request.form['done_ret']
        if begin_time == '':
            flash(u'请填写开始时间', 'error')
            return redirect('/init/step2')
        elif end_time == '':
            flash(u'请填写结束时间', 'error')
            return redirect('/init/step2')
        else:
            if time_misc.check_double_time(begin_time, end_time):
                wakeupEventInfo = wakeupEvent('1970-1-1', 0, begin_time, end_time, early_ret, late_ret, off_ret, acc_ret, done_ret)
                db.session.add(wakeupEventInfo)
                db.session.commit()
                return redirect('/init/done')
            else:
                flash(u'请设置合法时间或者结束时间大于开始时间', 'error')
                return redirect('/init/step2')

@app.route('/init/done', methods=['GET'])
def initDone():
    adminInfo = admin.query.filter_by(username='admin').first()
    wakeupEventInfo = wakeupEvent.query.filter_by(id=1).first()
    if adminInfo and wakeupEventInfo:
        if request.method == 'GET':
            return render_template('init_done.html')
    else:
        return redirect('/init/step1')

@app.route('/req', methods=['GET'])
def reflectReq():
    adminInfo = admin.query.filter_by(username='admin').first()
    wakeupEventInfo = wakeupEvent.query.filter_by(id=1).first()
    if not adminInfo or not wakeupEventInfo:
        return redirect('/init')
    _event = request.args.get('event')
    if _event:
        if _event == 'wakeup':
            try:
                _id = int(request.args.get('id'))
            except Exception, e:
                return abort(404)
            userInfo = user.query.filter_by(id=_id).first()
            if not userInfo:
                userInfo = user(_id, '')
                db.session.add(userInfo)
                db.session.commit()
            _date = time.strftime("%Y-%m-%d", time.localtime())
            _date = '2014-2-3'
            _time = time.strftime('%H:%M',time.localtime())
            _time = '13:13'
            # Return transed off_ret if switch is off
            if not wakeupEventInfo.switch:
                _ret = str_misc.trans_str(wakeupEventInfo.off_ret, _time)
                return _ret
            wakeupRecInfo = wakeupRec.query.filter_by(user_id=_id, create_date=_date).first()
            if not wakeupRecInfo:
                # Return early_ret if user hasn't checked and time is earlier than the begin time
                if time_misc.check_double_time(_time, wakeupEventInfo.begin_time):
                    _ret = str_misc.trans_str(wakeupEventInfo.early_ret, _time)
                    return _ret
                # Return late_ret if user hasn't checked and time is later than the begin time
                if time_misc.check_double_time(wakeupEventInfo.end_time, _time):
                    _ret = str_misc.trans_str(wakeupEventInfo.late_ret, _time)
                    return _ret
                # Return acc_ret if all thing is right
                if wakeupEventInfo.last_update_time == _date:
                    _rank = wakeupEventInfo.total + 1
                    wakeupEventInfo.total = _rank
                else:
                    _rank = 1
                    wakeupEventInfo.last_update_time = _date
                    wakeupEventInfo.total = _rank
                wakeupRecInfo = wakeupRec(_id, _rank, _date, _time)
                db.session.add(wakeupRecInfo)
                db.session.commit()
                _ret = str_misc.trans_str(wakeupEventInfo.acc_ret, _time, _time, str(_rank))
                return _ret
            else:
            # Return done_ret if user has checked in wakeupEvent
                _ret = str_misc.trans_str(wakeupEventInfo.done_ret, _time, wakeupRecInfo.create_time, str(wakeupRecInfo.rank))
                return _ret
        if _event == 'normal':
            return 'normal event'
    return abort(404)

@app.route('/manage', methods=['GET'])
def manageIndex():
    return render_template('manage_index.html')

@app.route('/manage/login', methods=['GET', 'POST'])
def manageLogin():
    if request.method == 'GET':
        return render_template('manage_login.html')
    else:
        adminInfo = admin.query.filter_by(username='admin').first()
        _passwd = hashlib.sha512('biu' + request.form['passwd']).hexdigest()
        if _passwd == adminInfo.passwd:
            session['username'] = 'admin'
            flash(u'欢迎回来，admin', 'success')
            return redirect('/manage')
        else:
            flash(u'密码错误', 'error')
            return redirect('/manage/login')

@app.route('/manage/logout')
def manageLogout():
    session.pop('username', None)
    flash(u'登出成功', 'success')
    return redirect('/manage')

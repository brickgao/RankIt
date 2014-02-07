# -*- coding: utf-8 -*-

from RankIt import *
from flask import Flask, render_template, request, flash, redirect, abort, session
from models.admin import admin
from models.wakeupEvent import wakeupEvent
from models.user import user
from models.wakeupRec import wakeupRec
from models.normalEvent import normalEvent
from models.normalRec import normalRec
from models.normalEventRules import normalEventRules
import hashlib, time, time_misc, str_misc, date_misc, datetime

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
                flash(u'时间不合法或者结束时间大于开始时间', 'error')
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
            _time = time.strftime('%H:%M',time.localtime())
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
    if 'username' in session:
        flash(u'你需要登出后在登录', 'error')
        return redirect('/manage')
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

@app.route('/manage/wakeup_event/summary', methods=['GET'])
def wakeupSummary():
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        wakeupEventInfo = wakeupEvent.query.filter_by(id=1).first()
        _date = time.strftime("%Y-%m-%d", time.localtime())
        _info = {}
        _info['switch'] = (lambda x: x and u'开启' or u'关闭')(wakeupEventInfo.switch)
        _info['time_on'] = wakeupEventInfo.begin_time + ' - ' + wakeupEventInfo.end_time
        if _date == wakeupEventInfo.last_update_time:    _info['total'] = str(wakeupEventInfo.total)
        else:                                           _info['total'] = '0'
        return render_template('manage_wakeup_summary.html', info=_info)

@app.route('/manage/wakeup_event/settings', methods=['GET', 'POST'])
def wakeupSettings():
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        wakeupEventInfo = wakeupEvent.query.filter_by(id=1).first()
        if request.method == 'GET':
            _info = {}
            _info['switch']     = wakeupEventInfo.switch
            _info['begin_time'] = wakeupEventInfo.begin_time
            _info['end_time']   = wakeupEventInfo.end_time
            _info['early_ret']  = wakeupEventInfo.early_ret
            _info['late_ret']   = wakeupEventInfo.late_ret
            _info['off_ret']    = wakeupEventInfo.off_ret
            _info['acc_ret']    = wakeupEventInfo.acc_ret
            _info['done_ret']   = wakeupEventInfo.done_ret
            return render_template('manage_wakeup_settings.html', info=_info)
        else:
            switch     = int(str(request.form['switch']))
            begin_time = request.form['begin_time']
            end_time   = request.form['end_time']
            early_ret  = request.form['early_ret']
            late_ret   = request.form['late_ret']
            off_ret    = request.form['off_ret']
            acc_ret    = request.form['acc_ret']
            done_ret   = request.form['done_ret']
            if begin_time == '':
                flash(u'请填写开始时间', 'error')
                return redirect('/manage/wakeup_event/settings')
            elif end_time == '':
                flash(u'请填写结束时间', 'error')
                return redirect('/manage/wakeup_event/settings')
            else:
                if time_misc.check_double_time(begin_time, end_time):
                    wakeupEventInfo.switch     = switch
                    wakeupEventInfo.begin_time = begin_time
                    wakeupEventInfo.end_time   = end_time
                    wakeupEventInfo.early_ret  = early_ret
                    wakeupEventInfo.late_ret   = late_ret
                    wakeupEventInfo.off_ret    = off_ret
                    wakeupEventInfo.acc_ret    = acc_ret
                    wakeupEventInfo.done_ret   = done_ret
                    db.session.commit()
                    flash(u'修改成功', 'success')
                    return redirect('/manage/wakeup_event/summary')
                else:
                    flash(u'时间不合法或者结束时间大于开始时间', 'error')
                    return redirect('/manage/wakeup_event/settings')

@app.route('/manage/wakeup_event/search', methods=['GET'])
def wakeupSearch():
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        return render_template('manage_wakeup_search.html')

@app.route('/manage/wakeup_event/search_result', methods=['GET'])
def wakeupSearchResult():
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        _begin_date = request.args.get('begin_date')
        _end_date   = request.args.get('end_date')
        _id         = request.args.get('id')
        _rank       = request.args.get('rank')
        if _begin_date and _end_date:
            if date_misc.check_double_date(_begin_date, _end_date):
                _info = []
                kargs = {}
                try:
                    if _id != '':       kargs['user_id'] = int(_id)
                    if _rank != '':     kargs['rank'] = int(_rank)
                except Exception, e:
                    flash(u'ID和排名不合法', 'error')
                    return redirect('/manage/wakeup_event/search')
                _t = 1
                for _date in date_misc.date_range(_begin_date, _end_date):
                    _kargs = kargs
                    _kargs['create_date'] = _date
                    wakeupRecInfoList = wakeupRec.query.order_by(wakeupRec.rank).filter_by(**kargs).all()
                    for _ in wakeupRecInfoList:
                        _d = {}
                        _d['id']          = str(_t)
                        _d['create_date'] = _.create_date
                        _d['create_time'] = _.create_time
                        _d['rank']        = str(_.rank)
                        _d['user_id']     = str(_.user_id)
                        _info.append(_d)
                        _t += 1
                return render_template('manage_wakeup_search_result.html', info=_info)
            else:
                flash(u'日期不合法或者截至日期大于起始日期', 'error')
                return redirect('/manage/wakeup_event/search')
        else:
            flash(u'请填写起始日期和截至日期', 'error')
        return redirect('/manage/wakeup_event/search')

@app.route('/manage/normal_event', methods=['GET'])
def normalEventIndex():
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        _info = []
        normalEventInfoList = normalEvent.query.all()
        for e in normalEventInfoList:
            _d = {}
            _d['id']         = str(e.id)
            _d['event_name'] = e.event_name
            _d['time']       = e.begin_time.strftime('%Y-%m-%d %H:%M') + ' - ' + e.end_time.strftime('%Y-%m-%d %H:%M')
            _info.append(_d)
        return render_template('manage_normal_event_index.html', info=_info)

@app.route('/manage/normal_event/new', methods=['GET', 'POST'])
def normalEventNew():
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        if request.method == 'GET':
            return render_template('manage_normal_event_new.html')
        else:
            event_name          = request.form['event_name']
            begin_time          = request.form['begin_time']
            end_time            = request.form['end_time']
            early_ret           = request.form['early_ret']
            late_ret            = request.form['late_ret']
            acc_defualt_ret     = request.form['acc_defualt_ret']
            done_ret            = request.form['done_ret']
            if event_name == '':
                flash(u'请填写时间名称', 'error')
                return redirect('/manage/normal_event/new')
            if begin_time == '':
                flash(u'请填写开始时间', 'error')
                return redirect('/manage/normal_event/new')
            if end_time == '':
                flash(u'请填写结束时间', 'error')
                return redirect('/manage/normal_event/new')
            _begin_time = date_misc.date_trans(begin_time)
            _end_time   = date_misc.date_trans(end_time)
            if not _begin_time:
                flash(u'开始时间不合法', 'error')
                return redirect('/manage/normal_event/new')
            if not _end_time:
                flash(u'结束时间不合法', 'error')
                return redirect('/manage/normal_event/new')
            if _begin_time > _end_time:
                flash(u'开始时间大于结束时间', 'error')
                return redirect('/manage/normal_event/new')
            _l = []
            normalEventInfoList = normalEvent.query.all()
            for e in normalEventInfoList:
                _l.append(e.id)
            _l.sort()
            _id = 1
            while True:
                if _id not in _l:
                    break
                _id += 1
            normalEventInfo = normalEvent(_id, event_name, _begin_time, _end_time, early_ret, late_ret, acc_defualt_ret, done_ret)
            db.session.add(normalEventInfo)
            db.session.commit()
            flash(u'新建事件成功', 'success')
            return redirect('/manage/normal_event')

@app.route('/manage/normal_event/<int:_id>/clear_data', methods=['GET', 'POST'])
def normalEventClearData(_id):
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        normalEventInfo = normalEvent.query.filter_by(id=_id).first()
        if not normalEventInfo:
            return abort(404)
        else:
            if request.method == 'GET':
                _event_name = normalEventInfo.event_name
                return render_template('manage_normal_event_clear_data.html', event_name=_event_name)
            else:
                _confirm = request.form['confirm']
                if _confirm == 'clear data':
                    normalRecInfoList = normalRec.query.filter_by(event_id=_id).all()
                    for e in normalRecInfoList:
                        db.session.delete(e)
                    normalEventInfo.total = 0
                    db.session.commit()
                    flash(u'清空数据成功', 'success')
                    return redirect('/manage/normal_event')
                else:
                    flash(u'确认字符不正确', 'error')
                    return redirect('/manage/normal_event/' + str(_id) + '/clear_data')

@app.route('/manage/normal_event/<int:_id>/delete', methods=['GET', 'POST'])
def normalEventDelete(_id):
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        normalEventInfo = normalEvent.query.filter_by(id=_id).first()
        if not normalEventInfo:
            return abort(404)
        else:
            if request.method == 'GET':
                _event_name = normalEventInfo.event_name
                return render_template('manage_normal_event_delete.html', event_name=_event_name)
            else:
                _confirm = request.form['confirm']
                if _confirm == 'delete':
                    normalRecInfoList = normalRec.query.filter_by(event_id=_id).all()
                    for e in normalRecInfoList:
                        db.session.delete(e)
                    db.session.delete(normalEventInfo)
                    db.session.commit()
                    flash(u'删除成功', 'success')
                    return redirect('/manage/normal_event')
                else:
                    flash(u'确认字符不正确', 'error')
                    return redirect('/manage/normal_event/' + str(_id) + '/delete')

@app.route('/manage/normal_event/<int:_id>', methods=['GET'])
def normalEventView(_id):
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        normalEventInfo = normalEvent.query.filter_by(id=_id).first()
        if not normalEventInfo:
            return abort(404)
        else:
            normalRecInfoList = normalRec.query.order_by(normalRec.rank).filter_by(event_id=_id).all()
            _info = {}
            _info['event_name'] = normalEventInfo.event_name
            _info['id']         = str(_id)
            _info['total']      = normalEventInfo.total
            _info['time']       = normalEventInfo.begin_time.strftime('%Y-%m-%d %H:%M') + ' - ' + \
                                  normalEventInfo.end_time.strftime('%Y-%m-%d %H:%M')
            _list = []
            for e in normalRecInfoList:
                _d = {}
                _d['rank']      = str(e.rank)
                _d['user_id']   = str(e.user_id)
                _d['create_time'] = e.create_time.strftime('%Y-%m-%d %H:%M')
                _list.append(_d)
            _info['user_list'] = _list
            return render_template('manage_normal_event_view.html', info=_info)

@app.route('/manage/normal_event/<int:_id>/edit', methods=['GET', 'POST'])
def normalEventEdit(_id):
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        normalEventInfo = normalEvent.query.filter_by(id=_id).first()
        if not normalEventInfo:
            return abort(404)
        else:
            if request.method == 'GET':
                _info = {}
                _info['event_name']      = normalEventInfo.event_name
                _info['early_ret']       = normalEventInfo.early_ret
                _info['late_ret']        = normalEventInfo.late_ret
                _info['acc_defualt_ret'] = normalEventInfo.acc_defualt_ret
                _info['done_ret']        = normalEventInfo.done_ret
                _info['begin_time']      = normalEventInfo.begin_time.strftime('%Y-%m-%d %H:%M')
                _info['end_time']        = normalEventInfo.end_time.strftime('%Y-%m-%d %H:%M')
                return render_template('manage_normal_event_edit.html', info=_info)
            else:
                event_name          = request.form['event_name']
                begin_time          = request.form['begin_time']
                end_time            = request.form['end_time']
                early_ret           = request.form['early_ret']
                late_ret            = request.form['late_ret']
                acc_defualt_ret     = request.form['acc_defualt_ret']
                done_ret            = request.form['done_ret']
                if event_name == '':
                    flash(u'请填写时间名称', 'error')
                    return redirect('/manage/normal_event/' + str(_id) + '/edit')
                if begin_time == '':
                    flash(u'请填写开始时间', 'error')
                    return redirect('/manage/normal_event/' + str(_id) + '/edit')
                if end_time == '':
                    flash(u'请填写结束时间', 'error')
                    return redirect('/manage/normal_event/' + str(_id) + '/edit')
                _begin_time = date_misc.date_trans(begin_time)
                _end_time   = date_misc.date_trans(end_time)
                if not _begin_time:
                    flash(u'开始时间不合法', 'error')
                    return redirect('/manage/normal_event/' + str(_id) + '/edit')
                if not _end_time:
                    flash(u'结束时间不合法', 'error')
                    return redirect('/manage/normal_event/' + str(_id) + '/edit')
                if _begin_time > _end_time:
                    flash(u'开始时间大于结束时间', 'error')
                    return redirect('/manage/normal_event/' + str(_id) + '/edit')
                normalEventInfo.event_name      = event_name
                normalEventInfo.early_ret       = early_ret
                normalEventInfo.late_ret        = late_ret
                normalEventInfo.acc_defualt_ret = acc_defualt_ret
                normalEventInfo.done_ret        = done_ret
                normalEventInfo.begin_time      = _begin_time
                normalEventInfo.end_time        = _end_time
                db.session.commit()
                flash(u'修改事件成功', 'success')
                return redirect('/manage/normal_event')

@app.route('/manage/normal_event/<int:_id>/rules', methods=['GET'])
def normalEventRulesIndex(_id):
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        normalEventInfo = normalEvent.query.filter_by(id=_id).first()
        if not normalEventInfo:
            return abort(404)
        else:
            _info = {}
            _info['event_id']   = str(_id)
            _info['event_name'] = normalEventInfo.event_name
            _list = []
            normalEventRulesInfoList = normalEventRules.query.filter_by(event_id=_id).all()
            for e in normalEventRulesInfoList:
                _d = {}
                _d['id']         = e.id
                if rule_type == 'range':
                    _id['range'] = str(e.range_begin) + ' - ' + str(e.range_end)
                _list.append(_d)
            _info['rules_list'] = _list
            return render_template('manage_normal_event_rules_index.html', info=_info)

@app.route('/manage/normal_event/<int:_id>/rules/new', methods=['GET', 'POST'])
def normalEventRulesIndex(_id):
    if not 'username' in session:
        flash(u'请先登录', 'error')
        return redirect('/manage/login')
    else:
        normalEventInfo = normalEvent.query.filter_by(id=_id).first()
        if not normalEventInfo:
            return abort(404)
        else:

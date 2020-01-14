from flask import Flask, render_template, flash, request, redirect, url_for, jsonify, json, session
from flask_login import login_user, logout_user, login_required
from app import app, lm
from app.forms import VWR_Admin, LoginForm
from cms_admin import getUsers, getTenants, getUserCoSpaces, createTenant, getSpaces, createSpace, createAccessMethod, getCoSpaceDetails, getCalls, getParticipants, getCallDetails, addUserToCospace, deleteCall, deleteSpace, getAccessMethod, getAccessMethodDetails, verifyUser
from app.extensions import get_user, validate_user, add_users
import pprint as pp
from config import Config
import time
from datetime import datetime
from .user import User


app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
#app.add_url_rule('/login', 'login', ldap.login, methods=['GET', 'POST'])
#LDAP_HOST = Config.LDAP_HOST

# - - - Routes - - -

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    tenant_list = getTenants()
    form = VWR_Admin()
    form.tenants.choices = tenant_list
    if request.method == 'POST':
        #userJid = request.form['users']
        #user_name =  dict(form.users.choices).get(form.users.data)
        tenant_id = request.form['tenants']
        tenant_name =  dict(form.tenants.choices).get(form.tenants.data)
        call_id_list = getCalls(tenant_id)
        calls = len(call_id_list)
        active_call_list = []
        waiting_call_list = []
        active_list = []
        waiting_list = []
        active_dur_list = []
        waiting_dur_list = []
        active_space_list = []
        waiting_space_list = []
        #following only needed for active calls
        uri_list = []
        passcode_list = []
        link_list = []
        owner_list = []
        if calls > 0:
            for call_id in call_id_list:
                participant_name, participant_id = getParticipants(call_id)
                duration_mins, coSpace_id = getCallDetails(call_id)
                link, callId, ownerJid = getCoSpaceDetails(coSpace_id)
                access_method_id = getAccessMethod(coSpace_id)
                uri, passcode, link = getAccessMethodDetails(coSpace_id, access_method_id)
                if len(ownerJid) > 0:
                    active_list.append(participant_name)
                    active_dur_list.append(duration_mins)
                    active_space_list.append(coSpace_id)
                    active_call_list.append(call_id)
                    owner_list.append(ownerJid)
                    uri_list.append(uri)
                    passcode_list.append(passcode)
                    link_list.append(link)
                else:
                    waiting_list.append(participant_name)
                    waiting_dur_list.append(duration_mins)
                    waiting_space_list.append(coSpace_id)
                    waiting_call_list.append(call_id)
        active_calls = len(active_call_list)
        waiting_calls = len(waiting_call_list)
        return render_template('vwr_main.html', tenant=tenant_name, active_calls=active_calls, waiting_calls=waiting_calls, waiting=zip(waiting_list,waiting_call_list,waiting_dur_list,waiting_space_list), active=zip(active_list,active_call_list,active_dur_list,active_space_list,uri_list,passcode_list,link_list, owner_list))
    elif request.method == 'GET':
        return render_template('index.html', form = form)

@app.route("/test")
@login_required
def test():
    return render_template('test.html')

@app.route("/patient", methods=['GET', 'POST'])
def patient():
    #users_list = getUsers()
    tenant_list = getTenants()
    pp.pprint (tenant_list)
    #createTenant("Test1")
    #getSpaces("Adam")
    form = VWR_Admin()
    #form.users.choices = users_list
    form.tenants.choices = tenant_list
    if request.method == 'POST':
        #user_id = request.form['users']
        tenant_id = request.form['tenants']
        tenant_name =  dict(form.tenants.choices).get(form.tenants.data)
        now = datetime.utcnow()
        timestamp_now = time.mktime(now.timetuple()) + now.microsecond * 1e-6
        timestamp_str = str(timestamp_now).rsplit('.',1)[1]
        space_name = tenant_name.replace(" ", "_") + "_" + timestamp_str
        coSpace_id = createSpace(space_name, tenant_id)
        link, callId, ownerJid = getCoSpaceDetails(coSpace_id)
        createAccessMethod(coSpace_id, callId, space_name)
        #print (user_id)
        #getUserCoSpaces(user_id)
        return redirect(link)
    elif request.method == 'GET':
        return render_template('index.html', form = form)

@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    form = VWR_Admin()
    users_list = getUsers()
    result = add_users(users_list)
    form.users.choices = users_list
    tenant_list = getTenants()
    form.tenants.choices = tenant_list
    if request.method == 'POST':
        userJid = request.form['users']
        user_name =  dict(form.users.choices).get(form.users.data)
        tenant_id = request.form['tenants']
        tenant_name =  dict(form.tenants.choices).get(form.tenants.data)
        call_id_list = getCalls(tenant_id)
        calls = len(call_id_list)
        active_call_list = []
        waiting_call_list = []
        active_list = []
        waiting_list = []
        active_dur_list = []
        waiting_dur_list = []
        active_space_list = []
        waiting_space_list = []
        #following only needed for active calls
        uri_list = []
        passcode_list = []
        link_list = []
        owner_list = []
        if calls > 0:
            for call_id in call_id_list:
                participant_name, participant_id = getParticipants(call_id)
                duration_mins, coSpace_id = getCallDetails(call_id)
                link, callId, ownerJid = getCoSpaceDetails(coSpace_id)
                access_method_id = getAccessMethod(coSpace_id)
                uri, passcode, link = getAccessMethodDetails(coSpace_id, access_method_id)
                if len(ownerJid) > 0:
                    active_list.append(participant_name)
                    active_dur_list.append(duration_mins)
                    active_space_list.append(coSpace_id)
                    active_call_list.append(call_id)
                    owner_list.append(ownerJid)
                    uri_list.append(uri)
                    passcode_list.append(passcode)
                    link_list.append(link)
                else:
                    waiting_list.append(participant_name)
                    waiting_dur_list.append(duration_mins)
                    waiting_space_list.append(coSpace_id)
                    waiting_call_list.append(call_id)
        active_calls = len(active_call_list)
        waiting_calls = len(waiting_call_list)
        return render_template('vwr_main.html', tenant=tenant_name, user=user_name, userJid=userJid, active_calls=active_calls, waiting_calls=waiting_calls, waiting=zip(waiting_list,waiting_call_list,waiting_dur_list,waiting_space_list), active=zip(active_list,active_call_list,active_dur_list,active_space_list,uri_list,passcode_list,link_list, owner_list))
    elif request.method == 'GET':
        return render_template('vwr.html', form = form)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')

@app.route("/addUser")
def addUser():
    userJid = request.args.get('userJid', None)
    coSpace_id = request.args.get('coSpace_id', None)
    addUserToCospace(coSpace_id, userJid)

### login routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        success, fullName = verifyUser(username)
        if success:
            user_obj, result = validate_user(username, form.password.data, fullName)
            if result == "success":
                session['name'] = fullName
                login_user(user_obj)
                flash("Logged in successfully!", category='success')
                return redirect(request.args.get("next") or url_for("home"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)

@app.route('/logout')
def logout():
    print ("logging out user")
    logout_user()
    return redirect(url_for('login'))

@lm.user_loader
def load_user(username):
    user_obj = get_user(username)
    return user_obj
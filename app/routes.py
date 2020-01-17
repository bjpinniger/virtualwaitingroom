from flask import Flask, render_template, flash, request, redirect, url_for, jsonify, json, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, lm
from app.forms import VWR_Admin, LoginForm, Endpoint, EnterEndpoint, AdminSettings, Admin
from cms import CMS
from app.extensions import Extensions 
import pprint as pp
from config import Config
import time
from datetime import datetime
from .user import User

app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# - - - Routes - - -

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    session['logo'] = Config.LOGO
    tenant_list = CMS.getTenants()
    if current_user.username == "admin":
        form = Admin()
        template = "admin.html"
        settings = Extensions.get_admin_settings()
        space_list = []
        for tenant in tenant_list:
            tenant_name = tenant[1]
            space_filter = tenant_name.replace(" ", "_")
            print (space_filter)
            space_list = CMS.getSpaces(space_filter, space_list)
        form.spaces.choices = space_list
        try:
            guestCLP = settings['guest_CLP']
        except:
            guestCLP = ""
        try:
            hostCLP = settings['host_CLP']
        except:
            hostCLP = ""
    else:
        form = VWR_Admin()
        template = "index.html"
    form.tenants.choices = tenant_list
    if request.method == 'POST':
        if "tenants" in request.form:
            tenant_id = request.form['tenants']
        if "create_tenant" in request.form:
            print ("create_tenant")
            CMS.createTenant(request.form['tenant'], settings['guest_CLP'])
        elif "delete_tenant" in request.form:
            print ("delete_tenant")
            CMS.deleteTenant(tenant_id)
        elif "create_guest_CLP" in request.form:
            print ("create_guest_CLP")
            Guest_CLP_ID = CMS.createGuest_CLP("guest")
            Extensions.update_admin_settings(Guest_CLP_ID, "")
        elif "create_host_CLP" in request.form:
            print ("create_host_CLP")
            Host_CLP_ID = CMS.createHost_CLP("host")
            Extensions.update_admin_settings("", Host_CLP_ID)
        elif "delete_spaces" in request.form:
            print ("delete_spaces")
            spaceIdList = request.form.getlist('spaces')
            CMS.deleteSpaces(spaceIdList)
        if current_user.username == "admin":
            return redirect(url_for('home'))
        else:
            return redirect(url_for('vwr', tenant_id=tenant_id))
    elif request.method == 'GET':
        if current_user.username == "admin":
            return render_template(template, form = form, guestCLP = guestCLP, hostCLP = hostCLP)
        else:
            return render_template(template, form = form)

@app.route("/patient", methods=['GET', 'POST'])
def patient():
    session['logo'] = Config.LOGO
    tenant_list = CMS.getTenants()
    form = VWR_Admin()
    form.tenants.choices = tenant_list
    if request.method == 'POST':
        tenant_id = request.form['tenants']
        tenant_name =  dict(form.tenants.choices).get(form.tenants.data)
        now = datetime.utcnow()
        timestamp_now = time.mktime(now.timetuple()) + now.microsecond * 1e-6
        timestamp_str = str(timestamp_now).rsplit('.',1)[1]
        space_name = tenant_name.replace(" ", "_") + "_" + timestamp_str
        coSpace_id = CMS.createSpace(space_name, tenant_id)
        link, callId, ownerJid = CMS.getCoSpaceDetails(coSpace_id)
        CMS.createAccessMethod(coSpace_id, callId, space_name)
        return redirect(link)
    elif request.method == 'GET':
        return render_template('index.html', form = form)

@app.route("/vwr", methods=['GET', 'POST'])
@login_required
def vwr():
    tenant_id = request.args.get('tenant_id', None)
    tenant_name = CMS.getTenant(tenant_id)
    Callback = Extensions.get_settings(current_user.username)
    form = EnterEndpoint()
    form.endpoint.data = Callback
    form.tenant_id.data = tenant_id
    call_id_list = CMS.getCalls(tenant_id)
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
            participant_name, participant_id, activator_name = CMS.getParticipants(call_id)
            duration_mins, coSpace_id = CMS.getCallDetails(call_id)
            link, callId, ownerJid = CMS.getCoSpaceDetails(coSpace_id)
            access_method_id = CMS.getAccessMethod(coSpace_id)
            uri, passcode, link = CMS.getAccessMethodDetails(coSpace_id, access_method_id)
            main_link, drop_link = link.split("/invited")
            if len(ownerJid) > 0:
                active_list.append(participant_name)
                active_dur_list.append(duration_mins)
                active_space_list.append(coSpace_id)
                active_call_list.append(call_id)
                owner_list.append(ownerJid)
                uri_list.append(uri)
                passcode_list.append(passcode)
                link_list.append(main_link)
            else:
                waiting_list.append(participant_name)
                waiting_dur_list.append(duration_mins)
                waiting_space_list.append(coSpace_id)
                waiting_call_list.append(call_id)
    active_calls = len(active_call_list)
    waiting_calls = len(waiting_call_list)
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
        else:
            print ("callid: " + request.form['callid'])
            if request.form['callid'] is not None:
                participant_name, participant_id, activator_name = CMS.getParticipants(request.form['callid'])
                print ("activator: " + activator_name)
                if activator_name == "":
                    CMS.addParticipantToCall(request.form['callid'], request.form['endpoint'])
    return render_template('vwr.html', form=form, tenant=tenant_name, active_calls=active_calls, waiting_calls=waiting_calls, waiting=zip(waiting_list,waiting_call_list,waiting_dur_list,waiting_space_list), active=zip(active_list,active_call_list,active_dur_list,active_space_list,uri_list,passcode_list,link_list, owner_list))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.username == "admin":
        form = AdminSettings()
        template = "settings_admin.html"
    else:
        Callback = Extensions.get_settings(current_user.username)
        form = Endpoint()
        form.endpoint.data = Callback
        template = "settings.html"
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template(template, form = form)
        else:
            if current_user.username == "admin":
                success = Extensions.change_pwd(current_user.username, request.form['current_password'], request.form['password'])
                if success:
                    flash("Password changed successfully!", category='success')
                    return redirect(url_for('home'))
                else:
                    flash("Wrong password!", category='error')
                    return render_template(template, form = form)
            else:
                result = Extensions.update_settings(current_user.username, request.form['endpoint'])
                print (result)
                return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template(template, form = form)

@app.route("/sendcmd", methods=['GET', 'POST'])
def sendcmd():
    if request.method == 'POST':
        command = request.form['command']
        cmd, call_id = command.split('_')
        coSpace_id = request.form['space_id']
        if cmd == "Drop":
            print ("delete call: " + call_id)
            CMS.deleteCall(call_id)
            CMS.deleteSpace(coSpace_id)
        else:
            userJid = current_user.username
            CMS.addUserToCospace(coSpace_id, userJid)
        data = {
            "result": "success"
        }
        response = app.response_class(response=json.dumps(data),
                                status=200,
                                mimetype='application/json')
        return response

### login routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        if username == "admin":
            fullName = "Administrator"
            user_obj, result = Extensions.validate_user(username, form.password.data, fullName)
        else:
            success, fullName = CMS.verifyUser(username)
            if success:
                user_obj, result = Extensions.validate_user(username, form.password.data, fullName)
        if result == "success" or result == "changePWD":
            session['name'] = fullName
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            if result == "changePWD":
                return redirect(url_for("settings"))
            else:
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
    user_obj = Extensions.get_user(username)
    return user_obj
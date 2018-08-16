from endpoints import get_endpoints, get_IPaddress
from codec import get_presets, send_preset, deactivate_standby
from flask import Flask, session, render_template, flash, request, redirect, url_for
from app import app
from app.forms import SelectEndpoint
from config import Config

app.config.from_object(Config)

app.secret_key = Config.SECRET_KEY
EP_filter = Config.FILTER

# - - - Routes - - -

@app.route("/", methods=['GET', 'POST'])
def index():
    """Main page"""
    DeviceNames, result = get_endpoints(EP_filter)
    if result != "Success":
        return render_template('error.html', result=result)
    else:
        form = SelectEndpoint()
        form.endpoint.choices = DeviceNames
        if request.method == 'POST':
            if form.validate() == False:
                flash('Please select an endpoint to continue.')
                return render_template('index.html', form = form)
            else:
                device = request.form['endpoint']
                IP, result = get_IPaddress(device)
                if result == "Success":
                    return redirect(url_for('presets', device=device, IP=IP))
                else:
                    return render_template('error.html', result=result)
        elif request.method == 'GET':
            return render_template('index.html', form = form)  

@app.route("/presets")
def presets():
    device = request.args.get('device', None)
    IP = request.args.get('IP', None)
    preset_result = request.args.get('result', None)
    name_list, id_list, result = get_presets(IP)
    if result == "Success":
        result = preset_result
        return render_template('presets.html', presets=zip(id_list,name_list), device=device, IP=IP, result=result)
    else:
        return render_template('error.html', result=result)

@app.route("/sendpreset")
def sendpreset():
    id = request.args.get('id', None)
    name = request.args.get('name', None)
    device = request.args.get('device', None)
    IP = request.args.get('IP', None)
    print ("user selected id: " + str(id))
    result = deactivate_standby(IP)
    if result != "Success":
        return render_template('error.html', result=result)
    result = send_preset(id, IP)
    if result != "Success":
        return render_template('error.html', result=result)
    else:
        result = result + ": " + name + " sent"
    return redirect(url_for('presets', device=device, IP=IP, result=result))

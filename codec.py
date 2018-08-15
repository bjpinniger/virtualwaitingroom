import requests
from xml.etree import ElementTree as ET
from endpoints import get_endpoints, get_IPaddress
from flask import Flask, session, render_template, flash, request, redirect, url_for
from app import app
from base64 import b64encode
from config import Config

app.config.from_object(Config)

username = Config.USERNAME
password = Config.PASSWORD

authTokenBytes = b64encode(bytes(username + ':' + password, "utf-8"))
authToken = authTokenBytes.decode('utf-8')


def get_presets(IP):
    url = "http://%s/putxml" % IP
    payload = "<Command>\n\t<Camera>\n\t\t<Preset>\n\t\t\t<List>\n\t\t\t\t<CameraId>1</CameraId>\n\t\t\t</List>\n\t\t</Preset>\n\t</Camera>\n</Command>"
    headers = {
        'Content-Type': "text/xml",
        'Authorization': "Basic %s" % authToken,
        'Cache-Control': "no-cache"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print (response)
    name_list = list()
    id_list = list()
    if(response.status_code == 200):
        result = "OK"
        tree=ET.fromstring(response.text)
        for name in tree.findall('.//Preset/Name'):
            name_list.append(name.text)
        for id in tree.findall('.//Preset/PresetId'):
            id_list.append(id.text)
    else:
        result = "No presets defined"
    return name_list, id_list, result


def send_preset(id, IP):
    url = "http://%s/putxml" % IP
    # bring codec out of standby state
    payload = "<Command>\r\n\t<Standby>\r\n\t\t<Deactivate/>\r\n\t</Standby>\r\n</Command>"
    headers = {
        'Content-Type': "text/xml",
        'Authorization': "Basic %s" % authToken,
        'Cache-Control': "no-cache",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    payload = "<Command>\n\t<Camera>\n\t\t<Preset>\n\t\t\t<Activate>\n\t\t\t\t<PresetId>%s</PresetId>\n\t\t\t</Activate>\n\t\t</Preset>\n\t</Camera>\n</Command>" % str(id)
    response = requests.request("POST", url, data=payload, headers=headers)
    if 'status="OK"' in response.text:
        result = "Success"
    else:
        result = "Failure: " + response.text
    return result
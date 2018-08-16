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
    name_list = list()
    id_list = list()
    url = "http://%s/putxml" % IP
    payload = "<Command>\n\t<Camera>\n\t\t<Preset>\n\t\t\t<List>\n\t\t\t\t<CameraId>1</CameraId>\n\t\t\t</List>\n\t\t</Preset>\n\t</Camera>\n</Command>"
    headers = {
        'Content-Type': "text/xml",
        'Authorization': "Basic %s" % authToken,
        'Cache-Control': "no-cache"
        }
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            result = "Success"
            tree=ET.fromstring(response.text)
            for name in tree.findall('.//Preset/Name'):
                name_list.append(name.text)
            for id in tree.findall('.//Preset/PresetId'):
                id_list.append(id.text)
        else:
            result = "No presets defined"
    except requests.exceptions.ConnectionError:
        name_list = list()
        id_list = list()
        result = "Failed to connect to the codec @ IP: " + IP
    return name_list, id_list, result

def deactivate_standby(IP):
    url = "http://%s/putxml" % IP
    payload = "<Command>\r\n\t<Standby>\r\n\t\t<Deactivate/>\r\n\t</Standby>\r\n</Command>"
    headers = {
        'Content-Type': "text/xml",
        'Authorization': "Basic %s" % authToken,
        'Cache-Control': "no-cache",
        }
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            result = "Success"
        else:
            result = "Failure: Status Code " + str(response.status_code)
    except requests.exceptions.ConnectionError:
        result = "Failed to connect to the codec @ IP: " + IP
    return result

def send_preset(id, IP):
    url = "http://%s/putxml" % IP
    payload = "<Command>\n\t<Camera>\n\t\t<Preset>\n\t\t\t<Activate>\n\t\t\t\t<PresetId>%s</PresetId>\n\t\t\t</Activate>\n\t\t</Preset>\n\t</Camera>\n</Command>" % str(id)
    headers = {
        'Content-Type': "text/xml",
        'Authorization': "Basic %s" % authToken,
        'Cache-Control': "no-cache",
        }
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            result = "Success"
        else:
            result = "Failure: Status Code " + str(response.status_code)
    except requests.exceptions.ConnectionError:
        result = "Failed to connect to the codec @ IP: " + IP
    return result
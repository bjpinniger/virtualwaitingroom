import requests
from xml.etree import ElementTree as ET

url = "http://192.168.0.17/putxml"

payload = "<Command>\n\t<Camera>\n\t\t<Preset>\n\t\t\t<List>\n\t\t\t\t<CameraId>1</CameraId>\n\t\t\t</List>\n\t\t</Preset>\n\t</Camera>\n</Command>"
headers = {
    'Content-Type': "text/xml",
    'Authorization': "Basic RGVtbzpDMXNjbzEyMzQ1",
    'Cache-Control': "no-cache",
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

name_list = list()
id_list = list()

tree=ET.fromstring(response.text)
for name in tree.findall('.//Preset/Name'):
    result = name.text
    name_list.append(result)
    #print (result)

print (name_list)

for id in tree.findall('.//Preset/PresetId'):
    result = id.text
    id_list.append(result)
    #print (result)

print  (id_list)
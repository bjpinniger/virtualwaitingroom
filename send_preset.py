import requests

url = "http://192.168.0.17/putxml"

payload = "<Command>\n\t<Camera>\n\t\t<Preset>\n\t\t\t<Activate>\n\t\t\t\t<PresetId>1</PresetId>\n\t\t\t</Activate>\n\t\t</Preset>\n\t</Camera>\n</Command>"
headers = {
    'Content-Type': "text/xml",
    'Authorization': "Basic RGVtbzpDMXNjbzEyMzQ1",
    'Cache-Control': "no-cache",
    'Postman-Token': "07c8025a-ff2f-4a1c-bf10-a7e49df2f3a7"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
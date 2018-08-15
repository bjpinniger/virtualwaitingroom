import requests
import xml.etree.ElementTree as ET
import urllib3
from config import Config
from app import app

urllib3.disable_warnings()

app.config.from_object(Config)
cucm = Config.CUCM
version = Config.VERSION
user = Config.CUCM_USER
pwd = Config.CUCM_PWD


def get_endpoints(filter):
    soaprequest = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/' + version + '"><soapenv:Header /><soapenv:Body><ns:listPhone>#<searchCriteria><description>%s</description></searchCriteria><returnedTags><name></name><description></description></returnedTags></ns:listPhone></soapenv:Body></soapenv:Envelope>' % filter
    soapheaders = {'Content-type':'text/xml', 'SOAPAction':'CUCM:DB ver=%s listPhone' % version}
    AXLRequest = requests.post('https://%s:8443/axl/' % cucm, data = soaprequest, headers = soapheaders, verify = False, auth=(user,pwd)) 
    root = ET.fromstring(AXLRequest.text)

    print (AXLRequest.text)

    DeviceNames = [(phone.find('name').text, phone.find('description').text) for phone in root.iter('phone')]
    return DeviceNames

def get_IPaddress(filter):
    url = 'https://%s:8443/realtimeservice2/services/RISService70?wsdl' % cucm
    soaprequest = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://schemas.cisco.com/ast/soap"><soapenv:Header /><soapenv:Body><soap:selectCmDevice><soap:StateInfo></soap:StateInfo><soap:CmSelectionCriteria><soap:MaxReturnedDevices>100</soap:MaxReturnedDevices><soap:DeviceClass>Any</soap:DeviceClass><soap:Model>255</soap:Model><soap:Status>Any</soap:Status><soap:NodeName></soap:NodeName><soap:SelectBy>Name</soap:SelectBy><soap:SelectItems><soap:item><soap:Item>%s</soap:Item></soap:item></soap:SelectItems><soap:Protocol>Any</soap:Protocol><soap:DownloadStatus>Any</soap:DownloadStatus></soap:CmSelectionCriteria></soap:selectCmDevice></soapenv:Body></soapenv:Envelope>' % filter
    soapheaders = {'Content-type':'text/xml'}
    SOAPRequest = requests.post('https://%s:8443/realtimeservice2/services/RISService70/' % cucm, data = soaprequest, headers = soapheaders, verify = False, auth=(user,pwd))
    ns = {
        'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
        'ns1': 'http://schemas.cisco.com/ast/soap'
        }
    root = ET.fromstring(SOAPRequest.text)
    devices = root.find('.//ns1:TotalDevicesFound', ns)
    if int(devices.text) > 0:
        IP_address = root.find('.//ns1:IP', ns)
        IP = IP_address.text
        result = "Success"
    else:
        IP = ""
        result = "Device not registered!"
    return IP, result





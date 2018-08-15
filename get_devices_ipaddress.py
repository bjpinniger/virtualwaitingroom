import requests
import xml.etree.ElementTree as ET
import urllib3

urllib3.disable_warnings()

filter = "SIP*"
cucm = "10.10.20.1"
user = "administrator"
pwd = "ciscopsdt"

url = 'https://' + cucm + ':8443/realtimeservice2/services/RISService70?wsdl'
soaprequest = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://schemas.cisco.com/ast/soap"><soapenv:Header /><soapenv:Body><soap:selectCmDevice><soap:StateInfo></soap:StateInfo><soap:CmSelectionCriteria><soap:MaxReturnedDevices>100</soap:MaxReturnedDevices><soap:DeviceClass>Any</soap:DeviceClass><soap:Model>255</soap:Model><soap:Status>Any</soap:Status><soap:NodeName></soap:NodeName><soap:SelectBy>Name</soap:SelectBy><soap:SelectItems><soap:item><soap:Item>' + filter + '</soap:Item></soap:item></soap:SelectItems><soap:Protocol>Any</soap:Protocol><soap:DownloadStatus>Any</soap:DownloadStatus></soap:CmSelectionCriteria></soap:selectCmDevice></soapenv:Body></soapenv:Envelope>'
soapheaders = {'Content-type':'text/xml'}
SOAPRequest = requests.post('https://' + cucm + ':8443/realtimeservice2/services/RISService70/', data = soaprequest, headers = soapheaders, verify = False, auth=(user,pwd))

ns = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'ns1': 'http://schemas.cisco.com/ast/soap'
    }

root = ET.fromstring(SOAPRequest.text)
#Name = root.find('.//ns1:CmDevices/ns1:item/ns1:Name', ns)
#Names = [(Name.text) for Name in Name_list]
IP_address = root.find('.//ns1:IP', ns)
print (IP_address.text)


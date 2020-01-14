import requests, base64, json, xmltodict
from config import Config
from app import app
import Canopy
import pprint as pp
import urllib3

urllib3.disable_warnings()

app.config.from_object(Config)
CMS_IP = Config.CMS_IP
user = Config.CMS_USER
pwd = Config.CMS_PWD
host_CLP = Config.host_CLP

a = Canopy.Acano(CMS_IP, user, pwd)
auth = "Basic " + base64.b64encode(str.encode(user + ":" + pwd)).decode("utf-8")
base_URL = "https://" + CMS_IP + "/api/v1/"

class CMS:

    def verifyUser(username):
        params = { 'emailFilter': username}
        response = a.get_users(params)
        total_results = int(response['users']['@total'])
        if total_results > 0:
            user = response['users']['user'][0]
            userDetails = a.get_user(user['@id'])
            fullName = userDetails['user']['name']
            success = True
        else:
            fullName = ""
            success = False
        return success, fullName

    def getUsers():
        offset = 0 
        params = { 'offset' : offset }
        response = a.get_users(params)
        total_results = int(response['users']['@total'])
        users_list = []
        while total_results > offset:
            users_list, index = append_users(response, users_list)
            offset = offset + index
            params = { 'offset' : offset }
            response = a.get_users(params)
        return users_list

    def append_users(response, users_list):
        index = 0
        try:
            users = response['users']['user']
            for user in users:
                userDetails = a.get_user(user['@id'])
                users_list.append((user['userJid'], userDetails['user']['name']))
                index = index + 1
        except Exception as e:
            print ("Exception: " + str(e))
        return  users_list, index

    def createSpace(name, tenantId):
        payload = {
            'name' : name,
            'uri' : name + '.space',
            'requireCallId' : True,
            'passcode' : '123',
            'tenant' : tenantId
            }
        response = a.create_coSpace(payload)
        coSpace_id = response['@id']
        return coSpace_id

    def createAccessMethod(coSpace_id, callId, name):
        payload = {
            'passcode' : '12345',
            'uri' : name + '.space',
            'callId' : callId,
            'callLegProfile' : host_CLP
        }
        response = a.create_coSpace_access_method(coSpace_id, payload)
        pp.pprint (response)

    def getSpaces(filter_name):
        params = {'filter':filter_name}
        url = base_URL + "coSpaces"
        headers = {
            'Authorization': auth,
            'cache-control': "no-cache"
            }
        response = requests.get(url=url, headers=headers, params=params, verify=False)
        spaces = xmltodict.parse(response.text)
        space_list = spaces['coSpaces']['coSpace']
        for space in space_list:
            print (space['@id'])

    def createTenant(tenant_name):
        payload = {
            'name': tenant_name
        }
        response = a.create_tenant(payload)
        pp.pprint (response)

    def getTenant(tenant_id):
        response = a.get_tenant(tenant_id)
        tenant_name = response['tenant']['name']
        return tenant_name

    def getTenants():
        print ("getting tenants")
        url = base_URL + "tenants"
        headers = {
            'Authorization': auth,
            'cache-control': "no-cache"
            }
        response = requests.get(url=url, headers=headers, verify=False)
        tenants = xmltodict.parse(response.text)
        tenants_list = tenants['tenants']['tenant']
        tenant_list = []
        for tenant in tenants_list:
            tenant_list.append((tenant['@id'], tenant['name']))
        return tenant_list

    def getUserCoSpaces(user_id):
        response = a.get_user_coSpaces(user_id)
        pp.pprint (response)

    def getCoSpaceDetails(coSpace_id):
        response = a.get_coSpace(coSpace_id)
        secret = response['coSpace']['secret']
        callId = response['coSpace']['callId']
        passcode = response['coSpace']['passcode']
        link = "https://se-cis-cms1.nsd5.ciscolabs.com/invited.sf?secret=" + secret + "&id=" + callId
        try:
            ownerJid = response['coSpace']['ownerJid']
        except:
            ownerJid = ""
        return link, callId, ownerJid

    def getCalls(tenant_id):
        parameters = {
            'tenantFilter': tenant_id
        }
        response = a.get_calls(parameters)
        call_id_list = []
        try:
            call_list = response['calls']['call']
            for call in call_list:
                call_id_list.append(call['@id'])
        except Exception as e:
            print ("Exception: " + str(e))
        return call_id_list

    def getParticipants(call_id):
        url = base_URL + "calls/" + call_id + "/participants"
        headers = {
            'Authorization': auth,
            'cache-control': "no-cache"
            }
        response = requests.get(url=url, headers=headers, verify=False)
        participants = xmltodict.parse(response.text)
        total_participants = int(participants['participants']['@total'])
        activator_name = ""
        if total_participants == 1:
            participant_name = participants['participants']['participant']['name']
            participant_id = participants['participants']['participant']['@id']
        elif total_participants > 1:
            participants_list = participants['participants']['participant']
            for participant in participants_list:
                participant_id = participant['@id']
                response = a.get_participant(participant_id)
                isActivator = response['participant']['isActivator']
                if isActivator == "false":
                    participant_name = participant['name']
                    participant_id = participant['@id']
                elif isActivator == "true":
                    activator_name = participant['name']
        else:
            participant_name = ""
            participant_id = ""
        return participant_name, participant_id, activator_name

    def getCallDetails(call_id):
        response = a.get_call(call_id)
        coSpace_id = response['call']['coSpace']
        duration = response['call']['durationSeconds']
        duration = divmod(int(duration), 60)
        duration_mins = duration[0]
        return str(duration_mins), coSpace_id

    def addUserToCospace(coSpace_id, userJid):
        payload = {
            'ownerJid' : userJid
        }
        response = a.modify_coSpace(coSpace_id, payload)
        pp.pprint (response)
        payload = {
            'userJid' : userJid,
            'callLegProfile' : host_CLP
        }
        response = a.add_member_to_coSpace(coSpace_id, payload)
        pp.pprint (response)

    def deleteCall(call_id):
        response = a.delete_call(call_id)
        pp.pprint (response)

    def deleteSpace(coSpace_id):
        response = a.delete_coSpace(coSpace_id)
        pp.pprint (response)

    def getAccessMethod(coSpace_id):
        response = a.get_coSpace_access_methods(coSpace_id, parameters={})
        access_methods = response['accessMethods']['accessMethod']
        for access_method in access_methods:
            access_method_id = access_method['@id']
        return access_method_id
            

    def getAccessMethodDetails(coSpace_id, access_method_id):
        url = base_URL + "coSpaces/" + coSpace_id + "/accessMethods/" + access_method_id
        headers = {
            'Authorization': auth,
            'cache-control': "no-cache"
            }
        response = requests.get(url=url, headers=headers, verify=False)
        details = xmltodict.parse(response.text)
        uri = details['accessMethod']['uri']
        secret = details['accessMethod']['secret']
        callId = details['accessMethod']['callId']
        passcode = details['accessMethod']['passcode']
        link = "https://se-cis-cms1.nsd5.ciscolabs.com/invited.sf?secret=" + secret + "&id=" + callId
        return uri, passcode, link

    def addParticipantToCall(call_id, remoteParty):
        url = base_URL + "calls/" + call_id + "/participants"
        headers = {
            'Authorization': auth,
            'Content-Type': 'application/x-www-form-urlencoded',
            'cache-control': "no-cache"
            }
        payload = ("remoteParty={0}&callLegProfile={1}").format(remoteParty, host_CLP)
        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            pp.pprint (response)
        except Exception as e:
            print (e)

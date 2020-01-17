# Virtual Waiting Room

This app uses the Cisco Meeting Server (CMS) api to allow a doctor to enter a Virtual Waiting Room and see what patients are waiting, and how long they've been waiting. The doctor can move a patient into their consultation queue, then decide how to connect to the patient, either by browser, a video client, or by having CMS call them at a remote destination (number or SIP URI).

To create environment variables for config.py add these to .env file in the root folder.

You'll also need to provide a connection URI to a Mongo DB.

clone canopy - https://github.com/ciscocms/canopy

install requirements by running the following: pip install -r requirements.txt

The first time you login to the app make sure you login with user/password = admin/admin. There are some initial setup tasks that need to be performed, such as creating Call Leg Profiles and Tenants on the CMS server.

The users (doctors) will need to login with LDAP credentials. Make sure you provide the same LDAP server details that are used on your CMS server.


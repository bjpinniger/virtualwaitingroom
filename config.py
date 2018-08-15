import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CUCM = "0.0.0.0" # enter ip address or fqdn of cucm
    VERSION = "12.0" # change this to match the AXL version you want to use, see here: https://developer.cisco.com/docs/axl/#!versioning
    CUCM_USER = os.environ.get("CUCM_USER")
    CUCM_PWD = os.environ.get("CUCM_PWD")
    FILTER = "%SX%" # this is the filter to use for the endpoints, based on the description of the endpoint in CUCM
    USERNAME = os.environ.get("TP_USERNAME") # username for the codec
    PASSWORD = os.environ.get("TP_PASSWORD") # password for the codec
    WTF_CSRF_ENABLED = True
    # Disable debugging
    DEBUG = True
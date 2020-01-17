import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ENCRYPT_PASS = os.environ.get('ENCRYPT_PASS')
    CMS_IP = os.environ.get("CMS_IP")
    CMS_USER = os.environ.get("CMS_USER")
    CMS_PWD = os.environ.get("CMS_PWD")
    MONGO_URI = os.environ.get("MONGO_URI")
    LDAP_HOST = os.environ.get("LDAP_HOST")
    LOGO = True

    WTF_CSRF_ENABLED = True
    # Disable/Enable debugging
    DEBUG = True
    
from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_bootstrap import Bootstrap
from app.extensions import mongo
#from flask_ldap import LDAP

app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)
#ldap = LDAP(app, mongo)
bootstrap = Bootstrap(app)
app.jinja_env.filters['zip'] = zip
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import routes
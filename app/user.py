import ldap
from config import Config

LDAP_HOST = Config.LDAP_HOST


def get_ldap_connection():
    conn = ldap.initialize('ldap://%s:389' % LDAP_HOST)
    return conn


class User:

    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(username, password):
        conn = get_ldap_connection()
        try:
            conn.simple_bind_s(username, password)
            conn.unbind_s()
            result = True
        except ldap.LDAPError as e:
            print ("authentication error")
            print (e)
            result = False
        return result
from flask_pymongo import PyMongo
from flask import jsonify
from datetime import date, datetime, timedelta
import json
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode
from .user import User
from config import Config

ENCRYPT_PASS = Config.ENCRYPT_PASS

mongo = PyMongo()

def encrypt_pwd(pwd):
    cipher = encrypt(ENCRYPT_PASS, pwd)
    encoded_pwd = b64encode(cipher)
    return encoded_pwd

def decrypt_pwd(encoded_pwd):
    cipher = b64decode(encoded_pwd)
    decoded_pwd = decrypt(ENCRYPT_PASS, cipher)
    return decoded_pwd

class Extensions:

    def validate_user(username, password, fullName):
        print ("validate user")
        user_obj = object()
        result = "failure"
        user_collection = mongo.db.users
        user = user_collection.find_one({'_id': username})
        if user['_id'] == "admin":
            try:
                if user['Password'] == "admin" and password == "admin":
                    result = "changePWD"
                else:
                    decoded_pwd = decrypt_pwd(user['Password'])
                    result = "success" if decoded_pwd.decode("utf-8") == password else "failure"
                    print (decoded_pwd.decode("utf-8") )
                    print ("pwd = " + password)
            except Exception as e:
                print (e)
        elif User.validate_login(username, password):  
            if not user:
                user_collection.insert({'_id': username, 'Name': fullName})
                user = user_collection.find_one({'_id': username})
            result = "success"
        if result == "success" or result == "changePWD":
            user_obj = User(user['_id'])
        return user_obj, result

    def get_user(username):
        user_collection = mongo.db.users
        u = user_collection.find_one({'_id': username})
        print ("get user")
        print (u)
        if not u:
            return None
        else:
            return User(u['_id'])

    def update_settings(username, Callback):
        user_collection = mongo.db.users
        user = user_collection.find_one({'_id': username})
        try:
            user_collection.update({'_id': username}, {"$set":{"Callback": Callback}})
            result = "settings updated"
        except Exception as e:
            print (e)
            result = "settings failed to update"
        return result

    def get_settings(username):
        user_collection = mongo.db.users
        user = user_collection.find_one({'_id': username})
        try:
            Callback = user['Callback']
        except Exception as e:
            print (e)
            Callback = ""
        return Callback

    def change_pwd(username, old_pwd, new_pwd):
        success = False
        user_collection = mongo.db.users
        user = user_collection.find_one({'_id': username})
        if user['_id'] == "admin" and user['Password'] == "admin" and old_pwd == "admin":
            encoded_pwd = encrypt_pwd(new_pwd)
            success = True
        elif user['_id'] == "admin" and user['Password'] == "admin":
            print ("current password incorrect")
        else:
            decoded_pwd = decrypt_pwd(old_pwd)
            if decoded_pwd == old_pwd:
                encoded_pwd = encrypt_pwd(new_pwd)
                success = True
        if success:
            user_collection.update({'_id': username}, {"$set":{"Password": encoded_pwd}})
        return success

    def get_admin_settings():
        admin_collection = mongo.db.admin 
        settings = admin_collection.find_one({'_id': "settings"})
        print (settings)
        if not settings:
            return None
        else:
            return settings

    def update_admin_settings(guest_CLP, host_CLP):
        admin_collection = mongo.db.admin 
        settings = admin_collection.find_one({'_id': "settings"})
        print (settings)
        if not settings:
            admin_collection.insert({'_id': "settings", 'guest_CLP': guest_CLP, 'host_CLP': host_CLP})
            result = "settings inserted to DB"
        elif guest_CLP != "":
            admin_collection.update({'_id': "settings"}, {"$set":{"guest_CLP": guest_CLP}})
            result = "settings updated"
        elif host_CLP != "":
            admin_collection.update({'_id': "settings"}, {"$set":{"host_CLP": host_CLP}})
            result = "settings updated"
        return result
from flask_pymongo import PyMongo
from flask import jsonify
from datetime import date, datetime, timedelta
import json
from base64 import b64encode, b64decode
from .user import User

mongo = PyMongo()

def validate_user(username, password, fullName):
    print ("validate user")
    user_collection = mongo.db.users
    if User.validate_login(username, password):
        user = user_collection.find_one({'_id': username})
        if not user:
            user_collection.insert({'_id': username, 'Name': fullName})
            user = user_collection.find_one({'_id': username})
        print (user)
        user_obj = User(user['_id'])
        result = "success"
    else:
        user_obj = object()
        result = "failure"
    return user_obj, result

def get_user(username):
    user_collection = mongo.db.users
    u = user_collection.find_one({'_id': username})
    print ("get user")
    print (u)
    if not u:
        return None
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
#!/usr/bin/env python
# coding=utf-8

import json
from pymongo import MongoClient
from datetime import datetime

data = json.load(open('settings.json'))

password=data["mongoPassword"]
mongoUri=data["mongoUri"]

def connect():
    client = MongoClient("mongodb://admin:"+password+"@"+mongoUri)
    return client.local

# Debe insertar la password en mongo segun cliente y app
# Comprobar si existe o no ya la aplicacion, si esta solo modificar el valor
# Supondremos que el psw es la version encriptada

def insertPsw(db,user,app,psw):

    if db.passwords.find_one({"user":user,"application":app}) is not None:
        db.passwords.update_one({"user":user,"application":app},{'$set' : {"password":psw}})
    else:
        db.passwords.insert_one({"user":user,
                                "application":app,
                                "password":psw,
                                "last-modification":datetime.now()
                                })
    return True

# Debe encontrar el password guardado en mongo segun cliente y app, el decrypt fuera
def findPsw(db,user,app):

    query=db.passwords.find_one({"user":user,"application":app})
    
    return query['password']

def collectionApps(db,user):

    ret=[]

    query = db.passwords.find({"user":user})

    for doc in query:
        ret.append(doc["application"])

    return ret
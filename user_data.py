from pymongo import MongoClient 
import os
import json
import requests

env = os.environ['env']

f = None

if env=="dev":
    f = open('config/config.dev.json',) 
else:
    f = open('config/config.prod.json',) 

data = json.load(f)

token = data['token']

client = MongoClient('localhost', 27017)

bot_database = client['bot_database'] 

user_data = bot_database['user_data'] 


def save_signature(signature,chat_id):
    user_data.update(
    {'chat_id':chat_id},
    {'$set' :{'chat_id':chat_id, 'signature':signature}},upsert=True,)

    cursor = user_data.find({})
    for document in cursor:
        print(document)

def get_signature_list(chat_id):
    document = user_data.find_one({'chat_id':chat_id})
    return document['signature']


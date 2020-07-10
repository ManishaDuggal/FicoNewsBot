from pymongo import MongoClient 
from financial_data import financial_quote
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

email_collection = bot_database['email_collection'] 

#function used to save template in database
def save_email_template(chat_id,email_name,subject,receivers):
    record = dict()
    record['chat_id']=chat_id
    record['email_name']=email_name
    record['subject']=subject
    record['receivers']=receivers
    email_collection.insert(record)
    return

def get_email_templates(chat_id):
    documents = email_collection.find({'chat_id':chat_id})
    return documents

def get_email_names(chat_id):
    documents = email_collection.find({'chat_id':chat_id})

#creating template name list from documents
    namelist = list()
    for document in documents:
        namelist.append(document['email_name'])
    return namelist

def delete_email_name(chat_id,name):
    email_collection.remove({'chat_id':chat_id,'email_name':name})
    return
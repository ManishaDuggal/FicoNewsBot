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

stock_alert = bot_database['stock_alert'] 



def save_stock_alert_price(stock_price,chat_id):
    stock_alert.update(
    {'chat_id':chat_id},
    {'$set' :{'chat_id':chat_id, 'stock_price':stock_price}},upsert=True,)
    #stock_alert.delete_many({})
    cursor = stock_alert.find({})
    for document in cursor:
        print(document)


def send_stock_alert():
    response = financial_quote()
    price = response['Global Quote']['05. price']
    cursor = stock_alert.find({})
    for document in cursor:
        if float(price) >= float(document['stock_price']):
            message="""Current price is {stock_price}. 
            Use /deletestockalert command to remove alert.""".format(stock_price=price)
            requests.get('https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'.format(chat_id=document['chat_id'],message=message,token=token))


def delete_stock_data(chat_id):
    stock_alert.remove({'chat_id':chat_id})
    return
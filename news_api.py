import requests
import json
from datetime import datetime, timedelta
import os

env = os.environ['env']

f = None

if env=="dev":
    f = open('config/config.dev.json',) 
else:
    f = open('config/config.prod.json',) 

data = json.load(f)
news_api_key = data['news_api_key']


headers = {'Authorization': news_api_key}


everything_news_url = 'https://newsapi.org/v2/everything'


final_date= datetime.now() - timedelta(days=5)


search2= '(Fair AND Isaac AND Corporation) OR FICO'

everything_payload = {'qInTitle':search2,'language': 'en','sortBy':'popularity','from':final_date,'excludeDomains':'rlsbb.ru'}

response = requests.get(url=everything_news_url, headers=headers, params=everything_payload)

def everything_news():
    response = requests.get(url=everything_news_url, headers=headers, params=everything_payload)
    return response.json()['articles']


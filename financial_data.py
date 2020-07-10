import requests
import  json
import os


env = os.environ['env']

f = None

if env=="dev":
    f = open('config/config.dev.json',) 
else:
    f = open('config/config.prod.json',) 

data = json.load(f)

#retriving api key from config file
financial_api_key = data['financial_api_key']


#hits alpha vantage api and returns response

def financial_quote():
    response = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=FICO&apikey={financial_api_key}".format(financial_api_key=financial_api_key))
    return response.json()



from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot
from telegram.parsemode import ParseMode
import os
import json
import time
from stock_handlers import add_stock_handlers
from news_handlers import add_news_handlers
from common_handlers import add_common_handlers
from stock_data import send_stock_alert
from email_handlers import add_email_handlers


env = os.environ['env']

f = None

if env=="dev":
    f = open('config/config.dev.json',) 
else:
    f = open('config/config.prod.json',) 

data = json.load(f)

token = data['token']


updater = Updater(token,use_context=True)

dispatcher: Dispatcher = updater.dispatcher

#registering command handlers 
add_stock_handlers(dispatcher)
add_news_handlers(dispatcher)
add_common_handlers(dispatcher)
add_email_handlers(dispatcher)
updater.start_polling()

while True:
    send_stock_alert()
    time.sleep(20)   




from telegram.ext.commandhandler import CommandHandler
from telegram.ext import Filters
from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler 
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot
from telegram.parsemode import ParseMode
from news_api import everything_news


def news(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    articles = everything_news()
#convert news details into message to send 
    for article in articles:
        title = article['title']
        url = article['url']
        message = "{title} <a href='{url}'>Click Here</a>".format(title=title,url=url)
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=ParseMode.HTML,
        )
    return



def add_news_handlers(dispatcher:Dispatcher):
    dispatcher.add_handler(CommandHandler("news", news))
    return






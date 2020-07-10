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
from financial_data import financial_quote
from stock_data import save_stock_alert_price,delete_stock_data

def stock(update: Update, context: CallbackContext):
    """
    the callback for handling stock command
    """

    response = financial_quote()

    bot: Bot = context.bot

    message = """
    Symbol : {symbol} 
    Open : {open} 
    High : {high} 
    Low : {low} 
    Price : {price} 
    Volume : {volume} 
    Latest Trading Day = {latest_trading_day} 
    Previous close : {previous_close} 
    Change : {change} 
    Change Percent : {change_percent}
    """.format(
    symbol=response['Global Quote']['01. symbol'], open=response['Global Quote']['02. open'], low=response['Global Quote']['04. low'],high=response['Global Quote']['03. high'],
    price=response['Global Quote']['05. price'], volume=response['Global Quote']['06. volume'], latest_trading_day=response['Global Quote']['07. latest trading day'],
    previous_close=response['Global Quote']['08. previous close'], change=response['Global Quote']['09. change'],change_percent=response['Global Quote']['10. change percent']
    )

    bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        #parse_mode=ParseMode.Markdown,
    )
    return


STOCKPRICE = 0



def stock_alert(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! You have used /stockalert command. Tell me stock price you want to set.")
    return STOCKPRICE


def save_price(update: Update, context: CallbackContext):
    text = update.message.text
    save_stock_alert_price(int(text),update.effective_chat.id)
    update.message.reply_text('Stock Alert is set')
    return ConversationHandler.END




def done(update: Update, context: CallbackContext):
    update.message.reply_text("Process Ended")
    return ConversationHandler.END


stock_alert_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('stockalert', stock_alert)],

        states={

            STOCKPRICE: [MessageHandler(Filters.text,save_price)],

        },

        fallbacks=[MessageHandler(Filters.all, done)]
    )


def delete_stock_alert(update: Update, context: CallbackContext):
    """
    the callback for handling deletestockalert command
    """
    delete_stock_data(update.effective_chat.id)
    bot: Bot = context.bot


    bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        """<b>Stock Alert</b> deleted.
        """,
        parse_mode=ParseMode.HTML,
    )





def add_stock_handlers(dispatcher:Dispatcher):
    dispatcher.add_handler(CommandHandler("stock", stock))
    dispatcher.add_handler(CommandHandler("deletestockalert", delete_stock_alert))
    dispatcher.add_handler(stock_alert_conv_handler)
    return
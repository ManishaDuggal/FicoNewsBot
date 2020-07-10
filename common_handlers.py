from telegram.ext.commandhandler import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot
from telegram.parsemode import ParseMode

#callback function for handling help command

def help(update: Update, context: CallbackContext):
    """
    the callback for handling start command
    """
    bot: Bot = context.bot


    bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        """Hi there, How can I help you?. 
        Use <b>/news</b> command to get news. 
        Use <b>/stock</b> command to get stocks quote.
        Use <b>/stockalert</b> command to set stock alert.
        Use <b>/deletestockalert</b> command to delete stock alert.
        Use <b>/setmailtemplate</b> command to create a new template.
        Use <b>/deletetemplate</b> command to delete a template.
        Use <b>/mymailtemplates</b> command to get list of all templates you have created.
        Use <b>/sendmail</b> command to send a mail.
        Use <b>/setsignature</b> command to set signature.
        """,
        parse_mode=ParseMode.HTML,
    )

#callback function for handling start command

def start(update: Update, context: CallbackContext):
    """
    the callback for handling start command
    """
    bot: Bot = context.bot


    bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        """Hi there, how can I help you? Use <b>/help</b> command to explore all command options.
        """,
        parse_mode=ParseMode.HTML,
    )


def add_common_handlers(dispatcher:Dispatcher):
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("start", start))
    return



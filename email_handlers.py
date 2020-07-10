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
from email_data import save_email_template,get_email_names,get_email_templates,delete_email_name
from email_api import send_mail
from user_data import save_signature,get_signature_list

NAME, SUBJECT, RECEIVER, CONTINUE, SEND, CONTENT, SIGNATURE, DELETETEMPLATE= range(8)

#callback function for handling setmailtemplate command

def start_email(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Tell me name of email template """)
    return NAME

#function will save template name entered by user and asks for email subject
def email_name(update: Update, context: CallbackContext):
    context.user_data['email_name'] = update.message.text
    update.message.reply_text(
        """Tell me subject line you want to use for mail. """)

    return SUBJECT

#function will save subject in context and then asks for first receiver
def subject_name(update: Update, context: CallbackContext):
    context.user_data['subject_name'] = update.message.text
    update.message.reply_text(
        """Now specify receivers one by one. """
    )
    return RECEIVER

#function saves first receiver and asks for other receivers if any
def first_receiver(update: Update, context: CallbackContext):
    context.user_data['receivers'] = list()
    context.user_data['receivers'].append(update.message.text)
    update.message.reply_text(
        """Tell me any another receiver or /quit."""
    )
    return CONTINUE

#this function continues asking for receivers
def continue_asking(update: Update, context: CallbackContext):
    context.user_data['receivers'].append(update.message.text)
    update.message.reply_text(
        """Tell me any another receiver or /quit. """
    )
    return CONTINUE

#function to save template in database and notifies user about details
def done(update: Update, context: CallbackContext):

    save_email_template(chat_id=update.effective_chat.id,email_name=context.user_data['email_name'],
    subject=context.user_data['subject_name'],receivers=context.user_data['receivers'])

    update.message.reply_text(
        """
        Template name is  {email_name}.
        Subject : {subject_name}
        Receiver/Receivers : {receivers}

        """.format(email_name=context.user_data['email_name'],subject_name=context.user_data['subject_name'],receivers=context.user_data['receivers'])
        )

    return ConversationHandler.END


def end(update: Update, context: CallbackContext):
    update.message.reply_text(
        """ Process Ended
        """
        )
    return ConversationHandler.END

#callback function for handling sendmail command
#it will show list of templates created by user 
def ask_email_name(update: Update, context: CallbackContext):

    templates = get_email_templates(update.effective_chat.id)
    context.user_data['templates']=templates

    l=list()
    for i,t in zip(range(1,templates.count()+1),templates):
        l.append("{i}. {t}".format(i=i,t=t['email_name']))

    l="\n".join(l)
    update.message.reply_text("Please choose one of the following templates\n"+l)
    return CONTENT

#this function will ask user for email content
def ask_email_content(update: Update, context: CallbackContext):
    print(update.message.text)
    no=int(update.message.text)-1
    templates = get_email_templates(update.effective_chat.id)
    document={}
    for i,t in zip(range(templates.count()),templates):
        if i==no:
            document=t

    context.user_data['document'] = document
    update.message.reply_text("Please specify mail content")
    return SEND

#function used to send mail
def send_email_call(update: Update, context: CallbackContext):
    print("Document")
    document = context.user_data['document']
    signature_list=get_signature_list(update.effective_chat.id)
    send_mail(document['receivers'],document['subject'],update.message.text,signature_list)
    update.message.reply_text("Mail Sent")
    return ConversationHandler.END

#callback function for handling setsignature command
def ask_signature(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Please enter signature line by line """
    )
    context.user_data['signature']=list()
    return SIGNATURE


def con_signature(update: Update, context: CallbackContext):
    context.user_data['signature'].append(update.message.text)
    update.message.reply_text(
        """Add another line or /quit """
    )
    return SIGNATURE

#saves signature list in database
def save(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Saved"""
    )
    save_signature(context.user_data['signature'],update.effective_chat.id)
    print(context.user_data['signature'])
    return ConversationHandler.END

#callback function for handling deletetemplate command

def ask_delete_template(update: Update, context: CallbackContext):
    update.message.reply_text("""Which template you want to delete ? """)
    show_email_templates(update,context)
    return DELETETEMPLATE

#function for deleting template
def delete_template(update: Update, context: CallbackContext):
    
    no=int(update.message.text)-1

#retrive all documents with user's chat id
    templates = get_email_templates(update.effective_chat.id)
    document={}
    for i,t in zip(range(templates.count()),templates):
        if i==no:
            document=t

#retrive template name from document and pass to delete
    delete_email_name(update.effective_chat.id,document['email_name'])
    update.message.reply_text("""Template with name {name} deleted""".format(name=document['email_name']))
    return ConversationHandler.END


#handling all email conversations through this conversation handler
email_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('setmailtemplate', start_email),CommandHandler('sendmail', ask_email_name),
        CommandHandler('setsignature', ask_signature),CommandHandler("deletetemplate", ask_delete_template)],

        states={

            NAME: [MessageHandler(Filters.text,email_name)],
            SUBJECT : [MessageHandler(Filters.text,subject_name)],
            RECEIVER : [CommandHandler('quit',done),MessageHandler(Filters.text,first_receiver)],
            CONTINUE : [CommandHandler('quit',done), MessageHandler(Filters.text,continue_asking)],
            CONTENT : [MessageHandler(Filters.text,ask_email_content)],
            SEND : [MessageHandler(Filters.text,send_email_call)],
            SIGNATURE : [CommandHandler('quit',save), MessageHandler(Filters.text,con_signature)],
            DELETETEMPLATE : [MessageHandler(Filters.text,delete_template)],
        },

        fallbacks=[MessageHandler(Filters.all, end)]
    )

#function used to print all template names with numbering
def show_email_templates(update: Update, context: CallbackContext):

    namelist = get_email_names(update.effective_chat.id)
    l=list()
    for i,t in zip(range(1,len(namelist)+1),namelist):
        l.append("{i}. {t}".format(i=i,t=t))
        print(l)
    
    str = "\n".join(l)
    bot: Bot = context.bot
    message = "These are all saved templates.\n" + str
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
    )
    return




def add_email_handlers(dispatcher:Dispatcher):
    dispatcher.add_handler(email_conv_handler)
    dispatcher.add_handler(CommandHandler("mymailtemplates", show_email_templates))
    return
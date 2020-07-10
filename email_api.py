import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json
env = os.environ['env']

f = None

if env=="dev":
    f = open('config/config.dev.json',) 
else:
    f = open('config/config.prod.json',) 

data = json.load(f)

gmail_address = data['gmail_address']
gmail_password = data['gmail_password']

mail = """Hi,
            {content}
            
{signature}
"""

def send_mail(receivers,subject,content,signature):
    
    signature="\n".join(signature)
    mail_content = mail.format(content=content,signature=signature)
    #The mail addresses and password
    sender_address = gmail_address
    sender_pass = gmail_password
    receiver_address = receivers
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'manishaduggal@fico.com'
    message['To'] = ", ".join(receivers)
    message['Subject'] = subject  
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


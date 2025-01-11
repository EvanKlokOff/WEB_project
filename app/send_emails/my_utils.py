import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.send_emails.config import conf
from app.send_emails.schemas import EmailSchema

def create_message(email: EmailSchema):
    msg = MIMEMultipart()
    msg["From"] = conf.MAIL_FROM
    msg["To"] = email.email
    msg.attach(MIMEText(email.body, email.body_type))

def send_message(email: EmailSchema):
    try:
        smtpobj = smtplib.SMTP("smtp.mail.ru", 465)
        smtpobj.starttls()
        smtpobj.login(conf.MAIL_USERNAME,conf.MAIL_PASSWORD)
        smtpobj.sendmail(conf.MAIL_FROM, email.email, email.body)
    except:
        pass
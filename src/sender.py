import os
import smtplib, ssl
from utils import log_detail

SERVER_MAIL = os.environ['SERVER_MAIL']
SERVER_MAIL_PWD = os.environ['SERVER_MAIL_PWD']

def send_token_mail(receiver, token):
    port = 465
    smtp_server_domain_name = "smtp.gmail.com"
    try:
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(smtp_server_domain_name, port, context=ssl_context)
        service.login(SERVER_MAIL, SERVER_MAIL_PWD)
        sender = 'noreply@gmail.com'
        subject = 'New token'
        content = f'Token: {token} has been generated.'
        service.sendmail(sender, [receiver], f'From: {sender}\nSubject: {subject}\n\n{content}')
        service.quit()
    except Exception as e:
        log_detail(f'Token: {token} not sent')

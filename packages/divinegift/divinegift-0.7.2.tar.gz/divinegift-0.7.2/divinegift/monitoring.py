import os
import smtplib
import sys
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
#import vk_api
import requests


config = {
    'server': 'mail.s7.ru',
    'from': 'noreply@s7.ru'
}


def send_email(subject, body_text, to_emails, cc_emails):
    """
    Send an email letter
    :param subject: Subject
    :param body_text: Text
    :param to_emails: List of email recievers
    :param cc_emails: List of emails who will recieve copy
    :return:
    """
    host = config['server']
    from_addr = config['from']

    BODY = "\r\n".join((
        "From: %s" % from_addr,
        "To: %s" % ', '.join(to_emails),
        "CC: %s" % ', '.join(cc_emails),
        "Subject: %s" % subject,
        "",
        body_text
    ))

    emails = to_emails + cc_emails

    server = smtplib.SMTP(host)
    server.sendmail(from_addr, emails, BODY)
    server.quit()


def send_email_with_attachment(subject, body_text, to_emails, cc_emails, file_to_attach, file_path):
    """
    Send an email with an attachment
    """
    header = 'Content-Disposition', 'attachment; filename="%s"' % file_to_attach

    host = config['server']
    from_addr = config['from']

    # create the message
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    if body_text:
        msg.attach(MIMEText(body_text))

    msg["To"] = ', '.join(to_emails)
    msg["cc"] = ', '.join(cc_emails)

    attachment = MIMEBase('application', "octet-stream")

    try:
        with open(file_path + file_to_attach, "rb") as fh:
            data = fh.read()

        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        msg = "Error opening attachment file %s" % file_to_attach
        sys.exit(1)

    emails = to_emails + cc_emails
    server = smtplib.SMTP(host)
    server.sendmail(from_addr, emails, msg.as_string())
    server.quit()


def send_telegram(message, chat_id=161680036, subject=None):
    """
    Send a telegram message
    :param message: Message
    :param chat_id: Id of chat where msg will be sent
    :param subject: Subject of message
    :return:
    """
    URL = 'https://api.telegram.org/bot'                        # URL на который отправляется запрос
    TOKEN = '456941934:AAGZMmXJE4VyLagIkVY7qMG0doASxU7f8ac'     # токен вашего бота, полученный от @BotFather
    data = {'chat_id': chat_id,
            'text': (('Тема сообщения: ' + subject + '\n') if subject else '') + 'Сообщение: ' + message}

    try:
        requests.post(URL + TOKEN + '/sendMessage', data=data)  # запрос на отправку сообщения
    except:
        print('Send message error')


def send_slack():
    """
    Will be done later
    :return:
    """
    pass


"""
def auth_vk(login, password):
    # Авторизоваться как человек
    vk = vk_api.VkApi(login=login, password=password)
    vk.auth()
    # Авторизоваться как сообщество
    #vk = vk_api.VkApi(token='a94dd2ef02952a0606fd37f2d1fb11b2d456c034c7671c2b3fab8c3f660474062b9e253c78597d9248469')

    return vk


def send_vk(vk, message, chat_id='8636128', mode='private'):
    #vk = auth_vk()
    if mode == 'private':
        vk.method('messages.send', {'user_id': chat_id, 'message': message})
    elif mode == 'chat':
        vk.method('messages.send', {'peer_id': chat_id, 'message': message})
    elif mode == 'group':
        vk.method('messages.send', {'user_ids': chat_id, 'message': message})
"""

if __name__ == '__main__':
    pass

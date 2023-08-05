import os
import logging
from divinegift.monitoring import send_telegram, send_slack, send_email, send_email_with_attachment
import traceback

telegram_chat = {'private': 161680036, 'chat': -277453709, 'channel': -1001343660695}
vk_chat = {'private': '8636128', 'chat': '2000000193'}
to_email_chat = {'private': ['r.rasputin@s7.ru'], 'chat': ['aims.control@s7.ru']}
cc_email_chat = {'private': [], 'chat': []}
log = None


def log_debug(msg):
    logging.debug(msg)
    print(msg)


def log_info(msg):
    logging.info(msg)
    print(msg)


def log_warning(msg):
    logging.warning(msg)
    print(msg)


def log_err(msg, src=None, mode=None, channel='private'):
    logging.exception(msg)
    print(msg)
    error_txt = 'Произошла ошибка в {}\nТекст ошибки: {}\n{}'.format(src, msg, traceback.format_exc())

    if mode:
        #if 'vk' in mode:
        #   send_vk(error_txt, vk_chat[channel.get('vk')], channel.get('vk', 'private'))
        if 'telegram' in mode:
            send_telegram(error_txt, chat_id=channel.get('telegram', -1001343660695))
        if 'slack' in mode:
            send_slack()
        if 'email' in mode:
            send_email(src + ' ERROR', error_txt,
                       channel.get('email_to', ['r.rasputin@s7.ru']),
                       channel.get('email_cc', []))
        if 'email_attach' in mode:
            send_email_with_attachment(src + ' ERROR', error_txt,
                                       channel.get('email_to', ['r.rasputin@s7.ru']),
                                       channel.get('email_cc', []),
                                       log, os.getcwd() + os.sep)


def log_crit(msg):
    logging.critical(msg)
    print(msg)


def set_loglevel(log_level, log_file):
    global log
    log = log_file
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    print('Add logging with level {} to file {}'.format(log_level, log_file))
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=numeric_level,
                        filename=log_file)

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from divinegift.monitoring import send_telegram, send_slack, send_email, send_email_with_attachment
import traceback

telegram_chat = {'private': 161680036, 'chat': -277453709, 'channel': -1001343660695}
vk_chat = {'private': '8636128', 'chat': '2000000193'}
to_email_chat = {'private': ['r.rasputin@s7.ru'], 'chat': ['aims.control@s7.ru']}
cc_email_chat = {'private': [], 'chat': []}
logger = None


def log_debug(msg):
    if logger:
        logger.debug(msg)
    else:
        logging.debug(msg)
    print(msg)


def log_info(msg):
    if logger:
        logger.info(msg)
    else:
        logging.info(msg)
    print(msg)


def log_warning(msg):
    if logger:
        logger.warning(msg)
    else:
        logging.warning(msg)
    print(msg)


def log_err(msg, src=None, mode=None, channel='private'):
    if logger:
        logger.exception(msg)
    else:
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
    global logger
    logger = logging.getLogger('Rotating log')
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logger.setLevel(numeric_level)
    formatter = logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s')
    if log_file:
        if not os.path.exists('logs/'):
            os.mkdir('logs/')
        handler = TimedRotatingFileHandler('logs/' + log_file, when='midnight', interval=1, backupCount=7)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

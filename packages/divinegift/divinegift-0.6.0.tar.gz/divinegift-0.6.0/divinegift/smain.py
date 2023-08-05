from divinegift.logger import log_info, log_err
from sqlalchemy import create_engine, MetaData, Table
from string import Template
import json
import sys
from datetime import datetime
import re
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import os

datetime_regex = r'20\d{2}(-|\/)((0[1-9])|(1[0-2]))(-|\/)((0[1-9])|([1-2][0-9])|(3[0-1]))(T|\s)(([0-1][0-9])|(2[0-3])):([0-5][0-9]):([0-5][0-9])'


class Settings:
    def __init__(self):
        self.settings = {}

    def get_settings(self):
        return self.settings

    def set_settings(self, json_str):
        self.settings = json_str

    def parse_settings(self, file='./settings.conf', encoding='utf-8'):
        json_data = parse_json(file, encoding=encoding)

        dict_c = dict_compare(self.settings, json_data)
        added, removed, modified, same = dict_c.values()
        if len(added) > 0:
            for r in list(added):
                log_info('Added {}: {}'.format(r, json_data.get(r)))
        if len(removed) > 0:
            for r in list(removed):
                log_info('Removed {}: {}'.format(r, self.settings.get(r)))
        if len(modified) > 0:
            for r in list(modified):
                log_info('Modified {}: {} -> {}'.format(r, modified.get(r)[0], modified.get(r)[1]))

        self.set_settings(json_data)


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d2_keys - d1_keys
    removed = d1_keys - d2_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])

    result = {'added': list(added), 'removed': list(removed), 'modified': modified, 'same': list(same)}
    return result


def get_conn(db_conn):
    """
    Create connection for SQLAlchemy
    :param db_conn: DB connection (user, password, host, port, db_name)
    :return: Engine, Connection, Metadata
    """
    if db_conn.get('dialect') == 'mssql+pytds':
        from sqlalchemy.dialects import registry
        registry.register("mssql.pytds", "sqlalchemy_pytds.dialect", "MSDialect_pytds")
    if db_conn.get('db_host') and db_conn.get('db_port'):
        connect_str = '{dialect}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(**db_conn)
    else:
        connect_str = '{dialect}://{db_user}:{db_pass}@{db_name}'.format(**db_conn)
    engine = create_engine(connect_str)
    conn = engine.connect()
    metadata = MetaData()
    return engine, conn, metadata


def get_raw_conn(db_conn):
    if db_conn.get('dialect') == 'mssql+pytds':
        from sqlalchemy.dialects import registry
        registry.register("mssql.pytds", "sqlalchemy_pytds.dialect", "MSDialect_pytds")
    if db_conn.get('db_host') and db_conn.get('db_port'):
        connect_str = '{dialect}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(**db_conn)
    else:
        connect_str = '{dialect}://{db_user}:{db_pass}@{db_name}'.format(**db_conn)    
    engine = create_engine(connect_str)
    conn = engine.raw_connection()
    return conn


def close_conn(conn):
    conn.close()


def get_sql(filename, encoding='cp1251'):
    """
    Get sql string from file
    :param filename: File name
    :return: String with sql
    """
    file = open(filename, 'r', encoding=encoding)
    sql = file.read()
    file.close()
    return sql


def get_data(sql, db_conn, encoding='cp1251', **kwargs):
    """
    Get raw aims data
    :param sql: File with sql which need to execute
    :param db_conn: DB connect creditions
    :param kwargs: List with additional data
    :return: Dictionary
    """
    if os.path.exists(sql):
        script_t = Template(get_sql(sql, encoding))
    else:
        script_t = Template(sql)
    script = script_t.safe_substitute(**kwargs)
    #print(script)

    engine, conn, metadata = get_conn(db_conn)
    res = conn.execute(script)
    ress = [dict(row.items()) for row in res]
    close_conn(conn)

    return ress


def run_script(sql, db_conn, encoding='cp1251', **kwargs):
    """
    Run custom script
    :param sql: File with sql which need to execute
    :param db_conn: DB connect creditions
    :param kwargs: List with additional data
    :return: None
    """    
    if os.path.exists(sql):
        script_t = Template(get_sql(sql, encoding))
    else:
        script_t = Template(sql)
    script = script_t.safe_substitute(**kwargs)

    engine, conn, metadata = get_conn(db_conn)
    conn.execute(script)
    close_conn(conn)


def get_args():
    args = sys.argv[1:]
    args_d = {}
    for i, arg in enumerate(args[::2]):
        if i == len(args):
            break
        args_d[arg] = args[i * 2 + 1]
    args_d['name'] = sys.argv[0]
    return args_d


def get_log_param(args):
    log_level = None
    log_name = None
    for key in args.keys():
        if key in ['--log_level', '-ll']:
            log_level = args.get(key)
        if key in ['--log_name', '-ln']:
            log_name = args.get(key)

    if not log_level:
        log_level = 'INFO'
    if not log_name:
        log_name = None

    return log_level, log_name


def parse_json(json_fname, encoding='utf-8'):
    try:
        json_file = open(json_fname, encoding=encoding)
        json_str = json_file.read()
        json_data = json.loads(json_str, object_hook=date_hook)
    except:
        json_data = None

    return json_data


def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            pass
    return json_dict


def create_json(json_fname, json_data, encoding='utf-8'):
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    with open(json_fname, 'w', encoding=encoding) as outfile:
        response = json.dump(json_data, outfile, ensure_ascii=False, default=dthandler, indent=4)


def send_email_with_attachments(subject, body_text, to_emails, cc_emails, files, file_path,
                                host="mail.s7.ru", from_addr="noreply@s7.ru"):
    """
    Send an email with an attachment
    """
    # create the message
    log_info('Send email with subject {}'.format(subject))
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    #if body_text:
    #    msg.attach(MIMEText(body_text))

    msg["To"] = ', '.join(to_emails)
    msg["cc"] = ', '.join(cc_emails)

    for file_to_attach in files:
        try:
            attachment = MIMEBase('application', "octet-stream")

            with open(file_path + file_to_attach, "rb") as fh:
                data = fh.read()

            attachment.set_payload(data)
            encoders.encode_base64(attachment)
            #attachment.add_header(*header)
            attachment.add_header('Content-Disposition', 'attachment; filename={}'.format(file_to_attach))
            msg.attach(attachment)
        except IOError:
            msg = "Error opening attachment file %s" % file_to_attach
            log_err(msg)
            #sys.exit(1)

    msg.attach(MIMEText(body_text, 'html'))

    emails = to_emails + cc_emails
    server = smtplib.SMTP(host)
    server.sendmail(from_addr, emails, msg.as_string())

    server.quit()
    log_info('Email was sended')


if __name__ == '__main__':
    pass

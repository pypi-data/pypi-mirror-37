"""Send email and log when there is an uncaught exception in your code
Use in your code:

    from os import path
    import crashlog

    logfile = path.expanduser('~/.crashes.log')
    crashlog.install(emails=['daffy@duck.com'], logfile=logfile)


For emails to work set SMTP_SERVER environment variable and possible SMTP_USER
and SMTP_PASSWORD.
"""

__version__ = '0.1.0'

import sys
from smtplib import SMTP
from email.mime.text import MIMEText
from os import environ, makedirs, path
from traceback import format_exception
from time import ctime

if sys.version_info[0] >= 3:
    from io import StringIO
else:
    from cStringIO import StringIO

_emails = []
_logfile = None
_prev_hook = None


def send_email(emails, program, message):
    server = environ.get('SMTP_SERVER')
    if not server:
        return

    message = MIMEText(message)
    message['Subject'] = '{} crashed'.format(program)
    crashlog_email = 'noreply@somewhere.com'
    message['From'] = 'Crashlog <{}>'.format(crashlog_email)

    smtp = SMTP(server)
    user, passwd = environ.get('SMTP_USER', 'SMTP_PASSWORD')
    if user and passwd:
        smtp.login(user, passwd)
    smtp.sendmail(crashlog_email, _emails, message.as_string())


def format_message(type, value, traceback):
    io = StringIO()

    def out(msg):
        io.write(u'{}\n'.format(msg))

    out(ctime())
    out('== Traceback ==')
    out(''.join(format_exception(type, value, traceback)))
    out('\n== Command line ==')
    out(' '.join(sys.argv))
    out('\n== Environment ==')
    for key, value in environ.items():
        out('{} = {}'.format(key, value))

    return io.getvalue()


def excepthook(type, value, traceback):
    try:
        if not (_emails or _logfile):
            return

        message = format_message(type, value, traceback)
        if _emails:
            send_email(_emails, sys.argv[0], message)

        if _logfile:
            with open(_logfile, 'at') as fo:
                fo.write('{}\n'.format(message))

    finally:
        if _prev_hook:
            _prev_hook(type, value, traceback)


def install(emails=None, logfile=None):
    """Install crashlog uncaught exception hook.

    Parameters
    ----------
    emails : list of str
        List of emails to send notification to
    logfile : str
        Log file to write exceptions to
    """
    global _emails, _prev_hook, _logfile

    log_dir = path.dirname(logfile)
    if not path.exists(log_dir):
        makedirs(log_dir)

    if emails and isinstance(emails, str):
        emails = [emails]

    _emails = emails or _emails
    _logfile = logfile
    _prev_hook = sys.excepthook
    sys.excepthook = excepthook

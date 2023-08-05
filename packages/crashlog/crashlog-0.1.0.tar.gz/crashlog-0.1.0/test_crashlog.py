import crashlog
import sys
from tempfile import NamedTemporaryFile


def test_install():
    emails = ['daffy@looney.org', 'bugs@looney.org']
    logfile = NamedTemporaryFile().name

    orig_emails = crashlog._emails
    orig_logfile = crashlog._logfile

    try:
        crashlog.install(emails, logfile)
        assert crashlog._emails == emails, 'bad emails'
        assert crashlog._logfile == logfile, 'bad logfile'
        assert sys.excepthook == crashlog.excepthook
    finally:
        crashlog._emails = orig_emails
        crashlog._logfile = orig_logfile
        sys.excepthook = crashlog._prev_hook

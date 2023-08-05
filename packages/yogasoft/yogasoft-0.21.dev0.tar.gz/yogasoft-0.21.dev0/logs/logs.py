import logging
from copy import copy
from django.views.debug import ExceptionReporter
from twilio.rest import Client
from yogasoft.settings import (
    ALLOWED_HOSTS,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_NUMBER
    )


class SmsHangler(logging.Handler):

    def __init__(self, include_html=False, email_backend=None):
        logging.Handler.__init__(self)
        self.include_html = include_html
        self.email_backend = email_backend


    def emit(self, record):
        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in ALLOWED_HOSTS
                 else 'EXTERNAL'),
                record.getMessage()
            )
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
        subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        message = "%s\n\n%s" % (self.format(no_exc_record), reporter.get_traceback_text())

        self.send_sms(subject, message)


    def send_sms(self, subject, message):
        account_sid = TWILIO_ACCOUNT_SID
        auth_token = TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        message = client.api.account.messages.create(to="+380970080823",
                                                     from_=TWILIO_NUMBER,
                                                     body=str(message)[:200])


    def format_subject(self, subject):
            """
            Escape CR and LF characters.
            """
            return subject.replace('\n', '\\n').replace('\r', '\\r')
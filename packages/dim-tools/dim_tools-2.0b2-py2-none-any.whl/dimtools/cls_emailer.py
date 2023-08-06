# -*- coding:utf-8 -*-
from smtplib import SMTP_SSL


class Sender:
    def __init__(self, recepient=None, subject=None, message=None,
                 login=None, word=None, server='smtp.yandex.ru', port=465):
        self.recepient = recepient
        self.subject = subject
        self.message = message
        self.login = login
        self.word = word
        self.server = server
        self.port = port
        self.msg = None

    def check_server_data(self):
        def none_check(data):
            if data[1] is None:
                print 'Error: no %s is specified' % data[0]
                return True
            return False
        error, warning = False, False
        if none_check(['server', self.server]):
            error = True
        if none_check(['port', self.port]):
            error = True
        if none_check(['login', self.login]):
            error = True
        if none_check(['password', self.word]):
            error = True
        return error, warning

    def send(self, rcpt):
        status = 1
        try:
            sender = self.login
            recepient = rcpt
            subject = self.subject
            self.msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (sender, recepient, subject, self.message))
            # sending data
            s = SMTP_SSL(self.server, self.port)
            s.login(self.login, self.word)
            s.sendmail(sender, recepient, self.msg)
            s.quit()
            status = 0
        finally:
            return status

    def notify(self, recepient=None, subject=None, message=None):
        error, warning = self.check_server_data()
        if recepient and len(recepient) > 0:
            if len(recepient[0]) > 1:
                self.recepient = recepient
            else:
                self.recepient = [recepient, ]
        elif self.recepient and len(self.recepient) > 0:
            if len(self.recepient[0]) == 1:
                self.recepient = [self.recepient, ]
        else:
            print 'Error: something wrong with recepients, got %s' % self.recepient
            error = True
        if not subject and not self.subject:
            print 'Warning: no subject'
            # warning = True
            self.subject = ''
        if not message and not self.message:
            print 'Warning: no message'
            # warning = True
            self.message = ''
        if error:
            return 1
        # warning is suppressed
        # if warning:  # at this moment warning behaves same as error
        #    return 1
        for r in self.recepient:
            res = self.send(r)
            if not res:
                print 'The message was send to %s' % r
            else:
                print 'Error: the message was lost on the way to %s' % r
            # self.sql_write(res)  # should write result in DB, before and after sending
        return 0

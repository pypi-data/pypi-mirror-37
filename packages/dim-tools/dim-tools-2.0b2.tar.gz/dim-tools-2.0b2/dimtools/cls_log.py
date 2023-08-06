# -*- coding:utf-8 -*-
from datetime import datetime


class LogClass:
    def __init__(self, log_name='default.log', to_log=False):
        self.log_name = log_name
        self.to_log = to_log

    def if_log_exists(self):
        try:
            with open(self.log_name, 'r'):
                pass
            return True
        except IOError:
            return False

    def show(self, *args):
        data = [str(datetime.now()), ]
        data += [str(item) for item in args]
        if self.to_log:
            if self.if_log_exists():
                print >> open(self.log_name, 'a'), '\t'.join(data)
            else:
                print >> open(self.log_name, 'w'), '\t'.join(data)
        else:
            print '\t'.join(data)


LogObj = LogClass()

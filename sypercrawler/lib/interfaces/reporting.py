'''Interface that allows to a class have a collection of messages to report'''
from pprint import pformat


class ReportingMessage(object):

    def __repr__(self, *args, **kwargs):
        return self._message

    def __init__(self, message="", prefix=""):
        self._message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message, prefix=""):
        if(prefix):
            message = "[%s] %s" % (prefix + message)
        self._message = message


class MessageReport():

    def __init__(self):
        self._report_messages = []

    @property
    def report_messages(self):
        return self._report_messages

    def add_report_message(self, report_message, prefix=""):
        self.report_messages.append(ReportingMessage(report_message, prefix))

    def last_report_messages(self):
        return self.report_messages[len(self.report_messages) - 1]

    def modify_last_report_messages(self, message):
        self.report_messages.message(message)

    def console_report(self):
        report = {}
        report[repr(self)] = self.report_messages
        return report

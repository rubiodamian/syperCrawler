'''Interface that allows to a class have a collection of messages to report'''


class ReportingMessage(object):

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

    def add_report_messages(self, report_messages, prefix=""):
        self.report_messages.append(ReportingMessage(report_messages, prefix))

    def last_report_messages(self):
        return self.report_messages[len(self.report_messages) - 1]

    def modify_last_report_messages(self, message):
        self.report_messages.message(message)

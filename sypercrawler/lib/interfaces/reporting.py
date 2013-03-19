'''Interface that allows to a class have a collection of messages to report'''
class ReportingMessage(object):

    def __init__(self, message="", prefix=""):
        self.setMessage(message)
    
    def setMessage(self, message, prefix=""):
        if(prefix):
            message = "[%s] %s" % (prefix + message)
        self.message = message
    
    def getMessage(self):
        return self.message
    
class MessageReport():
    
    def __init__(self):
        self.reportMessages = []
    
    def getReportMessages(self):
        return self.reportMessages

    def addReportMessage(self, reportMessage, prefix=""):
        self.getReportMessages().append(ReportingMessage(reportMessage,prefix))
        
    def getLastReportMessage(self):
        return self.getReportMessages()[len(self.getReportMessages())-1]
        
    def modifyLastReportMessage(self,message):
        self.getLastReportMessage().setMessage(message)

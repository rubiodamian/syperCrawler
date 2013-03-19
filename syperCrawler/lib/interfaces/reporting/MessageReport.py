from syperCrawler.lib.interfaces.reporting.ReportingMessage import ReportingMessage
'''Interface that allows to a class have a collection of messages to report'''
class MessageReport():
    reportMessages = []
    
    def getReportMessages(self):
        return self.reportMessages

    def addReportMessage(self, reportMessage, prefix=""):
        self.getReportMessages().append(ReportingMessage(reportMessage,prefix))
        
    def getLastReportMessage(self):
        return self.getReportMessages()[len(self.getReportMessages())-1]
        
    def modifyLastReportMessage(self,message):
        self.getLastReportMessage().setMessage(message)

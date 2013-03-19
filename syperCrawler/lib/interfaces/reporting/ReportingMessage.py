
class ReportingMessage(object):
    message = ""
    def __init__(self, message="", prefix=""):
        self.setMessage(message)
    
    def setMessage(self, message, prefix=""):
        if(prefix):
            message = "[%s] %s" % (prefix + message)
        self.message = message
    
    def getMessage(self):
        return self.message
        

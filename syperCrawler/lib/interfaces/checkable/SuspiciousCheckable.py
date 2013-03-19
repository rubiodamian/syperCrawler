class SuspiciousCheckable():
    def checkForSuspiciousStuff(self, spider=None, pipeline=None):
        raise NotImplementedError("Should have implemented this")
    
    def suspiciousUrl(self, spider=None, pipeline=None):
        raise NotImplementedError("Should have implemented this")
    
    def suspiciousHidden(self, spider=None, pipeline=None):
        raise NotImplementedError("Should have implemented this")
   
    def suspiciousSize(self, spider=None, pipeline=None):
        raise NotImplementedError("Should have implemented this")
    
    def suspiciousSizeTagAdditions(self, spider=None, pipeline=None):
        raise NotImplementedError("Should have implemented this")

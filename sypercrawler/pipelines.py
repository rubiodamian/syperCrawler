# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log

class TagPipeline(object):
    
    def __repr__(self, *args, **kwargs):
        return self.__class__.__name__
    
    def getTagCollection(self, item):
        raise NotImplementedError("Should have implemented this")
    
    def getTagDescription(self):
        raise NotImplementedError("Should have implemented this")
    
    def process_item(self, item, spider):
        log.msg("[%s] Checking %s for suspicious %s...\n" % (self, item.getUrl(), self.getTagDescription()), level=log.INFO, spider=spider)
        for tag in self.getTagCollection(item):
            log.msg("[%s] Processing %r..." % (self, tag), level=log.INFO, spider=spider)
            if(not spider.isUrlInBlackList(tag.getSrc())):
                tag.setItemContext(item.getUrl(),spider,self)
                tag.checkForSuspiciousStuff()
                spider.addUrlToBlackList(tag.getSrc())
            print "\t"
        log.msg("[%r] END\n" % (self), level=log.INFO, spider=spider)
        return item

class ScriptTagPipeline(TagPipeline):
    
    def getTagCollection(self, item):
        return item.getScriptTags()
    
    def getTagDescription(self):
        return '<script> tags'

class IframeTagPipeline(TagPipeline):
    
    def getTagCollection(self, item):
        return item.getIframeTags()
    
    def getTagDescription(self):
        return '<iframe> tags'
    
class ATagPipeline(TagPipeline):
    
    def getTagCollection(self, item):
        return item.getATags()
    
    def getTagDescription(self):
        return '<a> tags'
    
class ImgTagPipeline(TagPipeline):
    
    def getTagCollection(self, item):
        return item.getImgTags()
    
    def getTagDescription(self):
        return '<img> tags'
                        

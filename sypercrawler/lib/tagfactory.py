<<<<<<< HEAD
from sypercrawler.lib.tag import ATag, IframeTag, ImgTag, ScriptTag, NullTag
from string import capitalize


class TagFactory():

    def getTagFromStr(self, nodename):
        try:
            klass = str(capitalize(str(nodename)) + 'Tag')
            return globals()[klass]()
        except Exception as e:
            print str(e)
            return NullTag()

    def getTagFromHtmlXPathSelector(self, htmlXPS):
        nodename = htmlXPS.select('local-name()').extract()[0]
        tag = self.getTagFromStr(nodename)
        tag.fillFromHtmlXpathSelector(htmlXPS)
        return tag

    def getTagsFromHtmlXPathSelector(self, htmlXPSs):
        tags = []
        for htmlXPS in htmlXPSs:
            tags.append(self.getTagFromHtmlXPathSelector(htmlXPS))
        return tags
=======
from sypercrawler.lib.tag import ATag,IframeTag,ImgTag,ScriptTag,NullTag
from string import capitalize

class TagFactory():
    
    def getTagFromStr(self, nodename):
        try:
            klass = str(capitalize(str(nodename)) + 'Tag')
            return globals()[klass]()
        except Exception as e:
            print str(e)
            return NullTag()
    
    def getTagFromHtmlXPathSelector(self, htmlXPS):
        nodename = htmlXPS.select('local-name()').extract()[0]
        tag = self.getTagFromStr(nodename)
        tag.fillFromHtmlXpathSelector(htmlXPS)
        return tag
    
    def getTagsFromHtmlXPathSelector(self, htmlXPSs):
        tags = []
        for htmlXPS in htmlXPSs:
            tags.append(self.getTagFromHtmlXPathSelector(htmlXPS))
        return tags
            
>>>>>>> branch 'master' of https://github.com/rubiodamian/syperCrawler.git

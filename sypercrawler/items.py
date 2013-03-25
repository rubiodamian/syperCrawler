# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
# un pipe por tag, reportar con arbol de objetos al q le mando el xpath y se imprimen

from scrapy.item import Item, Field
from sypercrawler.lib.tagfactory import TagFactory


class ResponseItem(Item):
    url = Field()
    scriptTags = Field()
    aTags = Field()
    imgTags = Field()
    iframeTags = Field()

#    def __str__(self, *args, **kwargs):
#        return "aaaaaa"
#
#    def __repr__(self):
#        return "asdasd"

    def getUrl(self):
        return self.get('url', 'no url')

    def setUrl(self, url):
        self['url'] = url

    def getScriptTags(self):
        return self.get('scriptTags', {})

    def setScriptTags(self, scriptTags):
        self['scriptTags'] = TagFactory().tags_from_html_xpathselector(scriptTags)

    def getATags(self):
        return self.get('aTags', {})

    def setATags(self, aTags):
        self['aTags'] = TagFactory().tags_from_html_xpathselector(aTags)

    def getImgTags(self):
        return self.get('imgTags', {})

    def setImgTags(self, imgTags):
        self['imgTags'] = TagFactory().tags_from_html_xpathselector(imgTags)

    def getIframeTags(self):
        return self.get('iframeTags', {})

    def setIframeTags(self, iframeTags):
        self['iframeTags'] = TagFactory().tags_from_html_xpathselector(iframeTags)

    def getDebug(self):
        return self.get('debug')

    def setDebug(self, debug):
        self['debug'] = debug

    def getError(self):
        return self.get('error')

    def setError(self, error):
        self['error'] = error

    def getInfo(self):
        return self.get('info')

    def setInfo(self, info):
        self['info'] = info

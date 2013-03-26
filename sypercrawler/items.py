# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
# un pipe por tag, reportar con arbol de objetos al q le mando el xpath y se imprimen

from scrapy.item import Item, Field
from sypercrawler.lib.tagfactory import TagFactory


class ResponseItem(Item):
    url = Field()
    script_tags = Field()
    a_tags = Field()
    img_tags = Field()
    iframe_tags = Field()

    def get_url(self):
        return self.get('url', 'no url')

    def set_url(self, url):
        self['url'] = url

    def get_script_tags(self):
        return self.get('script_tags', {})

    def set_script_tags(self, script_tags):
        self['script_tags'] = TagFactory().tags_from_html_xpathselector(script_tags)

    def get_a_tags(self):
        return self.get('a_tags', {})

    def set_a_tags(self, a_tags):
        self['a_tags'] = TagFactory().tags_from_html_xpathselector(a_tags)

    def get_img_tags(self):
        return self.get('img_tags', {})

    def set_img_tags(self, img_tags):
        self['img_tags'] = TagFactory().tags_from_html_xpathselector(img_tags)

    def get_iframe_tags(self):
        return self.get('iframe_tags', {})

    def set_iframe_tags(self, iframe_tags):
        self['iframe_tags'] = TagFactory().tags_from_html_xpathselector(iframe_tags)

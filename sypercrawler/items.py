# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
# un pipe por tag, reportar con arbol de objetos al q le mando el xpath y se imprimen

from scrapy.item import Item, Field
from sypercrawler.lib.tagfactory import TagFactory
from pprint import pformat


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

    def tag_collections(self):
        tag_collection = []
        for (k, v) in self.items():
            if(k != 'url'):
                tag_collection += v
        return  tag_collection

    def console_report(self):
        report = []
        for tag in self.tag_collections():
            report.append(tag.console_report())
        return pformat(report)

    def is_empty(self):
        return not len(self.tag_collections())

    def is_suspicious(self):
        for tag in self.tag_collections():
            if(tag.is_suspicious()):
                return True
        return False

    def clean_out(self):
        for (k, v) in self.items():
            if(k != 'url'):
                suspicious_tags = list(tag for tag in v if tag.is_suspicious())
                if(not len(suspicious_tags)):
                    del self[k]
                else:
                    self[k] = suspicious_tags


class NullItem(ResponseItem):

    def __call__(self, *args, **kwargs):
        "Ignore method calls."
        return self

    def __repr__(self):
        "Return a string representation."
        return "<Null>"

    def __str__(self):
        "Convert to a string and return it."
        return "Null"

    def tag_collections(self):
        return  None

    def console_report(self):
        return None

    def is_empty(self):
        return True

    def is_suspicious(self):
        return False

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log


class TagPipeline(object):

    def __repr__(self, *args, **kwargs):
        return self.__class__.__name__

    def tag_collection(self, item):
        raise NotImplementedError("Should have implemented this")

    def tag_description(self):
        raise NotImplementedError("Should have implemented this")

    def process_item(self, item, spider):
        log.msg("[%s] Checking %s for suspicious %s...\n" % (self, item.get_url(), self.tag_description()), level=log.INFO, spider=spider)
        for tag in self.tag_collection(item):
            log.msg("[%s] Processing %r..." % (self, tag), level=log.INFO, spider=spider)
            if(not spider.is_url_in_blacklist(tag.src)):
                tag.item_context(item.get_url(), spider, self)
                tag.check_for_suspicious_stuff()
                spider.add_url_to_blacklist(tag.src)
            print "\t"
        log.msg("[%r] END\n" % (self), level=log.INFO, spider=spider)
        return item


class ScriptTagPipeline(TagPipeline):

    def tag_collection(self, item):
        return item.get_script_tags()

    def tag_description(self):
        return '<script> tags'


class IframeTagPipeline(TagPipeline):

    def tag_collection(self, item):
        return item.get_iframe_tags()

    def tag_description(self):
        return '<iframe> tags'


class ATagPipeline(TagPipeline):

    def tag_collection(self, item):
        return item.get_a_tags()

    def tag_description(self):
        return '<a> tags'


class ImgTagPipeline(TagPipeline):

    def tag_collection(self, item):
        return item.img_tags

    def tag_description(self):
        return '<img> tags'

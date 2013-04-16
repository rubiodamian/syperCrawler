# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log
from sypercrawler.items import NullItem


class FirstPipeline(object):

    def __repr__(self, *args, **kwargs):
        return self.__class__.__name__

    def process_item(self, item, spider):
        if(item):
            log.msg("Starting the verification of <%s>:" % (item.get_url()), level=log.INFO, spider=spider)
        else:
            log.msg("Nothing to verify", level=log.INFO, spider=spider)
        return item


class EmptyItemFilterPipeline(object):

    def process_item(self, item, spider):
        if (item.is_empty()):
            return NullItem()
        else:
            return item


class TagPipeline(object):

    def __repr__(self, *args, **kwargs):
        return self.__class__.__name__

    def tag_collection(self, item):
        raise NotImplementedError("Should have implemented this")

    def tag_description(self):
        raise NotImplementedError("Should have implemented this")

    def process_item(self, item, spider):
        if(item):
            log.msg("[%s] Checking %s for suspicious %s...\n" % (self, item.get_url(), self.tag_description()), level=log.INFO, spider=spider)
            for tag in self.tag_collection(item):
                if(not spider.is_a_visited_url(tag.src)):
                    log.msg("[%s] Processing %r...\n" % (self, tag), level=log.INFO, spider=spider)
                    tag.item_context(item.get_url(), spider, self)
                    tag.check_for_suspicious_stuff()
                    spider.add_visited_url(tag.src)
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
        return item.get_img_tags()

    def tag_description(self):
        return '<img> tags'


class NotSuspiciousItemFilterPipeline(object):

    def process_item(self, item, spider):
        if (not item.is_suspicious()):
            return NullItem()
        else:
            item.clean_out()
            return item


class ConsoleReportPipeline(object):

    def process_item(self, item, spider):
        if(item):
            msg = "[Report] %s report:\n %s \n" % (item.get_url(), item.console_report())
            log.msg(msg, level=log.INFO, spider=spider)
            if(spider.report_file):
                spider.report_file.write(msg + "\n")
        return item

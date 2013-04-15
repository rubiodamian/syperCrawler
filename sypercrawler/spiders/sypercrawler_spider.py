from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.http import FormRequest
#from scrapy.http import Request
from scrapy import log

from sypercrawler.items import ResponseItem


class SyperCrawlerSpider(CrawlSpider):
    name = "syperCrawler"
#    allowed_domains = ['localhost']
#     login_page = 'http://localhost/dvwa/login.php'
    #start_urls = ['http://localhost/test/']  # urls from which the spider will start crawling
    rules = [Rule(SgmlLinkExtractor(), callback='parse_item')]

    def __init__(self, urls=None, domains=None, *a, **kw):
        CrawlSpider.__init__(self, *a, **kw)
        if(urls):
            self.start_urls = urls.split(",")
        if(domains):
            self.allowed_domains = domains.split(",")
#     def parse(self, response):
#         return [FormRequest.from_response(response,
#             formdata={'username': 'admin', 'password': 'password'},
#             callback=self.after_login)]
#     def after_login(self, response):
#         # check login succeed before going on
#         if "authentication failed" in response.body:
#             self.log("Login failed", level=log.ERROR)
#             return
#         else:
#             self.log("Login successful", level=log.INFO)
#             return Request(url="http://localhost/dvwa/vulnerabilities/xss_s/",
#                    callback=self.parse_tastypage)
    _visited_urls = []

    @property
    def visited_urls(self):
        return self._visited_urls

    @visited_urls.setter
    def visited_urls(self, visited_urls):
        self._visited_urls = visited_urls

    def add_visited_url(self, url):
        if(url):
            self.visited_urls.append(url)

    def is_a_visited_url(self, url):
        return url in self.visited_urls

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = ResponseItem()
        item.set_url(response.url)
        print "\n"
        log.msg("Starting the parsing of <%s>:" % (item.get_url()), level=log.INFO, spider=self)
        log.msg("Parsing <a> tags...", level=log.INFO, spider=self)
        item.set_a_tags(hxs.select('//a[contains(@href, "http")]'))
        log.msg("Parsing <iframe> tags...", level=log.INFO, spider=self)
        item.set_iframe_tags(hxs.select('//iframe[contains(@src, "http")]'))
        log.msg("Parsing <script> tags...", level=log.INFO, spider=self)
        item.set_script_tags(hxs.select('//script'))
        log.msg("Parsing <img> tags...", level=log.INFO, spider=self)
        item.set_img_tags(hxs.select('//img[contains(@src, "http")]'))
        log.msg("End of <%s> parse.\n" % (item.get_url()), level=log.INFO, spider=self)
        return item

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy import log

from sypercrawler.items import ResponseItem


class SyperCrawlerSpider(CrawlSpider):
    name = "syperCrawler"
    allowed_domains = ['localhost']
#     login_page = 'http://localhost/dvwa/login.php'
    start_urls = ['http://localhost/test/']  # urls from which the spider will start crawling
    rules = [Rule(SgmlLinkExtractor(allow=[r'/test/test*']), callback='parse_item')]

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
    urlBlackList = []

    def getUrlBlackList(self):
        return self.urlBlackList

    def setUrlBlackList(self, urlBlackList):
        self.urlBlackList = urlBlackList

    def addUrlToBlackList(self, url):
        if(url):
            self.getUrlBlackList().append(url)

    def isUrlInBlackList(self, url):
        return url in self.getUrlBlackList()

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = ResponseItem()
        item.setUrl(response.url)
        print "\t"
        self.log("Parsing <a> tags...", level=log.INFO)
        item.setATags(hxs.select('//a[contains(@href, "http")]'))
        self.log("Parsing <iframe> tags...", level=log.INFO)
        item.setIframeTags(hxs.select('//iframe[contains(@src, "http")]'))
        self.log("Parsing <script> tags...", level=log.INFO)
        item.setScriptTags(hxs.select('//script'))
        self.log("Parsing <img> tags...\n", level=log.INFO)
        item.setImgTags(hxs.select('//img[contains(@src, "http")]'))
        return item

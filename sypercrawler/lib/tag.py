# allow to the division return a result
from __future__ import division
from sypercrawler.lib.browsinglookups.SafebrowsinglookupSingleton import SafebrowsinglookupClient
from sypercrawler.lib.interfaces.reporting import MessageReport
from sypercrawler.lib.interfaces.itemcontext import ItemContext
from sypercrawler.lib import linkcheck
from sypercrawler.lib.keywordanalizer import KeywordAnalizer
from scrapy import log
import unicodedata
import mimetypes
import urlparse
import urllib2


class Tag(object, MessageReport, ItemContext):

    def __init__(self, src="", unicode_tag=""):
        ItemContext.__init__(self, "", "", "")
        MessageReport.__init__(self)
        self._src = src
        self._unicode_tag = unicode_tag

    def __str__(self, *args, **kwargs):
        return "%s()" % (self.__class__.__name__)

    def __repr__(self, *args, **kwargs):
        return "%s('%s...')" % (self.__class__.__name__, self.src[0:30])

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, src):
        self._src = str(src)

    @property
    def unicode_tag(self):
        return self._unicode_tag

    @unicode_tag.setter
    def unicode_tag(self, unicode_tag):
        self._unicode_tag = str(''.join(c for c in unicodedata.normalize('NFD', unicode(unicode_tag)) if unicodedata.category(c) != 'Mn'))

    def fill_from_html_xpathselector(self, htmlXPS):
        src = htmlXPS.select('@src').extract()
        if(src):
            self.src = src[0]
        self.unicode_tag = htmlXPS.extract()

    def check_remote_url(self, url):
        response = linkcheck.check_url(url)
        if(isinstance(response, int)):
            if(response / 100 == 2):  # success
                log.msg("[%s] %r reference status its ok (%d)" % (self.pipeline, self, response), level=log.DEBUG, spider=self.spider)
                veredict = SafebrowsinglookupClient().lookup(url)
                if(veredict[url] in ('phishing', 'malware', 'phishing,malware')):
                    self.add_report_message("%s found in the remote URL %s" % (self.pipeline, veredict[url].capitalize(), url), "DANGER")
                    log.msg("[%s] %s found in the remote URL %s" % (self.pipeline(), veredict[url].capitalize(), url), level=log.DEBUG, spider=self.spider)
                log.msg("[%s] Google safe browsing lookup veredict:(%s : %s)" % (self.pipeline, url, veredict[url]), level=log.DEBUG, spider=self.spider)

            elif(response / 100 == 4):  # client error, probably broken link
                self.add_report_message("The url refence '%s' is broken (status code %d)" % (url, response), "WARNING")
                log.msg("[%s] %r reference is broken (status code %d)" % (self.pipeline, self, response), level=log.DEBUG, spider=self.spider)

            elif(response / 100 == 5):  # server error, probably a temporarily broken link
                self.add_report_message("The url refence '%s' server error (status code %d)" % (url, response), "WARNING")
                log.msg("[%s] %r reference is broken (status code %d)" % (self.pipeline, self, response), level=log.DEBUG, spider=self.spider)
        else:
            log.msg("[%s] %r redirection detected!(from %s to %s)" % (self.pipeline, self, url, response), level=log.DEBUG, spider=self.spider)
            self.add_report_message("The url refence '%s' redirects to %s )" % (url, response), "WARNING")
            self.check_remote_url(response)

    def suspicious_url(self):
        url = self.src
        if(url):
            log.msg("[%s] Checking for malicious remote sites..." % (self.pipeline), level=log.INFO, spider=self.spider)
            self.check_remote_url(url)

    def check_for_suspicious_stuff(self):
        self.suspicious_url()

    def image_mime_types(self):
        return ['image/gif', 'image/jpeg', 'image/png', 'application/x-shockwave-flash',
                'image/psd', 'image/bmp image/tiff', 'image/tiff', 'application/octet-stream',
                'image/jp2 ', 'application/octet-stream', 'application/octet-stream',
                 'application/x-shockwave-flash', 'image/iff', 'image/vnd.wap.wbmp',
                  'image/xbm', 'image/vnd.microsoft.icon']

    def url_extension(self, url):
        return mimetypes.guess_type(urlparse.urlsplit(url)[2])[0]

    def is_image(self):
        return self.url_extension(self.src) in self.image_mime_types()

    def is_suspicious(self):
        return len(self.report_messages)

class ATag(Tag):

    def fill_from_html_xpathselector(self, htmlXPS):
        src = htmlXPS.select('@href').extract()
        if(src):
            self.src = src[0]
        self.unicode_tag = htmlXPS.extract()


class ScriptTag(Tag):

    def __init__(self, src="", unicodeTag="", body=""):
        Tag.__init__(self, src, unicodeTag)
        self._body = body

    def __repr__(self, *args, **kwargs):
        if(self.src):
            src = self.src
        else:
            src = self.body.strip()
        return "%s('%s...')" % (self.__class__.__name__, src[0:30])

    @property
    def src(self):
        src = Tag.src.fget(self)
        if(src):
            if(not urlparse.urlparse(src)[0]):
                return urlparse.urljoin(self.current_url, src)
        return src

    @src.setter
    def src(self, src):
        self._src = src

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = str(body)

    def fill_from_html_xpathselector(self, htmlXPS):
        Tag.fill_from_html_xpathselector(self, htmlXPS)
        body = htmlXPS.select('text()')
        if(body):
            self.body = body.extract()[0]

    def javascript_code(self):
        url = self.src
        if(url):
            if(self.url_extension(url) == 'application/javascript'):
                t = urllib2.urlopen(url)
                js = t.read()
                return js
        else:
            return self.body

    def check_for_obfuscated_javascript(self):
        pass

    def check_for_suspicious_stuff(self):
        Tag.check_for_suspicious_stuff(self)
        self.check_for_obfuscated_javascript()


class SizeableTag(Tag):

    def __init__(self, src="", unicodeTag="", height=99, width=99, style=""):
        Tag.__init__(self, src, unicodeTag)
        self._height = height
        self._width = width
        self._style = style

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = int(height)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = int(width)

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        self._style = str(style)

    def fill_from_html_xpathselector(self, htmlXPS):
        Tag.fill_from_html_xpathselector(self, htmlXPS)
        height = htmlXPS.select('@height').extract()
        width = htmlXPS.select('@height').extract()
        style = htmlXPS.select('@style').extract()
        if(height):
            self.height = height[0]
        if(width):
            self.width = width[0]
        if(style):
            self.style = style[0]

    def suspicious_size(self):
        log.msg("[%s] Checking for suspicious size..." % (self.pipeline), level=log.INFO, spider=self.spider)
        if((self.height < 5) or (self.width < 5)):
            self.add_report_message("Suspicious size found!! This tag is suspiciously small")
            log.msg("[%s] Suspicious size found!! This tag (%r) is suspiciously small" % (self.pipeline, self), level=log.DEBUG, spider=self.spider)
            self.suspicious_size_tag_additions()
            return True
        else:
            return False

    def suspicious_size_tag_additions(self):
        raise NotImplementedError("Should have implemented this")

    def suspicious_hidden(self):
        log.msg("[%s] Checking for hidden tags..." % (self.pipeline), level=log.INFO, spider=self.spider)
        style_words = set(self.style.replace(" ", "").replace(";", ":").split(":"))
        if(set(["visibility", "hidden"]).issubset(style_words) or set(["display", "none"]).issubset(style_words)):
            self.add_report_message("%r: this tag is suspiciously hidden!" % (self))
            log.msg("[%s] %r: this tag is suspiciously hidden!" % (self.pipeline, self), level=log.DEBUG, spider=self.spider)

    def check_for_suspicious_stuff(self):
        Tag.check_for_suspicious_stuff(self)
        self.suspicious_size()
        self.suspicious_hidden()


class ImgTag(SizeableTag):

    def __init__(self, src="", unicodeTag="", height=99, width=99, style="", alt=""):
        SizeableTag.__init__(self, src=src, unicodeTag=unicodeTag, height=height, width=width, style=style)
        self._alt = alt

    @property
    def alt(self):
        return self._alt

    @alt.setter
    def alt(self, alt):
        self._alt = str(''.join(c for c in unicodedata.normalize('NFD', unicode(alt)) if unicodedata.category(c) != 'Mn'))

    def fill_from_html_xpathselector(self, htmlXPS):
        SizeableTag.fill_from_html_xpathselector(self, htmlXPS)
        alt = htmlXPS.select('@alt').extract()
        if(alt):
            self.alt = alt[0]

    def suspicious_size_tag_additions(self):
        pass

    def check_for_keywordstuffing(self):
        log.msg("[%s] Checking for keyword stuffing..." % (self.pipeline), level=log.INFO, spider=self.spider)
        if(KeywordAnalizer().check_for_keywordstuffing(self.alt)):
            log.msg("[%s] %r is victim of keyword stuffing!!" % (self.pipeline, self), level=log.DEBUG, spider=self.spider)
            self.add_report_message("This tag is victim of keyword stuffing!!")

    def check_for_suspicious_extension(self):
        log.msg("[%s] Checking for suspicious extension..." % (self.pipeline), level=log.INFO, spider=self.spider)
        if(not self.is_image()):
            log.msg("[%s] %r reference is not an image!! that is really suspicious..." % (self.pipeline, self), level=log.DEBUG, spider=self.spider)
            self.add_report_message("This tag is not an image!!")

    def check_for_suspicious_stuff(self):
        self.check_for_suspicious_extension()
        SizeableTag.check_for_suspicious_stuff(self)
        self.check_for_keywordstuffing()


class IframeTag(SizeableTag):

    def __init__(self, src="", unicodeTag="", height=99, width=99, style="", frameborder=99):
        SizeableTag.__init__(self, src=src, unicodeTag=unicodeTag, height=height, width=width, style=style)
        self._frameborder = frameborder

    @property
    def frameborder(self):
        return self._frameborder

    @frameborder.setter
    def frameborder(self, frameborder):
        self._frameborder = int(frameborder)

    def suspicious_frameborder(self):
        return not self.frameborder  # suspicious is if frameborder is equal to zero

    def suspicious_size_tag_additions(self):
        if(self.suspicious_frameborder()):
            self.add_report_message("And have frameborder = 0(zero) too...thats really suspicious!")
            log.msg("[%s] %r is small and have frameborder = 0(zero)...thats \
            really suspicious!" % (self.pipeline, self), level=log.DEBUG, spider=self.spider)

    def fill_from_html_xpathselector(self, htmlXPS):
        SizeableTag.fill_from_html_xpathselector(self, htmlXPS)
        frameborder = htmlXPS.select('@frameborder').extract()
        if(frameborder):
            self.frameborder = htmlXPS.select('@frameborder').extract()[0]


class NullTag(SizeableTag):
    def __init__(self, *args, **kwargs):
        "Ignore parameters."
        return None

    # object calling

    def __call__(self, *args, **kwargs):
        "Ignore method calls."
        return self

    # attribute handling

    def __getattr__(self, mname):
        "Ignore attribute requests."
        return self

    def __setattr__(self, name, value):
        "Ignore attribute setting."
        return self

    def __delattr__(self, name):
        "Ignore deleting attributes."
        return self

    def __repr__(self):
        "Return a string representation."
        return "<Null>"

    def __str__(self):
        "Convert to a string and return it."
        return "Null"

    def fill_from_html_xpathselector(self, htmlXPS):
        return self

    def suspicious_size(self):
        pass

    def suspicious_url(self):
        pass

    def suspicious_hidden(self):
        pass

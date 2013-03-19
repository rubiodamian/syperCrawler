from __future__ import division
from syperCrawler.lib.safebrowsinglookup.SafebrowsinglookupSingleton import SafebrowsinglookupClient
from syperCrawler.lib.interfaces.reporting.MessageReport import MessageReport
from syperCrawler.lib.interfaces.ItemContext import ItemContext
from syperCrawler.lib.LinkChecker import LinkChecker
from syperCrawler.lib.KeywordAnalizer import KeywordAnalizer
from scrapy import log
import unicodedata, mimetypes, urlparse, urllib2
from urlparse import urlsplit
from syperCrawler.lib import jsbeautifier

class Tag(object, MessageReport, ItemContext):
	src = ""
	unicodeTag = ""
		
	def __init__(self, src="", unicodeTag=""):
		self.setSrc(src)
		self.setUnicodeTag(unicodeTag)
	
	def __str__(self, *args, **kwargs):
		return "%s()" % (self.__class__.__name__)
	
	def __repr__(self, *args, **kwargs):
		return "%s('%s...')" % (self.__class__.__name__, self.getSrc()[0:30])
	
	def getSrc(self):
		return self.src

	def setSrc(self, src):
		self.src = str(src)
		
	def getUnicodeTag(self):
		return self.unicodeTag

	def setUnicodeTag(self, unicodeTag):
		self.unicodeTag = str(''.join(c for c in unicodedata.normalize('NFD', unicode(unicodeTag)) if unicodedata.category(c) != 'Mn'))
	
	def fillFromHtmlXpathSelector(self, htmlXPS):
		src = htmlXPS.select('@src').extract()
		if(src):
			self.setSrc(src[0])
		self.setUnicodeTag(htmlXPS.extract())
	
	def checkRemoteURL(self, url):
		response = LinkChecker().checkURL(url)
		if(isinstance(response, int)):
			if(response / 100 == 2):  # success
				log.msg("[%s] %r reference status its ok (%d)" % (self.getPipeline(), self, response), level=log.DEBUG, spider=self.getSpider())
				veredict = SafebrowsinglookupClient().lookup(url)
				if(veredict[url] in ('phishing', 'malware', 'phishing,malware')):
					self.addReportMessage("%s found in the remote URL %s" % (self.getPipeline(), veredict[url].capitalize(), url), "DANGER")
					log.msg("[%s] %s found in the remote URL %s" % (self.getPipeline(), veredict[url].capitalize(), url), level=log.DEBUG, spider=self.getSpider())
				log.msg("[%s] Google safe browsing lookup veredict:(%s : %s)" % (self.getPipeline(), url, veredict[url]), level=log.DEBUG, spider=self.getSpider())
			
			elif(response / 100 == 4):  # client error, probably broken link
				self.addReportMessage("The url refence '%s' is broken (status code %d)" % (url, response), "WARNING")
				log.msg("[%s] %r reference is broken (status code %d)" % (self.getPipeline(), self, response), level=log.DEBUG, spider=self.getSpider())
			
			elif(response / 100 == 5):  # server error, probably a temporarily broken link
				self.addReportMessage("The url refence '%s' server error (status code %d)" % (url, response), "WARNING")
				log.msg("[%s] %r reference is broken (status code %d)" % (self.getPipeline(), self, response), level=log.DEBUG, spider=self.getSpider())
		else:
			log.msg("[%s] %r redirection detected!(from %s to %s)" % (self.getPipeline(), self, url, response), level=log.DEBUG, spider=self.getSpider())
			self.addReportMessage("The url refence '%s' redirects to %s )" % (url, response), "WARNING")
			self.checkRemoteURL(response)
	
	
	def suspiciousUrl(self):
		url = self.getSrc()
		if(url):
			log.msg("[%s] Checking for malicious remote sites..." % (self.getPipeline()), level=log.INFO, spider=self.getSpider())
			self.checkRemoteURL(url)
		
	def checkForSuspiciousStuff(self):
		self.suspiciousUrl()
		
	def getImageMimeTypes(self):
		return ['image/gif', 'image/jpeg' , 'image/png'  , 'application/x-shockwave-flash'  , 'image/psd'  , 'image/bmp image/tiff'  , 'image/tiff'  , 'application/octet-stream'  , 'image/jp2 ' , 'application/octet-stream', 'application/octet-stream' , 'application/x-shockwave-flash' , 'image/iff' , 'image/vnd.wap.wbmp', 'image/xbm' , 'image/vnd.microsoft.icon']
	
	def getURLExtension(self, url):
		return mimetypes.guess_type(urlsplit(url)[2])[0]
	
	def isImage(self):
		return self.getURLExtension(self.getSrc()) in self.getImageMimeTypes()
		
class ATag(Tag):
	def fillFromHtmlXpathSelector(self, htmlXPS):
		src = htmlXPS.select('@href').extract()
		if(src):
			self.setSrc(src[0])
		self.setUnicodeTag(htmlXPS.extract())
			
class ScriptTag(Tag):
	body = ""
	
	def __init__(self, src="", unicodeTag="", body=""):
		Tag.__init__(self, src, unicodeTag)
	
	def __repr__(self, *args, **kwargs):
		if(self.getSrc()):
			src= self.getSrc()
		else:
			src= self.getBody().strip()
		return "%s('%s...')" % (self.__class__.__name__, src[0:30])
	
	def getSrc(self):
		if(self.src):
			if(not urlparse.urlparse(self.src)[0]):
				return urlparse.urljoin(self.getCurrentUrl(), self.src)
		return self.src
	
	def getBody(self):
		return self.body
	
	def setBody(self, body):
		self.body = str(body)
	
	def fillFromHtmlXpathSelector(self, htmlXPS):
		Tag.fillFromHtmlXpathSelector(self, htmlXPS)
		body = htmlXPS.select('text()')
		if(body):
			self.setBody(body.extract()[0])

	def getJavascriptCode(self):
		url = self.getSrc()
		if(url):
			if(self.getURLExtension(url) == 'application/javascript'):
				t = urllib2.urlopen(url)
				js = t.read()
				return js
		else:
			return self.getBody()
		
	def checkForObfuscatedJavascript(self):
		js = self.getJavascriptCode()
#		print len(jsbeautifier.beautify(js)),jsbeautifier.beautify(js)
#		print "\n"
#		print len(js),js
		from syperCrawler.lib.jsunpck import jsunpck
#		obj = jsunpck.parse(js)
		print jsbeautifier.beautify(js)
		print len(js)

	def checkForSuspiciousStuff(self):
		Tag.checkForSuspiciousStuff(self)
		self.checkForObfuscatedJavascript()

class SizeableTag(Tag):
	height = 99
	width = 99
	style = ""
	def __init__(self, src="", unicodeTag="", height=0, width=0):
		Tag.__init__(self, src, unicodeTag)
		self.setHeight(height)
		self.setWidth(width)

	def getHeight(self):
		return self.height

	def setHeight(self, height):
		self.height = int(height)

	def getWidth(self):
		return self.width

	def setWidth(self, width):
		self.width = int(width)
	
	def getStyle(self):
		return self.style

	def setStyle(self, style):
		self.style = str(style)
	
	def fillFromHtmlXpathSelector(self, htmlXPS):
		Tag.fillFromHtmlXpathSelector(self, htmlXPS)
		height = htmlXPS.select('@height').extract()
		width = htmlXPS.select('@height').extract()
		style = htmlXPS.select('@style').extract()
		if(height):
			self.setHeight(height[0])
		if(width):
			self.setWidth(width[0])
		if(style):
			self.setStyle(style[0])
	
	def suspiciousSize(self):
		log.msg("[%s] Checking for suspicious size..." % (self.getPipeline()), level=log.INFO, spider=self.getSpider())
		if((self.getHeight() < 5) or (self.getWidth() < 5)):
			self.addReportMessage("Suspicious size found!! This tag is suspiciously small")
			log.msg("[%s] Suspicious size found!! This tag (%r) is suspiciously small" % (self.getPipeline(), self), level=log.DEBUG, spider=self.getSpider())
			self.suspiciousSizeTagAdditions()
			return True
		else:
			return False
	
	def suspiciousSizeTagAdditions(self):
		raise NotImplementedError("Should have implemented this")
	
	def suspiciousHidden(self):
		log.msg("[%s] Checking for hidden tags..." % (self.getPipeline()), level=log.INFO, spider=self.getSpider())
		styleWords = set(self.getStyle().replace(" ", "").replace(";", ":").split(":"))
		if(set(["visibility", "hidden"]).issubset(styleWords) or set(["display", "none"]).issubset(styleWords)):
			self.addReportMessage("%r: this tag is suspiciously hidden!" % (self))
			log.msg("[%s] %r: this tag is suspiciously hidden!" % (self.getPipeline(), self), level=log.DEBUG, spider=self.getSpider())
	
	def checkForSuspiciousStuff(self):
		Tag.checkForSuspiciousStuff(self)
		self.suspiciousSize()
		self.suspiciousHidden()	

class ImgTag(SizeableTag):
	alt = ""
	
	def getAlt(self):
		return self.alt

	def setAlt(self, alt):
		self.alt = str(''.join(c for c in unicodedata.normalize('NFD', unicode(alt)) if unicodedata.category(c) != 'Mn'))
	
	def fillFromHtmlXpathSelector(self, htmlXPS):
		SizeableTag.fillFromHtmlXpathSelector(self, htmlXPS)
		alt = htmlXPS.select('@alt').extract()
		if(alt):
			self.setAlt(alt[0])
		
	def suspiciousSizeTagAdditions(self):
		pass
	
	def checkForKeywordStuffing(self):
		log.msg("[%s] Checking for keyword stuffing..." % (self.getPipeline()), level=log.INFO, spider=self.getSpider())
		if(KeywordAnalizer().checkForKeywordStuffing(self.getAlt())):
			log.msg("[%s] %r is victim of keyword stuffing!!" % (self.getPipeline(), self), level=log.DEBUG, spider=self.getSpider())
			self.addReportMessage("This tag is victim of keyword stuffing!!")
	
	def checkForSuspiciousExtension(self):
		log.msg("[%s] Checking for suspicious extension..." % (self.getPipeline()), level=log.INFO, spider=self.getSpider())
		if(not self.isImage()):
			log.msg("[%s] %r reference is not an image!! that is really suspicious..." % (self.getPipeline(), self), level=log.DEBUG, spider=self.getSpider())
			self.addReportMessage("This tag is not an image!!")
	
	def checkForSuspiciousStuff(self):
		self.checkForSuspiciousExtension()	
		SizeableTag.checkForSuspiciousStuff(self)
		self.checkForKeywordStuffing()

class IframeTag(SizeableTag):
	frameborder = 99
	
	def getFrameborder(self):
		return self.frameborder

	def setFrameborder(self, frameborder):
		self.frameborder = int(frameborder)
	
	def suspiciousFrameborder(self):
		return not self.getFrameborder()  # suspicious is if frameborder is equal to zero
		
	def suspiciousSizeTagAdditions(self):
		if(self.suspiciousFrameborder()):
			self.addReportMessage("And have frameborder = 0(zero) too...thats really suspicious!")
			log.msg("[%s] %r is small and have frameborder = 0(zero)...thats really suspicious!" % (self.getPipeline(), self), level=log.DEBUG, spider=self.getSpider())
		
	def fillFromHtmlXpathSelector(self, htmlXPS):
		SizeableTag.fillFromHtmlXpathSelector(self, htmlXPS)
		frameborder = htmlXPS.select('@frameborder').extract()
		if(frameborder):
			self.setFrameborder(htmlXPS.select('@frameborder').extract()[0])
			
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
	
	def fillFromHtmlXpathSelector(self, htmlXPS):
		return self
	
	def suspiciousSize(self):
		pass
	
	def suspiciousUrl(self):
		pass
	
	def suspiciousHidden(self):
		pass

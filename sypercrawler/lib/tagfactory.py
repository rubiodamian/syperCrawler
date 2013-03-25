from sypercrawler.lib.tag import ATag, IframeTag, ImgTag, ScriptTag, NullTag
from string import capitalize


class TagFactory():

    def tag_from_str(self, nodename):
        try:
            klass = str(capitalize(str(nodename)) + 'Tag')
            return globals()[klass]()
        except Exception as e:
            print str(e)
            return NullTag()

    def tag_from_html_xpathselector(self, htmlXPS):
        nodename = htmlXPS.select('local-name()').extract()[0]
        tag = self.tag_from_str(nodename)
        tag.fill_from_html_xpathselector(htmlXPS)
        return tag

    def tags_from_html_xpathselector(self, htmlXPSs):
        tags = []
        for htmlXPS in htmlXPSs:
            tags.append(self.tag_from_html_xpathselector(htmlXPS))
        return tags

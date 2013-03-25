class ItemContext():

    def __init__(self, current_url="", spider="", pipeline=""):
        self._current_url = current_url
        self._spider = spider
        self._pipeline = pipeline

    def item_context(self, current_url="", spider="", pipeline=""):
        self.current_url = current_url
        self.spider = spider
        self.pipeline = pipeline

    @property
    def current_url(self):
        return self._current_url

    @current_url.setter
    def current_url(self, current_url):
        self._current_url = current_url

    @property
    def spider(self):
        return self._spider

    @spider.setter
    def spider(self, spider):
        self._spider = spider

    @property
    def pipeline(self):
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline):
        self._pipeline = pipeline

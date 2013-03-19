class ItemContext():

    def setItemContext(self, currentUrl="", spider="", pipeline=""):
        self.setCurrentUrl(currentUrl)
        self.setSpider(spider)
        self.setPipeline(pipeline)

    def setCurrentUrl(self, currentUrl):
        self.currentUrl = currentUrl

    def getCurrentUrl(self):
        return self.currentUrl

    def setSpider(self, spider):
        self.spider = spider

    def getSpider(self):
        return self.spider

    def setPipeline(self, pipeline):
        self.pipeline = pipeline

    def getPipeline(self):
        return self.pipeline

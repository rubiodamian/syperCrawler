# Scrapy settings for syperCrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'syperCrawler'

SPIDER_MODULES = ['sypercrawler.spiders']
NEWSPIDER_MODULE = 'sypercrawler.spiders'
ITEM_PIPELINES = [
    'sypercrawler.pipelines.FirstPipeline',
    'sypercrawler.pipelines.IframeTagPipeline',
    'sypercrawler.pipelines.ATagPipeline',
    'sypercrawler.pipelines.ImgTagPipeline',
    'sypercrawler.pipelines.ScriptTagPipeline',
    'sypercrawler.pipelines.ConsoleReportPipeline']
LOG_LEVEL = 'INFO'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'syperCrawler (+http://www.yourdomain.com)'

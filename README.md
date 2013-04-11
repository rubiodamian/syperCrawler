============
Syper Crawler
============

Install
-------

First install Scrapy:

    pip install scrapy
    
To make it work:
----------------



    scrapy crawl syperCrawler -a urls=http://localhost/test/ -a domains=localhost
    #domains = An optional list of strings containing domains that this spider is allowed to crawl
    #urls = urls from which the spider will start crawling
    
    #for multiple argumets use ",": scrapy crawl syperCrawler -a urls=http://localhost/test/,http://testdomain/test/ -a domains=localhost,testdomain
    
NOTE: If you get errors try installing:

    apt-get install libxml2-dev libxslt-dev
    apt-get install python-lxml
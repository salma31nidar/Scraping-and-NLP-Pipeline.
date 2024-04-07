from scrapy.crawler import CrawlerProcess
from aljazeera_spider.spiders.aljazeera import AljazeeraSpider

# Start the Scrapy crawler process
process = CrawlerProcess()
process.crawl(AljazeeraSpider)
process.start()

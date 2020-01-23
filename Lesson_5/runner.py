from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hh import HhSpider
from jobparser.spiders.sj import SjSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process_hh = CrawlerProcess(settings=crawler_settings)
    process_sj = CrawlerProcess(settings=crawler_settings)

    process_hh.crawl(HhSpider)
    process_sj.crawl(SjSpider)

    process_hh.start()
    process_sj.start()

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hh import HhSpider
from jobparser.spiders.sj import SjSpider


if __name__ == '__main__':

    vacancy_for_search = 'python'

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(SjSpider, vacancy_search=vacancy_for_search)
    process.crawl(HhSpider, vacancy_search=vacancy_for_search)
    process.start()

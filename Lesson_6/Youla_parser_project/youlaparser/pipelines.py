# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
from urllib.parse import urlparse
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class YoulaPhotosPipeline(ImagesPipeline):
    # def get_media_requests(self, item, info):
    #     if item['photos']:
    #         for img in item['photos']:
    #             try:
    #                 yield scrapy.Request(img)
    #             except Exception as e:
    #                 print(e)

    # def file_path(self, request, response, info):
    #     return 'files/' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        print(item)
        # if results:
        #     item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.youla

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.start_urls[0].split('/')[-1]]
        collection.insert_one(item)
        return item

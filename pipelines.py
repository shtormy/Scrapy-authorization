# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pymongo import MongoClient
from pymongo import errors



class ParseGbPipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongodb = client.geekbrains

    def process_item(self, item, spider):
        collection = self.mongodb[spider.name]
        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            pass
        return item

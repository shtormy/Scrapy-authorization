# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


class ParseGbItem(scrapy.Item):

    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    level = scrapy.Field(output_processor=TakeFirst())
    learning_lines = scrapy.Field(output_processor=TakeFirst())
    price_per_month = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field(output_processor=TakeFirst())


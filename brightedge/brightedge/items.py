# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BrightedgespiderItem(scrapy.Item):
    # Define the fields for your item here like:
    url = scrapy.Field()
    tokens = scrapy.Field()
    topics = scrapy.Field()
    failure_reason = scrapy.Field()

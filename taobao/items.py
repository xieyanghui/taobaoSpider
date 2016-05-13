# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy

class TaobaoItem(scrapy.Item):
    name = scrapy.Field();
    keywords = scrapy.Field();
    gid = scrapy.Field();
    description = scrapy.Field();
    price_attr = scrapy.Field();
    price_value = scrapy.Field();
    attr = scrapy.Field();
    text = scrapy.Field();
    img = scrapy.Field();


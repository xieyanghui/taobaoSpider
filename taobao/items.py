# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field

class TaobaoItem(Item):
	name = Field();
	keywords = Field();
	temp = Field();
	description = Field();
	price_attr = Field();
	price_value = Field();
	attr = Field();
	text = Field();
	img = Field();


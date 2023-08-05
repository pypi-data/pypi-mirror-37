# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
from dateutil.parser import parse
import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity
from scrapy.loader.processors import Compose, SelectJmes, MergeDict
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class CrawledItem(scrapy.Item):
    url = scrapy.Field()


class ScrapItem(scrapy.Item):
    url = scrapy.Field()



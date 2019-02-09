# -*- coding: utf-8 -*-
import scrapy
# ------------------------------------
# date 反映时间
# _content 来信内容
# ans_date 答复时间
# source 信件来源
# depaertment 答复单位
# ans_content 答复内容
# aera 问题属地
# url 网页
# ------------------------------------
class QuotesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # title= scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    _content = scrapy.Field()
    aera = scrapy.Field()
    source = scrapy.Field()
    department = scrapy.Field()
    ans_date = scrapy.Field()
    ans_content = scrapy.Field()
    # result = scrapy.Field()


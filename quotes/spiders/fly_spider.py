# -*- coding: utf-8 -*-
import scrapy
import time
import sys
import os
# 代码进行迁移可能报错点
# ------------------------
sys.path.append(os.getcwd()+r'\quotes')
# ------------------------
from items import QuotesItem
class FlySpider(scrapy.Spider):
    name = "fly"
    allowed_domains = ["www.zjzxts.gov.cn"]
    start_urls = ["http://www.zjzxts.gov.cn/sun/satisfaction?page=xjgk&gkbz=1&areacode=330109&index=0&bt="]

    def parse(self, response):
        # 解析数据
        Source = response.css(".tablelist1 td")
        message = Source.css("::text").extract()
        message2 = Source.css("::attr(onclick)").extract()
        message3 = response.css('#content .default::text').extract()
        temp = message3.copy()
        for i in temp:
            if '--' in i:
                message3.remove(i)
        message3.insert(0, '浙江省 ')
        message3 = ''.join(message3)
        time.sleep(0.1)
        # 1 获取日期和title
        # 1 _title = []
        # 1 for i in message[0::3]:
        # 1   _title.append(i)
        # 访问二级页面
        for index,value in enumerate(message2):
            item = QuotesItem()
            # 1 item['title'] = _title[index]
            # item['aera'] = message3
            # item['_url'] = 'http://www.zjzxts.gov.cn/wsdt/wsdtHtml/xfjxq.jsp?id='+ value[6:-2]
            url = 'http://www.zjzxts.gov.cn/wsdt/wsdtHtml/xfjxq.jsp?id='+ value[6:-2]
            time.sleep(0.1)
            yield scrapy.Request(url,meta={'item':item,'Aera':message3,'Url':url},callback=self.detail_parse2)
        current_page = response.css('#content .paginList #cp::text').extract()
        current_page = str(int(current_page[0]))
        if(current_page!='10'):
            one_url = response.css('#content .paginList a::attr(href)').extract_first()
            next_url = 'http://www.zjzxts.gov.cn'+one_url[:-5]+current_page+'&bt='
            time.sleep(1)
            yield scrapy.Request(url=next_url,callback = self.parse)

    def detail_parse2(self,response):
        # 接受上级已爬取的数据
        item = response.meta['item']
        source = response.css('.blue1::text').extract()
        # 二级页数据提取
        item = QuotesItem()
        item['url'] = response.meta['Url']
        item['date'] = source[1]
        item['aera'] = response.meta['Aera']
        item['source'] = source[2]
        item['_content'] = source[0]
        item['department'] = source[3]
        item['ans_date'] = source[4]
        item['ans_content'] = source[5]
        return item
        # 返回给爬虫引擎
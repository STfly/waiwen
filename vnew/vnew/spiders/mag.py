# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import VnewItem
import time
i = 0
class MagSpider(CrawlSpider):
    name = 'mag'
    allowed_domains = ['sciencemag.org']
    # start_urls = ['https://www.sciencemag.org/']
    # start_urls = ['https://www.sciencemag.org/careers/2016/09/how-review-paper']
    start_urls = ['https://www.sciencemag.org/news/latest-news']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.sciencemag.org/news/\d+/\d+/.*?'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'https://www.sciencemag.org/careers/\d+/\d+/.*?'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        global i
        i = i + 1
        print(str(i) + '++++++++++' + response.url)
        item = VnewItem()
        item['title'] = response.xpath('//*[@id="main-content"]/div/div/article//h1[@class="article__headline"]/text()').get()
        item['author'] = response.xpath('//*[@id="main-content"]/div/div/article//p[@class="byline byline--article"]/a/text()').get()
        item['time'] = response.xpath('//*[@id="main-content"]/div/div/article//p[@class="byline byline--article"]/time/text()').get()
        # item['content'] = response.xpath('string(//article/div[@class="article__body"]//*)').extract()
        # 解决标题标签，和尾部签署名的问题,只能取p和好标签
        item['content'] = response.xpath(
            '//article/div[@class="article__body"]/p//text() | //article/div[@class="article__body"]/h2//text()'
        ).extract()
        item['posted'] = response.xpath('//article/footer/div[@class="meta-line"]/ul//li/a/text()').extract()
        print(item['title'])
        # print(item['author'])
        # print(item['time'])
        # print(item['content'])
        print(item['posted'])
        # time.sleep(10)
        return item


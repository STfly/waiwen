# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random, base64
import scrapy
from vnew.settings import USER_AGENT_LIST
from vnew.settings import PROXY_LIST


class VnewSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class VnewDownloaderMiddleware2(object):

    def __init__(self):
        self.user_agent_list = USER_AGENT_LIST

    def process_request(self, request, spider):
        # 更换代理ip
        proxy = random.choice(PROXY_LIST)
        # 代理有密码的认证
        if 'user_passwd' in proxy:
            # 对帐号密码进行加密设置编码
            b64_up = base64.b64encode(proxy['user_passwd'].encode())
            # 设置认证
            request.headers['Proxy-Authorization'] = 'Basic' + b64_up.decode()
            # 设置代理
            request.meta['proxy'] = proxy['ip_port']
        else:
            request.meta['proxy'] = proxy['ip_port']
        # 更换UA
        ua = random.choice(self.user_agent_list)
        if ua:
            # 如果 key 存在, 直接覆盖
            request.headers['User-Agent'] = ua
            # request.headers.setdefault(b'User-Agent', ua)
        # 问题就在 request.headers.setdefault() 方法中 . setdefault 方法意味着 :
        # 如果键不存在于字典中，将会添加键并将值设为默认值。如果存在,则不添加 。
        return None
    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


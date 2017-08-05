#!/usr/bin/python
#coding=utf-8
# @hequan


import scrapy

from scrapy.spiders import Spider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import re
from scrapy.spiders import CrawlSpider

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from spider_scrapy_lianjia.items import SpiderDianpingXmtItem

class dianping_xmt_baby_spider(CrawlSpider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫中你必须定义不同的名字
    name = "dianping_xmt_baby_spider"    # 设置爬虫名称

    # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    allowed_domains = ["dianping.com"] # 设置允许的域名

    # 爬取的url列表，爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始，其他子url将会从这些起始url中继承性生成
    start_urls = [

        # 托班/托儿所
	'http://www.dianping.com/search/category/15/70/g33800', # 寒暑托
	'http://www.dianping.com/search/category/15/70/g33801', # 双语托班
	'http://www.dianping.com/search/category/15/70/g33802', # 晚托

        # 婴儿游泳
	'http://www.dianping.com/search/category/15/70/g27767', # 婴儿游泳

        # 亲子游乐
	'http://www.dianping.com/search/category/15/70/g27760', # 亲子乐园
	'http://www.dianping.com/search/category/15/70/g33775', # 儿童主题乐园
	'http://www.dianping.com/search/category/15/70/g33776', # 运动探险
	'http://www.dianping.com/search/category/15/70/g33777', # 角色扮演

        # 亲子旅游
	'http://www.dianping.com/search/category/15/70/g33808', # 亲子旅游
        # 其他亲子服务
	'http://www.dianping.com/search/category/15/70/g33810', # 其他亲子服务
	'http://www.dianping.com/search/category/15/70/g2833', # 婴儿理发

        # 幼儿教育
	'http://www.dianping.com/search/category/15/70/g33778', # 综合教育
	'http://www.dianping.com/search/category/15/70/g33779', # 幼升小辅导
	'http://www.dianping.com/search/category/15/70/g33856', # 教育机器人
	'http://www.dianping.com/search/category/15/70/g2995', # 乐高

        # 幼儿园
	'http://www.dianping.com/search/category/15/70/g27770', # 公办幼儿园
	'http://www.dianping.com/search/category/15/70/g27771', # 民办幼儿园
	'http://www.dianping.com/search/category/15/70/g27772', # 示范/一级园 
	'http://www.dianping.com/search/category/15/70/g27773', # 双语幼儿园
	'http://www.dianping.com/search/category/15/70/g27774', # 寄宿幼儿园

        # 幼儿才艺
	'http://www.dianping.com/search/category/15/70/g33786', # 乐器演奏
	'http://www.dianping.com/search/category/15/70/g33787', # 钢琴培训
	'http://www.dianping.com/search/category/15/70/g33788', # 围棋
	'http://www.dianping.com/search/category/15/70/g33789', # 少儿跆拳道
	'http://www.dianping.com/search/category/15/70/g33790', # 主持表演
	'http://www.dianping.com/search/category/15/70/g33791', # 珠心算
	'http://www.dianping.com/search/category/15/70/g2982', # 少儿美术
	'http://www.dianping.com/search/category/15/70/g2984', # 国学
	'http://www.dianping.com/search/category/15/70/g2988', # 综合才艺
	'http://www.dianping.com/search/category/15/70/g2992', # 少儿舞蹈
	'http://www.dianping.com/search/category/15/70/g2994', # 少儿运动

        # 幼儿外语
	'http://www.dianping.com/search/category/15/70/g33780', # 兴趣英语
	'http://www.dianping.com/search/category/15/70/g33781', # 学科英语
	'http://www.dianping.com/search/category/15/70/g33782', # 美式英语
	'http://www.dianping.com/search/category/15/70/g33783', # 应试英语
	'http://www.dianping.com/search/category/15/70/g33784', # 国际英语
	'http://www.dianping.com/search/category/15/70/g33785', # 绘本阅读

        # 早教中心
	'http://www.dianping.com/search/category/15/70/g33768', # 亲子游泳
	'http://www.dianping.com/search/category/15/70/g33769', # 蒙氏教育
	'http://www.dianping.com/search/category/15/70/g33770', # 大脑开发
	'http://www.dianping.com/search/category/15/70/g33771', # 情商培养
	'http://www.dianping.com/search/category/15/70/g33772', # 感觉统合
	'http://www.dianping.com/search/category/15/70/g33773', # 艺术启蒙
	'http://www.dianping.com/search/category/15/70/g33774', # 思维训练


    ]

    shop_type_map = {
        # 早教中心
        'http://www.dianping.com/search/category/15/70/g33768' : {'city_id' : '0592', 'shop_type' : 10001},
        'http://www.dianping.com/search/category/15/70/g33769' : {'city_id' : '0592', 'shop_type' : 10002},
        'http://www.dianping.com/search/category/15/70/g33770' : {'city_id' : '0592', 'shop_type' : 10003},
        'http://www.dianping.com/search/category/15/70/g33771' : {'city_id' : '0592', 'shop_type' : 10004},
        'http://www.dianping.com/search/category/15/70/g33772' : {'city_id' : '0592', 'shop_type' : 10005},
        'http://www.dianping.com/search/category/15/70/g33773' : {'city_id' : '0592', 'shop_type' : 10006},
        'http://www.dianping.com/search/category/15/70/g33774' : {'city_id' : '0592', 'shop_type' : 10007},

        # 幼儿外语
        'http://www.dianping.com/search/category/15/70/g33780' : {'city_id' : '0592', 'shop_type' : 20001},
        'http://www.dianping.com/search/category/15/70/g33781' : {'city_id' : '0592', 'shop_type' : 20002},
        'http://www.dianping.com/search/category/15/70/g33782' : {'city_id' : '0592', 'shop_type' : 20003},
        'http://www.dianping.com/search/category/15/70/g33783' : {'city_id' : '0592', 'shop_type' : 20004},
        'http://www.dianping.com/search/category/15/70/g33784' : {'city_id' : '0592', 'shop_type' : 20005},
        'http://www.dianping.com/search/category/15/70/g33785' : {'city_id' : '0592', 'shop_type' : 20006},

        # 幼儿才艺
        'http://www.dianping.com/search/category/15/70/g33786' : {'city_id' : '0592', 'shop_type' : 30001},
        'http://www.dianping.com/search/category/15/70/g33787' : {'city_id' : '0592', 'shop_type' : 30002},
        'http://www.dianping.com/search/category/15/70/g33788' : {'city_id' : '0592', 'shop_type' : 30003},
        'http://www.dianping.com/search/category/15/70/g33789' : {'city_id' : '0592', 'shop_type' : 30004},
        'http://www.dianping.com/search/category/15/70/g33790' : {'city_id' : '0592', 'shop_type' : 30005},
        'http://www.dianping.com/search/category/15/70/g33791' : {'city_id' : '0592', 'shop_type' : 30006},
        'http://www.dianping.com/search/category/15/70/g2982'  : {'city_id' : '0592', 'shop_type' : 30007},
        'http://www.dianping.com/search/category/15/70/g2984'  : {'city_id' : '0592', 'shop_type' : 30008},
        'http://www.dianping.com/search/category/15/70/g2988'  : {'city_id' : '0592', 'shop_type' : 30009},
        'http://www.dianping.com/search/category/15/70/g2992'  : {'city_id' : '0592', 'shop_type' : 30010},
        'http://www.dianping.com/search/category/15/70/g2994'  : {'city_id' : '0592', 'shop_type' : 30011},
        # 幼儿教育
        'http://www.dianping.com/search/category/15/70/g33778' : {'city_id' : '0592', 'shop_type' : 100001},
        'http://www.dianping.com/search/category/15/70/g33779' : {'city_id' : '0592', 'shop_type' : 100002},
        'http://www.dianping.com/search/category/15/70/g33856' : {'city_id' : '0592', 'shop_type' : 100003},
        'http://www.dianping.com/search/category/15/70/g2995'  : {'city_id' : '0592', 'shop_type' : 100004},
        # 其他亲子服务
        'http://www.dianping.com/search/category/15/70/g33810' : {'city_id' : '0592', 'shop_type' : 90001},
        'http://www.dianping.com/search/category/15/70/g2833'  : {'city_id' : '0592', 'shop_type' : 90002},
        # 亲子旅游
        'http://www.dianping.com/search/category/15/70/g33808' : {'city_id' : '0592', 'shop_type' : 80001},
        # 亲子游乐
        'http://www.dianping.com/search/category/15/70/g27760' : {'city_id' : '0592', 'shop_type' : 70001},
        'http://www.dianping.com/search/category/15/70/g33775' : {'city_id' : '0592', 'shop_type' : 70002},
        'http://www.dianping.com/search/category/15/70/g33776' : {'city_id' : '0592', 'shop_type' : 70003},
        'http://www.dianping.com/search/category/15/70/g33777' : {'city_id' : '0592', 'shop_type' : 70004},

        # 婴儿游泳
        'http://www.dianping.com/search/category/15/70/g27767' : {'city_id' : '0592', 'shop_type' : 60001},

        # 托班/托儿所
        'http://www.dianping.com/search/category/15/70/g33800' : {'city_id' : '0592', 'shop_type' : 50001},
        'http://www.dianping.com/search/category/15/70/g33801' : {'city_id' : '0592', 'shop_type' : 50002},
        'http://www.dianping.com/search/category/15/70/g33802' : {'city_id' : '0592', 'shop_type' : 50003},
        # 幼儿园
        'http://www.dianping.com/search/category/15/70/g27770' : {'city_id' : '0592', 'shop_type' : 40001},
        'http://www.dianping.com/search/category/15/70/g27771' : {'city_id' : '0592', 'shop_type' : 40002},
        'http://www.dianping.com/search/category/15/70/g27772' : {'city_id' : '0592', 'shop_type' : 40003},
        'http://www.dianping.com/search/category/15/70/g27773' : {'city_id' : '0592', 'shop_type' : 40004},
        'http://www.dianping.com/search/category/15/70/g27774' : {'city_id' : '0592', 'shop_type' : 40005},


    }


    def parse(self, response):
        sel = Selector(response)
        if response.meta.has_key("shop_type"):
            shop_type = response.meta['shop_type']
        else:
            shop_type = self.shop_type_map[response.url]['shop_type']

        if response.meta.has_key("city_id"):
            city_id = response.meta['city_id']
        else:
            city_id = self.shop_type_map[response.url]['city_id']

        cat_url = response.url
        http_status = response.status
        self.log("http_url = %s" % cat_url)
        self.log("http_status = %s proxy = %s" % (http_status, response.meta['proxy']))

        self.log("shop_type = %s" % shop_type)
        items = []
        shop_list = sel.xpath('//li[@class="t-item-box t-district J_li"]/div[@class="t-item"]/div[@class="t-list"]/ul/li')
	self.log("shop_list_len = %d" % len(shop_list))
        for shop in shop_list:
            uri = shop.xpath('a/@href').extract()[0]
            self.log("page_uri = %s" % uri)
            yield scrapy.Request('http://www.dianping.com' + uri, callback=self.parse_list, meta={'shop_type':shop_type, 'cat_url' : cat_url, 'city_id' : city_id})

    def parse_list(self, response):
        sel = Selector(response)

        shop_type = response.meta['shop_type']
        cat_url = response.meta['cat_url']
        city_id = response.meta['city_id']

        http_status = response.status
        self.log("http_status = %s proxy = %s" % (http_status, response.meta['proxy']))

        self.log("shop_type = %s" % shop_type)
        items = []
        shop_list = sel.xpath('//ul[@class="shop-list"]/li')
        for shop in shop_list:
            uri = shop.xpath('div/p/a[@class="shopname"]/@href').extract()[0]
            self.log("shop_uri = %s" % uri)
            yield scrapy.Request('http://www.dianping.com' + uri, callback=self.parse_content, meta={'shop_type':shop_type, 'cat_url' : cat_url, 'city_id' : city_id})

        ### 是否还有下一页，如果有，则继续
        next_page = sel.xpath('//a[@class="NextPage"]')
        if len(next_page) <= 0:
            return

        next_page = sel.xpath('//a[@class="NextPage"]/@href').extract()[0].strip()
        self.log("next_page = %s" % next_page)
        if next_page:
            self.log("next_page_uri = %s" % next_page)
            yield scrapy.Request('http://www.dianping.com' + next_page, callback=self.parse_list, meta={'shop_type' : shop_type, 'cat_url' : cat_url,  'city_id' : city_id})

    # 解析的方法，调用的时候传入从每一个url传回的response对象作为唯一参数，负责解析并获取抓取的数据(解析为item)，跟踪更多的url
    def parse_content(self, response):
        self.log("=================================================")
        self.log("cat_url = %s proxy = %s" % (response.meta['cat_url'], response.meta['proxy']))
        chenshi_name= response.meta['city_id']
        sel = Selector(response)

        item = SpiderDianpingXmtItem()

        shop_type   = response.meta['shop_type']
        shop_url    = response.url
        http_status = response.status

        self.log("shop_url = %s" % shop_url)
        self.log("shop_type = %s" % shop_type)
        self.log("http_status = %s" % http_status)

	x = sel.xpath('//div[@class="block shop-info"]')
        if len(x) > 0:
            shop_name   = sel.xpath('//div[@class="block shop-info"]/div/div[@class="shop-name"]/h1[@class="shop-title"]/text()').extract()[0].strip()

            shop_addr   = x[0].xpath('div/div[@class="desc-list"]/dl[@class="shopDeal-Info-address"]/dd[@class="shop-info-content"]/span[@itemprop="street-address"]/text()').extract()[0].strip()

            # shop_mobile
            x2 = x[0].xpath('div/div[@class="desc-list"]/dl/dd[@class="shop-info-content"]/a[@id="J-showPhoneNumber"]')
            if len(x2) > 0:
                shop_mobile = x2[0].xpath('@data-real').extract()[0].strip()
            else:
                shop_mobile = ""

            # shop_intro
            shop_intro  = ""
        else:
            shop_name   = sel.xpath('//div[@class="shop-info"]/div[@class="shop-name"]/h1[@class="shop-title"]/text()').extract()[0].strip()
            shop_addr   = sel.xpath('//div[@class="shop-info"]/div[@class="shop-addr"]/span/@title').extract()[0].strip()

            # shop_mobile
            x = sel.xpath('//div[@class="shop-info"]/div[@class="shopinfor"]/p/span')
            if len(x) == 0:
                shop_mobile = ""
            else:
                shop_mobile = x[0].xpath('text()').extract()[0].strip()

            # shop_intro 
            x = sel.xpath('//div[@class="block_all"]/div[@class="block_right"]/span')
            if len(x) < 2:
                shop_intro=""
            else:
                shop_intro = x[0].xpath('text()').extract()[0].strip()


        self.log("shop_name = %s" % shop_name)

        self.log("shop_addr = %s" % shop_addr)


        self.log("shop_mobile = %s" % shop_mobile)


        self.log("shop_intro = %s" % shop_intro)

        item['chenshi_name']    = chenshi_name
        item['shop_type']       = shop_type
        item['shop_url']        = shop_url
        item['shop_name']       = shop_name
        item['shop_addr']       = shop_addr
        item['shop_mobile']     = shop_mobile
        item['shop_intro']      = shop_intro

        return item



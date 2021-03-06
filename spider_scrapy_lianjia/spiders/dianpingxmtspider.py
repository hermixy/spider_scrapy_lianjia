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

class dianping_xmt_spider(CrawlSpider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫中你必须定义不同的名字
    name = "dianping_xmt_spider"    # 设置爬虫名称

    # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    allowed_domains = ["dianping.com"] # 设置允许的域名

    # 爬取的url列表，爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始，其他子url将会从这些起始url中继承性生成
    start_urls = [
        # 外语培训
        # 上海
        'http://www.dianping.com/search/category/1/75/g3030',
        'http://www.dianping.com/search/category/1/75/g3032',
        'http://www.dianping.com/search/category/1/75/g3034',
        'http://www.dianping.com/search/category/1/75/g3039',
        'http://www.dianping.com/search/category/1/75/g3036',
        'http://www.dianping.com/search/category/1/75/g3038',
        'http://www.dianping.com/search/category/1/75/g33816',
        'http://www.dianping.com/search/category/1/75/g3040',

        # 音乐培训
        # 上海
        'http://www.dianping.com/search/category/1/75/g3041', # 钢琴
        'http://www.dianping.com/search/category/1/75/g3042', # 吉他
        'http://www.dianping.com/search/category/1/75/g3044', # 古筝
        'http://www.dianping.com/search/category/1/75/g3046', # 架子鼓
        'http://www.dianping.com/search/category/1/75/g3048', # 声乐
        'http://www.dianping.com/search/category/1/75/g3043', # 小提琴
        'http://www.dianping.com/search/category/1/75/g3050', # 其他音乐培训

        # 职业技术
        # 上海
        'http://www.dianping.com/search/category/1/75/g3057', # 美容美妆
        'http://www.dianping.com/search/category/1/75/g3059', # IT
        'http://www.dianping.com/search/category/1/75/g3058', # 会计
        'http://www.dianping.com/search/category/1/75/g3060', # 厨艺
        'http://www.dianping.com/search/category/1/75/g33812', # 管理培训
        'http://www.dianping.com/search/category/1/75/g33814', # 摄影培训
        'http://www.dianping.com/search/category/1/75/g33829', # 公务员培训
        'http://www.dianping.com/search/category/1/75/g3062', # 其他职业培训

        # 升学辅导
        # 上海
        'http://www.dianping.com/search/category/1/75/g3052', # 小学辅导
        'http://www.dianping.com/search/category/1/75/g3054', # 中学辅导
        'http://www.dianping.com/search/category/1/75/g3055', # 高中辅导
        'http://www.dianping.com/search/category/1/75/g33817', # 专升本/自考
        'http://www.dianping.com/search/category/1/75/g33828', # 自考
        'http://www.dianping.com/search/category/1/75/g33813', # 考研
        'http://www.dianping.com/search/category/1/75/g3056', # 其他升学辅导

        # 美术培训
        # 上海
        'http://www.dianping.com/search/category/1/75/g33756', # 绘画
        'http://www.dianping.com/search/category/1/75/g33757', # 书法
        'http://www.dianping.com/search/category/1/75/g33758', # 其他美术培训

        # 兴趣生活
        # 上海
        'http://www.dianping.com/search/category/1/75/g33900', # 棋牌培训
        'http://www.dianping.com/search/category/1/75/g33897', # 烘焙培训
        'http://www.dianping.com/search/category/1/75/g33898', # 插花培训
        'http://www.dianping.com/search/category/1/75/g33899', # 手工培训
        'http://www.dianping.com/search/category/1/75/g33901', # 其他兴趣生活

        # 留学
        # 上海
        'http://www.dianping.com/search/category/1/75/g33945', # 留学申请
        'http://www.dianping.com/search/category/1/75/g33946', # 雅思托福
        'http://www.dianping.com/search/category/1/75/g33947', # 其他留学服务
        # 更多教育培训
        # 上海
        'http://www.dianping.com/search/category/1/75/g2882', # 更多教育培训
        
    ]

    # 外语培训
    # 1001 英语 1002 日语 1004 韩语 1009 汉语 1006 法语 1008 德语 1007 西班牙语 1100 其他

    # 音乐培训
    # 2001 钢琴 2002 吉他 2003 古筝 2004 架子鼓 2005 声乐 2006 小提琴 2100 其他音乐培训

    # 职业技术
    # 3001 美容美妆 3002 IT 3003 会计 3004 厨艺 3005 管理培训 3006 摄影培训 3007 公务员培训 3100 其他职业培训

    # 升学辅导
    # 4001 小学辅导 4002 初中辅导 4003 高中辅导 4004 专升本/自考 4005 艺考 4006 考研 4100 其他升学辅导

    # 美术培训
    # 5001 绘画 5002 书法 5100 其他美术培训

    # 兴趣生活
    # 6001 棋牌培训 6002 烘焙培训 6003 插花培训 6004 手工培训 6100 其他兴趣生活

    # 留学
    # 7001 留学申请 7002 雅思托福 7100 其他留学服务

    # 更多教育培训
    # 8100


    # 城市
    # 021 上海 010 北京 028 成都
    shop_type_map = {
        # 更多教育培训
        # 上海
        'http://www.dianping.com/search/category/1/75/g2882' : {'city_id' : '021', 'shop_type' : 8100},

        # 留学
        # 上海
        'http://www.dianping.com/search/category/1/75/g33945' : {'city_id' : '021', 'shop_type' : 7001},
        'http://www.dianping.com/search/category/1/75/g33946' : {'city_id' : '021', 'shop_type' : 7002},
        'http://www.dianping.com/search/category/1/75/g33947' : {'city_id' : '021', 'shop_type' : 7100},
        # 兴趣生活
        # 上海
        'http://www.dianping.com/search/category/1/75/g33900' : {'city_id' : '021', 'shop_type' : 6001},
        'http://www.dianping.com/search/category/1/75/g33897' : {'city_id' : '021', 'shop_type' : 6002},
        'http://www.dianping.com/search/category/1/75/g33898' : {'city_id' : '021', 'shop_type' : 6003},
        'http://www.dianping.com/search/category/1/75/g33899' : {'city_id' : '021', 'shop_type' : 6004},
        'http://www.dianping.com/search/category/1/75/g33901' : {'city_id' : '021', 'shop_type' : 6100},
        # 美术培训
        # 上海
        'http://www.dianping.com/search/category/1/75/g33756' : {'city_id' : '021', 'shop_type' : 5001},
        'http://www.dianping.com/search/category/1/75/g33757' : {'city_id' : '021', 'shop_type' : 5002},
        'http://www.dianping.com/search/category/1/75/g33758' : {'city_id' : '021', 'shop_type' : 5100},
        # 外语培训
        # 上海
        'http://www.dianping.com/search/category/1/75/g3030' : {'city_id' : '021', 'shop_type' : 1001},
        'http://www.dianping.com/search/category/1/75/g3032' : {'city_id' : '021', 'shop_type' : 1002},
        'http://www.dianping.com/search/category/1/75/g3034' : {'city_id' : '021', 'shop_type' : 1004},
        'http://www.dianping.com/search/category/1/75/g3039' : {'city_id' : '021', 'shop_type' : 1009},
        'http://www.dianping.com/search/category/1/75/g3036' : {'city_id' : '021', 'shop_type' : 1006},
        'http://www.dianping.com/search/category/1/75/g3038' : {'city_id' : '021', 'shop_type' : 1008},
        'http://www.dianping.com/search/category/1/75/g33816' : {'city_id' : '021', 'shop_type' : 1007},
        'http://www.dianping.com/search/category/1/75/g3040' : {'city_id' : '021', 'shop_type' : 1100},

        # 音乐培训
        # 上海
        'http://www.dianping.com/search/category/1/75/g3041' : {'city_id' : '021', 'shop_type' : 2001},
        'http://www.dianping.com/search/category/1/75/g3042' : {'city_id' : '021', 'shop_type' : 2002},
        'http://www.dianping.com/search/category/1/75/g3044' : {'city_id' : '021', 'shop_type' : 2003},
        'http://www.dianping.com/search/category/1/75/g3046' : {'city_id' : '021', 'shop_type' : 2004},
        'http://www.dianping.com/search/category/1/75/g3048' : {'city_id' : '021', 'shop_type' : 2005},
        'http://www.dianping.com/search/category/1/75/g3043' : {'city_id' : '021', 'shop_type' : 2006},
        'http://www.dianping.com/search/category/1/75/g3050' : {'city_id' : '021', 'shop_type' : 2100},

        # 职业技术
        # 上海
        'http://www.dianping.com/search/category/1/75/g3057' : {'city_id' : '021', 'shop_type' : 3001},
        'http://www.dianping.com/search/category/1/75/g3059' : {'city_id' : '021', 'shop_type' : 3002},
        'http://www.dianping.com/search/category/1/75/g3058' : {'city_id' : '021', 'shop_type' : 3003},
        'http://www.dianping.com/search/category/1/75/g3060' : {'city_id' : '021', 'shop_type' : 3004},
        'http://www.dianping.com/search/category/1/75/g33812' : {'city_id' : '021', 'shop_type' : 3005},
        'http://www.dianping.com/search/category/1/75/g33814' : {'city_id' : '021', 'shop_type' : 3006},
        'http://www.dianping.com/search/category/1/75/g33829' : {'city_id' : '021', 'shop_type' : 3007},
        'http://www.dianping.com/search/category/1/75/g3062' : {'city_id' : '021', 'shop_type' : 3100},

        # 升学辅导
        # 上海
        'http://www.dianping.com/search/category/1/75/g3052' : {'city_id' : '021', 'shop_type' : 4001},
        'http://www.dianping.com/search/category/1/75/g3054' : {'city_id' : '021', 'shop_type' : 4002},
        'http://www.dianping.com/search/category/1/75/g3055' : {'city_id' : '021', 'shop_type' : 4003},
        'http://www.dianping.com/search/category/1/75/g33817' : {'city_id' : '021', 'shop_type' : 4004},
        'http://www.dianping.com/search/category/1/75/g33828' : {'city_id' : '021', 'shop_type' : 4005},
        'http://www.dianping.com/search/category/1/75/g33813' : {'city_id' : '021', 'shop_type' : 4006},
        'http://www.dianping.com/search/category/1/75/g3056' : {'city_id' : '021', 'shop_type' : 4100},
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
        self.log("http_status = %s proxy = %s" % (http_status, response.meta['proxy']))

        self.log("shop_type = %s" % shop_type)
        items = []
        shop_list = sel.xpath('//div[@id="region-nav"]/a')
        for shop in shop_list:
            uri = shop.xpath('@href').extract()[0]
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
        shop_list = sel.xpath('//div[@class="txt"]/div[@class="tit"]/a[@data-hippo-type="shop"]')
        for shop in shop_list:
            uri = shop.xpath('@href').extract()[0]
            self.log("shop_uri = %s" % uri)
            yield scrapy.Request('http://www.dianping.com' + uri, callback=self.parse_content, meta={'shop_type':shop_type, 'cat_url' : cat_url, 'city_id' : city_id})

        ### 是否还有下一页，如果有，则继续
        next_page = sel.xpath('//a[@class="next"]')
        if len(next_page) <= 0:
            return

        next_page = sel.xpath('//a[@class="next"]/@href').extract()[0].strip()
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

        shop_name   = sel.xpath('//div[@class="shop-name"]/h1/text()').extract()[0].strip()
        self.log("shop_name = %s" % shop_name)

        shop_addr   = sel.xpath('//div[@class="address"]/text()').extract()[1].strip()
        self.log("shop_addr = %s" % shop_addr)

        x = sel.xpath('//div[@class="phone"]/span')
        if len(x) == 0:
            shop_mobile=""
        else:
            shop_mobile = x[0].xpath('@data-phone').extract()[0]

        self.log("shop_mobile = %s" % shop_mobile)

        x = sel.xpath('//div[@class="mod shop-info"]/ul/li')
        if len(x) < 2:
            shop_intro=""
        else:
            shop_intro = x[1].xpath('text()').extract()[1].strip()

        self.log("shop_intro = %s" % shop_intro)

        item['chenshi_name']    = chenshi_name
        item['shop_type']       = shop_type
        item['shop_url']        = shop_url
        item['shop_name']       = shop_name
        item['shop_addr']       = shop_addr
        item['shop_mobile']     = shop_mobile
        item['shop_intro']      = shop_intro

        return item



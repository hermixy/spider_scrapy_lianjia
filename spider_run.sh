#!/bin/bash

workdir=/root/hequan/spider_scrapy_lianjia/spider_scrapy_lianjia
cd ${workdir}
/usr/bin/python /usr/local/bin/scrapy crawl lianjia_house_spider
/usr/bin/python /usr/local/bin/scrapy crawl chenshi_count_spider


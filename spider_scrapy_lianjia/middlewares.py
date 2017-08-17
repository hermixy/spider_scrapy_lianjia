#!/usr/bin/python
#coding=utf-8

import random
import base64
import requests
import simplejson
import redis

from settings import PROXIES
from time import ctime,sleep

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        r=redis.Redis(host='127.0.0.1',port=6379,db=1)
        ip_json = r.get("ip_list")
        ip_list = simplejson.loads(ip_json)
        while True:
            ip_info = random.choice(ip_list)
            if ip_info['ip:port'].find("127.0.0.1") == -1:
                break

        proxy = ip_info['ip:port']
        print "proxy_server = %s" % (proxy)
        request.meta['proxy'] = "http://%s" % proxy
        return 

        request.meta['proxy'] = "http://%s" % proxy
        # 添加账号密码，如果不用账号密码，则下面的代码删除即可
        proxy_user_pass = "hequan:2mjhm256"
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

        return

        proxy = random.choice(PROXIES)
        request.meta['proxy'] = "http://%s" % proxy
        return

        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

        return




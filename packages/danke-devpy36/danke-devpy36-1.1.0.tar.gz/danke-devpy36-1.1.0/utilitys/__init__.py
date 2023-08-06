# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 下午4:52
# @Author  : Shark
# @File    : __init__.py.py
import re

import logging
import time
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)

'''
清洗规则
'''
class Factory(object):

    def merge_str(self,params,result):
        """
        用于合并字符串
        """
        result_list = result.split(";")[:-1]
        merge_result = ""
        for result in result_list:
            merge_result += params[0] + result + params[1]
        return merge_result

    def sub_ascill(self,params,result):
        """
        用于替换字符
        """
        result = re.sub(params[0],params[1],result)
        return result

    def sub_str(self, params, result):
        result_str = ''
        for i in range(len(params)):
            re_expression = re.compile(params[i])
            # if params[1] == :
            re_result = re.search(re_expression, result).group(1)
            result_str += re_result
        return result_str

    def sub_all(self, params, result):
        result_str = ""
        for i in range(len(params)):
            re_expression = re.compile(params[i])
            # if params[1] == :
            re_result = re.findall(re_expression, result)
            re_result = ",".join(re_result)
            result_str += re_result
        return result_str



    # def sub_str(self, params, result):
    #     # 对模板中传入的参数进行判断r
    #     start = params[0]
    #     end = params[1]
    #     if isinstance(params[0], int):
    #         start = params[0]
    #     else:
    #         start = result.find(params[0])
    #
    #     if isinstance(params[1], int):
    #         end = params[1]
    #     else:
    #         end = result.find(params[1])
    #
    #     if end > len(result):
    #         end = len(result)
    #     final_str = result[start:end]
    #     return final_str

    def adds_str(self, params, result):
        i = 0
        if isinstance(params[1], int):
            i = params[1]
        else:
            i = result.find(params[1])
        url = result[0:i] + params[0] + result[i:]
        return url

    def split_str(self, params, result):
        str_list = result.split(params[0])
        item_str = str_list[params[1]]
        return item_str

    def join_str(self, params, result):
        return params[0].join(result)

    def replace_str(self, params, result):
        pass

    def clean_str(self, result):
        # 对抓取到网页的数据做处理
        result = re.sub('\n+',"",result)
        result = re.sub('  +',"",result)
        result = re.sub('\t+',"",result)
        result = re.sub('\r+', '',result)
        # result = re.sub(',+',' ',result)
        # result = re.sub('，+',' ',result)
        result = re.sub('&nbsp+', ' ',result)
        return result


'''
scrapy close 插件
'''
class RedisSpiderSmartIdleClosedExtensions(object):

    def __init__(self, idle_number, crawler):
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查是否应该启用和提高扩展
        # 否则不配置
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # 获取配置中的时间片个数，默认为360个，30分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 360)

        # 实例化扩展对象
        ext = cls(idle_number, crawler)

        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s redis spider Idle, Continuous idle limit： %d", spider.name, self.idle_number)

    def spider_closed(self, spider):
        logger.info("closed spider %s, idle count %d , Continuous idle count %d",
                    spider.name, self.idle_count, len(self.idle_list))

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数

        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and self.idle_list[-1] - self.idle_list[-2] > 10:
            self.idle_list = [self.idle_list[-1]]

        elif idle_list_len > self.idle_number:
            # 连续触发的次数达到配置次数后关闭爬虫
            logger.info('\n continued idle number exceed {} Times'
                        '\n meet the idle shutdown conditions, will close the reptile operation'
                        '\n idle start time: {},  close spider time: {}'.format(self.idle_number,
                                                                                self.idle_list[0], self.idle_list[0]))
            # 执行关闭爬虫操作
            self.crawler.engine.close_spider(spider, 'closespider_pagecount')







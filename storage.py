"""
代理存储模块
"""
import redis
from model import Proxy
from p_exceptions import NotProxyError, PoolEmptyError
from crawl import XiCiProxyHelper
from datetime import datetime
from random import choice

DEBUG_MODE = False

class RedisClient(object):
    """
    Proxies storage container
    """
    __MAX_SCORE = 100
    __MIN_SCORE = 50
    __INITIAL_SCORE = 80

    __REDIS_HOST = ''
    __REDIS_PORT = ''
    __REDIS_PSW = ''
    __REDIS_STORAGE_KEY = ''


    def __init__(self, host='localhost', port=6379, password=None, s_key='hades_proxies', num=1):
        """
        Initial storage client
        :param self:
        :param host: redis host, default as localhost
        :param port: redis port, default as 6379
        :param password: redis login password
        :param s_key: storage key
        :param num: call get_proxy() return number at one time
        """
        self.__REDIS_HOST = host
        self.__REDIS_PORT = port
        self.__REDIS_PSW = password
        self.__REDIS_STORAGE_KEY = s_key
        self.__num = num
        self.__db = redis.StrictRedis(self.__REDIS_HOST, self.__REDIS_PORT, password=self.__REDIS_PSW, decode_responses=True)


    def add(self, proxy_serializer):
        """
        添加代理
        :param self:
        :param proxy: Proxy object
        """
        if not self.__db.zscore(self.__REDIS_STORAGE_KEY, proxy_serializer):
            return self.__db.zadd(self.__REDIS_STORAGE_KEY, {proxy_serializer:self.__INITIAL_SCORE}) 
    

    def get_proxy(self):
        """
        获取num个较优的proxy。
        :param self:
        :param num: default 1, 返回个数
        2019年02月28日 11:50:55
        将筛选范围改为100-initial，不允许检测过无效的ip进入可选范围
        """
        result = self.__db.zrevrangebyscore(self.__REDIS_STORAGE_KEY, self.__MAX_SCORE, self.__INITIAL_SCORE)
        if len(result):
            proxies = []
            for i in range(0, self.__num): 
                proxies.append(Proxy().re_serialize(choice(result)))
            return proxies
        else:
            raise PoolEmptyError
    

    def remove_by_range(self, min_score, max_score):
        """
        按照范围清理代理池
        :param self:
        :param min_score: 最小值
        :param max_score: 最大值
        """
        self.__db.zremrangebyscore(self.__REDIS_STORAGE_KEY, min_score, max_score)
    

    def decrease(self, proxy_serializer):
        """
        降低代理可用值
        """
        score = self.__db.zscore(self.__REDIS_STORAGE_KEY, proxy_serializer)
        if score and score > self.__MIN_SCORE:
            return self.__db.zincrby(self.__REDIS_STORAGE_KEY, -1, proxy_serializer)
        else:
            # 2019年02月28日 11:40:29
            # 修复逻辑错误
            if DEBUG_MODE:
                print("{}    淘汰代理{}".format(datetime.now(), proxy_serializer))
            return self.__db.zrem(self.__REDIS_STORAGE_KEY, proxy_serializer)
    

    def increase(self, proxy_serializer):
        """
        增加代理可用值
        """
        score = self.__db.zscore(self.__REDIS_STORAGE_KEY, proxy_serializer)
        if score and score < self.__MAX_SCORE:
            return self.__db.zincrby(self.__REDIS_STORAGE_KEY, +1, proxy_serializer)
        else:
            return 0
    

    def count(self):
        """
        返回可用数量
        """
        return self.__db.zcard(self.__REDIS_STORAGE_KEY)

    
    def all(self):
        """
        返回所有代理
        """
        result = self.__db.zrangebyscore(self.__REDIS_STORAGE_KEY, self.__MIN_SCORE, self.__MAX_SCORE)
        proxies = []
        for i in result:
            proxies.append(Proxy().re_serialize(i))
        return proxies
    

    def show(self):
        """
        展示所有代理及分数
        """
        print('+{}+{}+'.format('-'*21, '-'*8))
        result = self.__db.zrevrangebyscore(self.__REDIS_STORAGE_KEY, self.__MAX_SCORE, self.__MIN_SCORE)
        for i in result:
            proxy = Proxy().re_serialize(i)
            score = self.__db.zscore(self.__REDIS_STORAGE_KEY, i)
            size = 20 - len(proxy.ip+proxy.port)
            print('|{}:{}{}|  {}  |'.format(proxy.ip, proxy.port, ' '*size, score))
        print('+{}+{}+'.format('-'*21, '-'*8))
            


class Booter(object):
    """启动器 抓取->存储"""
    
    CAPACITY = 1000

    def __init__(self, redis_client, crwaler, capacity=1000, ):
        self.__redis = redis_client
        self.__crawler = crwaler
        self.CAPACITY=capacity
    

    def is_over_capacity(self):
        if self.__redis.count() > self.CAPACITY:
            return True
        else:
            return False

    
    def run(self):
        print('{}    正在爬取代理服务...'.format(datetime.now()))
        if not self.is_over_capacity():
            http = self.__crawler.get_http_proxy()
            # https 暂时不抓取
            # https = self.__crawler.get_https_proxy()
            # http.extend(https)
            for item in http:
                self.__redis.add(item.serializer(convert_to_json=True))
        print('{}    本次一共爬取{}个代理服务器...'.format(datetime.now(), len(http)))





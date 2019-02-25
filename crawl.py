
import re
import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from model import Proxy
from p_exceptions import KindError 

class XiCiProxyHelper(object):
    """
    代理获取类
    从西刺免费代理网页获取HTTPS和HTTP代理
    """

    __headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15',
    }

    __HTTP_GET_URL = 'https://www.xicidaili.com/wt/{}'
    __HTTPS_GET_URL = 'https://www.xicidaili.com/wn/{}'

    def __init__(self, quantity=20, threshold=2.000):
        """
        :param self:
        :param quantity: 每次返回的数量。默认 20 条
        :param threshold: 延迟下限阀值。默认 2.000 秒
        """
        self.__quantity = quantity
        self.__threshold = threshold
    
    def __get_page(self, kind, page=1):
        """
        获取西刺网页
        :param self:
        :param kind: 种类(0 - http, 1 - https)
        :param page: 页数 
        """
        if 0 == kind:
            response = requests.get(self.__HTTP_GET_URL.format(page), headers = self.__headers)
            if response.status_code == 200:
                return response.text
            else:
                raise ConnectionError
        elif 1 == kind:
            response = requests.get(self.__HTTPS_GET_URL.format(page), headers = self.__headers)
            if response.status_code == 200:
                return response.text
            else:
                raise ConnectionError
        else:
            raise KindError("The parameter must 0 or 1")

    
    def get_https_proxy(self):
        """
        返回 https 代理
        """
        result = list()
        page = 1
        while True:
            if len(result) > self.__quantity:
                result = result[0:self.__quantity]
                break
            html = self.__get_page(1, page=page)
            result.extend(self.__parse_html(html, 'https'))
            page += 1
        return result
    

    def get_http_proxy(self):
        """
        返回 http 代理字典
        """
        result = list()
        page = 1
        while True:
            if len(result) > self.__quantity:
                result = result[0:self.__quantity]
                break
            html = self.__get_page(0, page=page)
            result.extend(self.__parse_html(html, 'http'))
            page += 1
        return result
        
    
    def __parse_html(self, html, link_type):
        """
        解析网页
        :param html: 源码
        """
        result = list()
        doc = pq(html)
        trs = doc('#ip_list > tr').items()
        trs.__next__()
        for tr in trs:
            text_speed = tr('.bar').attr('title')
            if self.__check_delay(text_speed):
                child = tr.children()
                ip = child.eq(1).text()
                port = child.eq(2).text()
                site = child.eq(3).text()
                result.append(Proxy(ip=ip, port=port, site=site, p_type=link_type, delay=text_speed))
        return result

    
    def __check_delay(self, text):
        """
        传入文本检测该item是否符合threshold的要求。
        :param self: 
        :param text: 取值文本。
        """
        pattern = r'(\d+).(\d+)'
        m = re.match(pattern, text)
        delay = float(m.group(0))
        if delay > self.__threshold:
            return False
        else:
            return True


if __name__ == '__main__':
    te = XiCiProxyHelper(threshold=1.000)
    result = te.get_http_proxy()
    print(result[0].serializer(need_site=False))
    result = te.get_https_proxy()
    print(result[0].serializer())

import aiohttp
from aiohttp.client_exceptions import ClientError, ClientConnectionError, ClientResponseError
from datetime import datetime
import asyncio
import time
from asyncio import TimeoutError

class Detector(object):
    """代理检测器"""

    VALID_STATUS_CODE = 200
    TEST_URL = 'http://www.baidu.com'
    BATCH_TEST_SIZE = 100

    def __init__(self, redis_client, valid_status_code=200, test_url='http://www.baidu.com', test_size=100):
        self.__redis = redis_client
        self.VALID_STATUS_CODE = valid_status_code
        self.TEST_URL = test_url
        self.BATCH_TEST_SIZE = test_size
    

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 
        """

        conn = aiohttp.TCPConnector()
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                test_proxy = '{}://{}:{}'.format(proxy.p_type, proxy.ip, proxy.port)
                async with session.get(self.TEST_URL, proxy=test_proxy, timeout=15) as response:
                    if response.status == self.VALID_STATUS_CODE:
                        self.__redis.increase(proxy.serializer(convert_to_json=True))        
                    else:
                        self.__redis.decrease(proxy.serializer(convert_to_json=True))     
            except Exception:
                #  2019年02月27日 22:51:05
                # 这里修改为只要出现错误都直接decrease，因为会出错的Exceptions太多。
                # 并且Xici上的代理多数不稳定。暂时先这样修改，如果有更好的建议请发邮件或者在issue底下提出感谢。
                # email: geekhades1@gmail.com
                self.__redis.decrease(proxy.serializer(convert_to_json=True))
                

    
    def run(self):
        """
        测试主函数
        """
        print("{}    检测器运行...".format(datetime.now()))
        try:
            proxies = self.__redis.all()
            loop = asyncio.get_event_loop()
            # 批量测试
            for i in range(0, len(proxies), self.BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+self.BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('{}    检测器错误'.format(datetime.now()), e.args)



                
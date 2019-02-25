import sys, getopt
from configparser import ConfigParser, NoOptionError
from scheduler import Scheduler
from storage import RedisClient
from crawl import XiCiProxyHelper
from storage import Booter
from detector import Detector
from flask import Flask, g
from datetime import datetime
import json

__all__ = ['app']
app = Flask(__name__)


REDIS_HOST = None
REDIS_PORT = None
REDIS_PASSWORD = None
REDIS_KEY = None

API_SERVER_HOST = None
API_SERVER_PORT = None

DETECTOR_MINUTE = None
GETTER_MINUTE = None
GET_NUM = None

THRESHOLD = None
QUANTITY = None
CAPACITY = None



def usage():
    print('-h --help: show help')
    print('-d --default: start by default config')
    print('-c path --config path: use config to setting proxy, example is proxy.conf')


def try_to_get_options(cfg_func, section, key):
    if not callable(cfg_func):
        raise TypeError('cfg_func must a config parse get* function')
    try:
        value = cfg_func(section, key)
        return value
    except NoOptionError:
        return None


def parse_config(path='proxy.conf'):
    cfg = ConfigParser()

    f = cfg.read(path)
    if len(f) == 0:
        raise FileNotFoundError('{} not found'.format(path))
    
    global REDIS_HOST
    global REDIS_PORT
    global REDIS_PASSWORD
    global REDIS_KEY
    global API_SERVER_HOST
    global API_SERVER_PORT
    global DETECTOR_MINUTE
    global GETTER_MINUTE
    global GET_NUM
    global QUANTITY
    global THRESHOLD
    global CAPACITY

    REDIS_HOST = try_to_get_options(cfg.get, 'redis', 'host')
    REDIS_PORT = try_to_get_options(cfg.getint, 'redis', 'port')
    REDIS_PASSWORD = try_to_get_options(cfg.get, 'redis', 'password')
    REDIS_KEY = try_to_get_options(cfg.get, 'redis', 'key')
    
    API_SERVER_HOST = try_to_get_options(cfg.get, 'server', 'host')
    API_SERVER_PORT = try_to_get_options(cfg.getint, 'server', 'port')

    DETECTOR_MINUTE = try_to_get_options(cfg.getint, 'other', 'detector_minute')
    GETTER_MINUTE = try_to_get_options(cfg.getint, 'other', 'getter_minute')
    GET_NUM = try_to_get_options(cfg.getint, 'other', 'get_num')

    QUANTITY = try_to_get_options(cfg.getint, 'proxy_setting', 'quantity')
    THRESHOLD = try_to_get_options(cfg.getfloat, 'proxy_setting', 'threshold')
    CAPACITY = try_to_get_options(cfg.getfloat, 'proxy_setting', 'capacity')
    


def parse_cmd():
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 'hc:d', ['help', 'config', 'default'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    if len(opts) == 0:
        print('Error, require -c or -d')
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-c', '--config'):
            parse_config(a)
        elif o in ('-d', '--default'):
            parse_config()
        else:
            assert False, "unhandled option"

detector = None
booter = None
redis_client = None
def init_module():
    global detector
    global booter
    global redis_client
    redis_client = RedisClient(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, s_key=REDIS_KEY, num=GET_NUM)
    xc = XiCiProxyHelper(quantity=QUANTITY, threshold=THRESHOLD)
    detector = Detector(redis_client)
    booter = Booter(redis_client, xc, capacity=CAPACITY)


@app.route('/get')
def get_proxy():
    """
    获取一组可用代理
    """
    result = []
    proxies = redis_client.get_proxy()
    for i in proxies:
        result.append(i.serializer())
    return json.dumps(result, ensure_ascii=False)
    

def run_api_server():
    print('{}    服务器开启...'.format(datetime.now()))
    app.run(host=API_SERVER_HOST, port=API_SERVER_PORT)

def main():
    parse_cmd()
    init_module()
    scheduler = Scheduler(detector, booter, detect_minute=DETECTOR_MINUTE, get_minute=GETTER_MINUTE)
    scheduler.run()
    run_api_server()





if __name__ == "__main__":
    main()

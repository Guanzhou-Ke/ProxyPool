"""
clear database script
"""

from storage import RedisClient
from configparser import ConfigParser, NoOptionError

def try_to_get_options(cfg_func, section, key):
    if not callable(cfg_func):
        raise TypeError('cfg_func must a config parse get* function')
    try:
        value = cfg_func(section, key)
        return value
    except NoOptionError:
        return None

while True:
    path = input('Please input config file path(if you use default file type \'d\'.): ')
    if path == 'd':
        path = 'proxy.conf'
    sure = input('Are you sure the config file in \'{}\'. [y/n]: '.format(path))
    if sure == 'y':
        break;

cfg = ConfigParser()
cfg.read(path)
REDIS_HOST = try_to_get_options(cfg.get, 'redis', 'host')
REDIS_PORT = try_to_get_options(cfg.getint, 'redis', 'port')
REDIS_PASSWORD = try_to_get_options(cfg.get, 'redis', 'password')
REDIS_KEY = try_to_get_options(cfg.get, 'redis', 'key')
redis_client = RedisClient(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, s_key=REDIS_KEY)
count = redis_client.count()
if count == 0:
    print('Already cleaning!')
else:
    redis_client.show()
    sure = input('Are you sure remove that data? amount {} items! [y/n]: '.format(count))
    if sure == 'y':
        redis_client.remove_by_range(0, 100)
    else:
        print('Good luck! Bye Bye')

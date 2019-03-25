# ProxyPool
## README
#### [English Docs](https://github.com/GeekHades1/ProxyPool/blob/master/README.md)   |   [中文版文档](https://github.com/GeekHades1/ProxyPool/blob/master/README-CN.md)

## Introduction

This is a proxy server which can build quick and easy, it able to continuously obtain the lastest proxies by xici.com, and continuing to diagnose existing proxies during runtime.


## Quick Start

After installing all the packages in `requirements.txt`, type `python proxy.py -d` at the command line. Finally, obtain proxies by open `${host}:${port}/get`

## Remove data 
if you want to remove redundancy data, you could run `clear_db.py`


## Config File
When you use the arguments `-d` to start server, server will automatic to load all config in default file `proxy.conf`. You can also pass your custom configuration file using `-c configpath`. The parameters are briefly described below.


```
# Redis client config
[redis]
host=localhost
port=6379
# If you has password, could remove the sharp
# password=
# If you want to modify default key, could remove the sharp
key=hades_proxies

# Api server config
[server]
host=localhost
port=8000

[proxy_setting]
# proxy delay
threshold=1.000
# quantity of crawls at one time
quantity=20  
# proxy capacity
capacity=1000
# If you need to test a specific 'url', you can fill in the following options     
url=www.baidu.com

# You could modify detector and proxy getter running cycle in there.
[other]
# the cycle of detector running, default is five minute
detector_minute=5
# the cycle of crawler running, default is twenty minute
getter_minute=20
# Number of proxies returned when requesting the server
get_num=1
```

# ProxyPool
## README
#### [中文版文档](https://github.com/GeekHades1/ProxyPool/blob/master/README-CN.md)   |   [English Docs](https://github.com/GeekHades1/ProxyPool/blob/master/README.md)

## 介绍
一款基于`Flask`快速搭建的代理服务器，能够从西刺持续的获取最新的符合延迟要求的免费服务器，并且在运行期间持续对已有的代理池进行诊断，保证每次获取的代理都是高可用的。

## 快速运行
在装完`requirements.txt`所需要的依赖包后，只需要在命令行键入`python proxy -d`即可快速搭建一个代理服务器。

## 配置说明
使用`-d`只是以默认的配置文件`proxy.conf`所分配的属性开启代理服务器。当然您也可以使用`-c configpath` 的方式传入您自定义的配置文件。下面对参数进行简要说明。
```
# 指定redis参数域
[redis]
# 本机部署的redis链接主机名以及端口
host=localhost
port=6379
# 密码，如果有的话打开注释填充，如果没有可以省略
# password=
# 如果你希望重新定义一个存储代理的键名可以修改key属性
key=hades_proxies


# 代理服务器参数域 host和port分别是你希望部署在本机的哪个端口
[server]
host=localhost
port=8000

# 代理抓取参数域
[proxy_setting]
# 代理服务器的抓取延迟阀值，默认只抓取低于1秒的代理服务器，如果您需要更加严格的速度可以修改此选项。
threshold=1.000
# 每次抓取的代理数量
quantity=20  
# 代理池的总容量
capacity=1000

# 一些其他参数配置
[other]
# 检测器检测间隔 单位为分钟
detector_minute=5
# 爬虫爬取间隔 单位为分钟
getter_minute=20
# 代理服务器每次请求返回的个数， 默认返回一个
get_num=1
```

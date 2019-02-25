import json

class Proxy(object):
    """
    代理对象
    """
    ip = ""
    port = ""
    site = ""
    p_type = ""
    delay = ""

    def __init__(self, ip=None, port=None, site=None, p_type=None, delay=None):
        self.ip = ip
        self.port = port
        self.site = site
        self.p_type = p_type
        self.delay = delay
    

    def serializer(self, need_site=True, need_type=True, need_delay=True, convert_to_json=False):
        """
        对象数据序列化
        :param self:
        :param need_site: 需要序列化位置参数
        :param need_type: 需要序列化类型参数
        :param need_delay: 需要序列化速度参数
        """
        result = {
            'ip': self.ip,
            'port': self.port,
        }
        if need_site:
            result['site'] = self.site
        if need_type:
            result['type'] = self.p_type
        if need_delay:
            result['delay'] = self.delay
        if convert_to_json:
            return json.dumps(result, ensure_ascii=False)
        return result
        
    
    def re_serialize(self, json_str):
        """
        反序列化
        """
        s = json.loads(json_str, encoding='utf-8')
        self.ip = s['ip']
        self.port = s['port']
        if 'site' in s:
            self.site = s['site']
        if 'type' in s:
            self.p_type = s['type']
        if 'delay' in s:
            self.delay = s['delay']
        return self
    

    def __str__(self):
        return self.serializer(convert_to_json=True)

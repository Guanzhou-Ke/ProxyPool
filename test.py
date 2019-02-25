from crawl import XiCiProxyHelper
from storage import Booter, RedisClient
from detector import Detector

if __name__ == "__main__":
    xch = XiCiProxyHelper(quantity=40, threshold=1.000)
    rc = RedisClient()
    
    b = Booter(rc, xch)
    b.run()

    de = Detector(rc)
    
    de.run()
    print('一共有{}'.format(rc.count()))

    rc.show()

    rc.remove_by_range(0,100)
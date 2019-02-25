class Error(Exception):
    """
    base exception
    """
    pass

class KindError(Error):
    pass

class NotProxyError(Error):
    pass

class PoolEmptyError(Error):
    pass
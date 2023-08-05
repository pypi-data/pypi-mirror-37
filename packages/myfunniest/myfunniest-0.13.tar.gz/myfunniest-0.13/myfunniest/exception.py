
class ServiceException(Exception):
    """
    参数类异常：          2xxx
    非法操作类异常：      3xxx
    接口调用类异常：      4xxx
    系统类异常：         9xxx
    """
    code = 9999
    message = '系统调用错误'


class PowerCacheCallFailedException(ServiceException):
    code = 4004
    message = 'PowerCache调用失败'


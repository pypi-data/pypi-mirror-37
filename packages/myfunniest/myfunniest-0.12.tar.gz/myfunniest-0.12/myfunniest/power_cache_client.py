import requests

AppConfig = "http://powercache-proxy-test.zhonganonline.com/powercache/api"


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


class PowerCacheClient:
    query_api = 'http://{uri}'.format(uri=AppConfig.POWER_CACHE_URI)
    op_set_string = 'setstring'
    op_get_string = 'getstring'
    op_delete = 'delete'

    @classmethod
    def set_string(cls, key: str, value: str, expired_time: int):
        """
        设置指定key的值（字符串类型）
        :param key: 键
        :param value: 值
        :param expired_time: 指定时长后过期，单位为秒，可为null（永不过期）
        :return:
        """
        args = {'key': key, 'value': value, 'expireTime': expired_time}
        response = cls._request(cls.op_set_string, args).json()
        if not response.get('success'):
            raise PowerCacheCallFailedException

    @classmethod
    def get_string(cls, key: str, require_expire_time: bool = False):
        """
        获取指定key的值（字符串类型）
        :param key: 建
        :param require_expire_time: 是否需要超时时间
        :return:
        """
        args = {'key': key, 'requireExpireTime': str(require_expire_time)}
        response = cls._request(cls.op_get_string, args).json()
        if response.get('success'):
            return response.get('result').get('value') if response.get('result') else None
        else:
            raise PowerCacheCallFailedException

    @classmethod
    def delete(cls, key: str):
        """
        在key存在时删除key
        :param key: 键
        :return:
            存在则返回1，不存在则返回0
        """
        args = {'key': key}
        response = cls._request(cls.op_delete, args).json()
        if response.get('success'):
            return response.get('result').get('value')
        else:
            raise PowerCacheCallFailedException

    @classmethod
    def _request(cls, operation: str, args: dict):
        request_body = {**args, 'namespace': int(AppConfig.POWER_CACHE_NAMESPACE)}
        request_url = cls.query_api + '/' + operation
        response = requests.post(request_url, json=request_body)
        return response

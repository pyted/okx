import hmac
import base64
import datetime
import urllib.parse as up
import json
import requests
import time


# 请求方法错误
class RequestMethodError(Exception):
    error_msg: str

    def __init__(self, msg):
        self.error_msg = msg

    def __str__(self):
        return self.error_msg


# 响应状态码错误
class ResponseStatusError(Exception):
    error_msg: str

    def __init__(self, msg):
        self.error_msg = msg

    def __str__(self):
        return self.error_msg


def request_retry_wrapper(retry_num=50, retry_delay=0.1):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            for i in range(retry_num - 1):
                try:
                    result = func(*args, **kwargs)
                    # 50001 服务暂时不可用，请稍后重试
                    # 50004 接口请求超时（不代表请求成功或者失败，请检查请求结果）
                    # 50011 用户请求频率过快，超过该接口允许的限额。请参考 API 文档并限制请求
                    # 50013 当前系统繁忙，请稍后重试
                    # 50026 系统错误，请稍后重试
                    if result['code'] in ['50001', '50004', '50011', '50013', '50026']:
                        time.sleep(retry_delay)
                        continue
                    else:
                        return result
                except requests.exceptions.ConnectionError:
                    time.sleep(retry_delay)
            result = func(*args, **kwargs)
            return result

        return wrapper2

    return wrapper1


class Client(object):
    API_URL = 'https://www.okx.com'

    def __init__(
            self,
            key='',
            secret='',
            passphrase='',
            flag='0',
            proxies={},
            proxy_host: str = None,
            retry_num=50,
            retry_delay=0.1,
    ):
        self.key = key
        self.secret = secret
        self.passphrase = passphrase
        self.flag = flag
        self.proxies = proxies
        if proxy_host and proxy_host.endswith('/'):
            proxy_host = proxy_host[0:-1]
        self.proxy_host = proxy_host
        self.retry_num = retry_num
        self.retry_delay = retry_delay

    def send_request(self, path, method, *args, **params):
        @request_retry_wrapper(retry_num=self.retry_num, retry_delay=self.retry_delay)
        def inner(path, method, **params):
            params_no_empty = {}
            for k, v in params.items():
                if v not in ['', [], {}, None] and k not in ['proxies', 'proxy_host']:
                    params_no_empty[k] = v
            # path
            if method == 'GET' and params_no_empty:
                path = path + '?' + up.urlencode(params_no_empty)
            # params中的proxy_host优先级 大于 self.proxy_host 大于 API_URL
            # url
            if params['proxy_host']:
                proxy_host = params['proxy_host']
                if proxy_host.endswith('/'):
                    proxy_host = proxy_host[0:-1]
                url = proxy_host + path
            elif self.proxy_host:
                url = self.proxy_host + path
            else:
                url = up.urljoin(self.API_URL, path)
            # params中proxies的优先级高于self.proxies
            if 'proxies' in params.keys() and params['proxies']:
                proxies = params['proxies']
            else:
                proxies = self.proxies
            # body
            if method == 'POST':
                # 类似批量下单这种无Key类型的body
                if args:
                    body = json.dumps(args[0])
                else:
                    body = json.dumps(params_no_empty)
            else:
                body = ''
            timestamp = datetime.datetime.utcnow().isoformat("T", "milliseconds") + 'Z'
            # sign
            sign = self._get_sign(
                message=self._pre_hash(timestamp, method, path, body),
                secret=self.secret,
            )
            # header
            header = self._get_header(
                key=self.key,
                sign=sign,
                passphrase=self.passphrase,
                flag=self.flag,
                timestamp=timestamp
            )

            # request
            if method == 'GET':
                if 'proxies' in params.keys() and params['proxies']:
                    response = requests.get(url, headers=header, proxies=proxies)
                else:
                    response = requests.get(url, headers=header, proxies=proxies)

            elif method == 'POST':
                response = requests.post(url, data=body, headers=header, proxies=self.proxies)
            else:
                msg = 'Error request method {method}'.format(method=str(method))
                raise RequestMethodError(msg)

            if not str(response.status_code).startswith('2'):
                msg = 'Error response_status_code {code}\nresponse_content={content}'.format(code=response.status_code,
                                                                                             content=response.text)
                raise ResponseStatusError(msg)
            return response.json()

        return inner(path, method, **params)

    @staticmethod
    def _get_sign(message, secret):
        mac = hmac.new(bytes(secret, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    @staticmethod
    def _pre_hash(timestamp, method, request_path, body):
        return str(timestamp) + str.upper(method) + request_path + body

    @staticmethod
    def _get_header(key, sign, passphrase, flag, timestamp):
        header = {}
        header['Content-Type'] = 'application/json'
        header['OK-ACCESS-KEY'] = key
        header['OK-ACCESS-SIGN'] = sign
        header['OK-ACCESS-TIMESTAMP'] = str(timestamp)
        header['OK-ACCESS-PASSPHRASE'] = passphrase
        header['x-simulated-trading'] = flag
        return header

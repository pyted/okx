from okx import Status
from pprint import pprint

if __name__ == '__main__':
    # System模块无需秘钥
    key = ''
    secret = ''
    passphrase = ''
    flag = '0'

    status = Status(key, secret, passphrase, flag)
    # 获取系统升级事件的状态
    result = status.get_status()
    pprint(result)

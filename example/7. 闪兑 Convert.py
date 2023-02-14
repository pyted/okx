from okx import Convert
from pprint import pprint

if __name__ == '__main__':
    # 闪兑模块需要秘钥
    key = '****'
    secret = '****'
    passphrase = '****'
    flag = '0'

    convert = Convert(key, secret, passphrase, flag)

    # 获取闪兑币种列表
    result = convert.get_currencies()
    pprint(result)

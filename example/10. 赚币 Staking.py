from okx import Earn
from pprint import pprint

if __name__ == '__main__':
    # 赚币模块需要秘钥
    key = '****'
    secret = '****'
    passphrase = '****'
    flag = '0'

    earn = Earn(key, secret, passphrase, flag)

    # 查看项目
    result = earn.get_offers()
    pprint(result)

from okx import Staking
from pprint import pprint

if __name__ == '__main__':
    # 赚币模块需要秘钥
    key = '****'
    secret = '****'
    passphrase = '****'
    flag = '0'

    staking = Staking(key, secret, passphrase, flag)

    # 查看项目
    result = staking.get_offers()
    pprint(result)

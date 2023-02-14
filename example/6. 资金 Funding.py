from okx import Funding
from pprint import pprint

if __name__ == '__main__':
    # 资金模块需要秘钥
    key = '****'
    secret = '****'
    passphrase = '****'
    flag = '0'

    funding = Funding(key, secret, passphrase, flag)

    # 获取资金账户余额
    result = funding.get_balances(ccy='USDT')
    pprint(result)

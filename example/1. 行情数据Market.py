from okx import Market
from pprint import pprint

if __name__ == '__main__':
    # 行情数据模块无需秘钥
    key = ''
    secret = ''
    passphrase = ''
    flag = '0'

    market = Market(key, secret, passphrase, flag)
    # 获取所有产品行情信息
    result = market.get_tickers(instType='SPOT')  # SPOT币币
    pprint(result)

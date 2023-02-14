from okx import Trade
from pprint import pprint

if __name__ == '__main__':
    # 交易模块需要秘钥
    key = '****'
    secret = '****'
    passphrase = '****'
    flag = '0'

    trade = Trade(key, secret, passphrase, flag)

    # 限价单购买BTC-USDT现货，数量2，价格1
    result = trade.set_order(
        instId='BTC-USDT',
        tdMode='cash',
        side='buy',
        ordType='limit',
        px='1',
        sz='2',

    )
    pprint(result)

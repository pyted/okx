from okx import Public
from pprint import pprint

if __name__ == '__main__':
    # 公共数据模块无需秘钥
    key = ''
    secret = ''
    passphrase = ''
    flag = '0'

    public = Public(key, secret, passphrase, flag)
    # 获取交易产品基础信息
    result = public.get_instruments(instType='SWAP', instId='BTC-USDT-SWAP')
    pprint(result)

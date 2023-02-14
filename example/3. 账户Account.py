from okx import Account
from pprint import pprint

if __name__ == '__main__':
    # 账户数据必须添加key、secret与passphrase
    key = '****'
    secret = '****'
    passphrase = '****'
    flag = '0'

    account = Account(key, secret, passphrase, flag)
    # 查看USDT账户余额
    pprint(account.get_balance(ccy='USDT'))

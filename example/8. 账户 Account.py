from okx import Account
from pprint import pprint

if __name__ == '__main__':
    # 账户模块需要秘钥
    key = '****'
    secret = '****'
    passphrase = '****'
    flag = '0'
    
    account = Account(key, secret, passphrase, flag)

    # 查看账户USDT余额
    result = account.get_balance('USDT')
    pprint(result)

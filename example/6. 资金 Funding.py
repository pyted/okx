from okx import FundingAccount
from pprint import pprint

if __name__ == '__main__':
    # 资金模块需要秘钥
    key = '****'
    secret = '****'
    passphrase = '****'
    flag = '0'

    fundingAccount = FundingAccount(key, secret, passphrase, flag)

    # 获取资金账户余额
    result = fundingAccount.get_balances(ccy='USDT')
    pprint(result)

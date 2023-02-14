from okx import SubAccount
from pprint import pprint

if __name__ == '__main__':
    # 子账户模块需要秘钥
    key = '****'
    secret = '****'
    passphrase = '****'
    flag = '0'

    subAccount = SubAccount(key, secret, passphrase, flag)

    # 查看子账户列表
    result = subAccount.get_list()
    pprint(result)

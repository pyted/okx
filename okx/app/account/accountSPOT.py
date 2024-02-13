from okx.api import Account as AccountAPI
from okx.app import exception
from copy import deepcopy


class AccountSPOT():
    instType = 'SPOT'

    def __init__(
            self,
            key: str,
            secret: str,
            passphrase: str,
            proxies={},
            proxy_host: str = None,
    ):
        FLAG = '0'
        self.api = AccountAPI(
            key=key,
            secret=secret,
            passphrase=passphrase,
            flag=FLAG,
            proxies=proxies,
            proxy_host=proxy_host,
        )

    # 查看账户余额 details为列表
    def get_balances(self, instIds=[], ccys=[]):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-balance
        '''
        if instIds or ccys:
            inner_ccys = deepcopy(ccys)
            for instId in instIds:
                _ccy = instId.split('-')[0]
                if _ccy not in inner_ccys:
                    inner_ccys.append(_ccy)
            request_ccy = ','.join(inner_ccys)
            result = self.api.get_balance(ccy=request_ccy)
        else:
            result = self.api.get_balance()
        result['data'] = result['data'][0]
        return result

    # 查看账户余额 details为字典
    def get_balancesMap(self, instIds=[], ccys=[]):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-balance
        '''
        result = self.get_balances(instIds=instIds, ccys=ccys)
        data_map = {}
        for data in result['data']['details']:
            ccy = data['ccy']
            data_map[ccy] = data
        result['data']['details'] = data_map
        return result

    # 获取单个币种的余额
    def get_balance(self, instId: str = '', ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-balance

        :param instId: 产品ID
        :param ccy: 币种
        注意：
            1. instId 与 ccy 必须填写一个
            2. 当instId和ccy同时存在 优先级：ccy > instId
        '''
        if not ccy and not instId:
            msg = 'ccy and instId can not be empty together.'
            raise exception.ParamException(msg)
        if not ccy:
            ccy = instId.split('-')[0]
        result = self.api.get_balance(ccy=ccy)
        if not result['code'] == '0':
            return result
        result['data'] = result['data'][0]
        if len(result['data']['details']) == 0:
            result['data']['details'] = {}
        elif len(result['data']['details']) == 1:
            result['data']['details'] = result['data']['details'][0]
        else:
            msg = 'details got multi data,use get_balances instead.'
            raise exception.UnexpectedException(msg)
        return result

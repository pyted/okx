from typing import Union
from okx.api import Account as AccountAPI
from okx.app import exception
from copy import deepcopy


class AccountSWAP():
    instType = 'SWAP'

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
        if result['code'] != '0':
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

    # 设置持仓模式
    def set_position_mode(self, posMode: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-set-position-mode

        请求参数：
        Parameter         	Type    	Required	Description
        posMode           	String  	是       	持仓方式long_short_mode：双向持仓net_mode：单向持仓仅适用交割/永续
        '''
        result = self.api.set_position_mode(posMode=posMode)
        if result['code'] != '0':
            return result
        result['data'] = result['data'][0]
        return result

    # 设置杠杆倍数
    def set_leverage(
            self,
            lever: Union[str, int],
            mgnMode: str,
            instId: str = '',
            ccy: str = '',
            posSide: str = ''
    ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-set-leverage

        请求参数：
        Parameter         	Type    	Required	Description
        lever             	String  	是       	杠杆倍数
        mgnMode           	String  	是       	保证金模式isolated：逐仓cross：全仓如果ccy有效传值，该参数值只能为cross。
        instId            	String  	可选      	产品ID：币对、合约instId和ccy至少要传一个；如果两个都传，默认使用instId
        ccy               	String  	可选      	保证金币种仅适用于跨币种保证金模式的全仓币币杠杆。设置自动借币的杠杆倍数时必填
        posSide           	String  	可选      	持仓方向long：双向持仓多头short：双向持仓空头仅适用于逐仓交割/永续在双向持仓且保证金模式为逐仓条件下必填
        '''
        result = self.api.set_leverage(
            instId=instId,
            ccy=ccy,
            lever=lever,
            mgnMode=mgnMode,
            posSide=posSide,
        )
        return result

    # 获取杠杆倍数
    def get_leverage(
            self,
            instId: str,
            mgnMode: str,
    ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-leverage

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID支持多个instId查询，半角逗号分隔。instId个数不超过20个
        mgnMode           	String  	是       	保证金模式isolated：逐仓cross：全仓
        '''
        result = self.api.get_leverage_info(
            instId,
            mgnMode
        )
        if result['code'] != '0':
            return result

        data_map = {}

        for data in result['data']:
            posSide = data['posSide']
            data_map[posSide] = data
        result['data'] = data_map
        return result

    # 查看持仓信息
    def get_position(
            self,
            instId: str,
            mgnMode: str = '',
            posSide: str = '',
    ):
        get_positions_result = self.get_positions(instIds=[instId], mgnMode=mgnMode, posSide=posSide)
        return get_positions_result

    # 查看持仓信息 列表
    def get_positions(
            self,
            instIds: list = [],
            mgnMode: str = '',
            posSide: str = '',
    ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-positions

        :param instId: 产品ID
            instId = ''             全部产品
        :param mgnMode: 持仓类型
            mgnMode = 'isolated'    逐仓
            mgnMode = 'cross'       全仓
            mgnMode = ''            全部
        :param posSide: 持仓方向
            posSide = 'long'        多仓
            posSide = 'short'       空仓
            posSide = ''            全部
        '''
        requests_instId = ','.join(instIds)
        result = self.api.get_positions(
            instType=self.instType,
            instId=requests_instId, posId=''
        )
        if result['code'] != '0':
            return result
        datas_filtered = []  # 过滤mgnMode与posSide后的结果
        for data in result['data']:
            if mgnMode and data['mgnMode'] != mgnMode:
                continue
            if posSide and data['posSide'] != posSide:
                continue
            datas_filtered.append(data)
        result['data'] = datas_filtered
        return result

    # 查看持仓信息 字典
    def get_positionsMap(self):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-positions
        '''

        result = self.get_positions()
        if result['code'] != '0':
            return result
        data_map = {
            'isolated': {
                'long': {},
                'short': {},
            },
            'cross': {
                'long': {},
                'short': {},
            },
        }
        for data in result['data']:
            mgnMode = data['mgnMode']
            posSide = data['posSide']
            instId = data['instId']
            if instId not in data_map[mgnMode][posSide].keys():
                data_map[mgnMode][posSide][instId] = data
            else:
                msg = 'instId got multi positions by posSide and mgnMode, use get_positions instead.'
                raise exception.UnexpectedException(msg)
        result['data'] = data_map
        return result

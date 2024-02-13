import time
from okx.app import code
from okx.app.market._base import MarketBase


class ExchangeInfo(MarketBase):

    # 以缓存的方式获取全部交易产品基础信息
    def get_exchangeInfos(self, expire_seconds: int = 60 * 5, uly: str = ''):
        '''
        :param expire_seconds: 缓存时间（秒）
        :param uly: 标的指数，仅适用于交割/永续/期权，期权必填
        使用的缓存数据格式：
            self._exchangeInfo_cache = [
                {
                    'code':<状态码>,
                    'data':<exchangeInfo数据>,
                    'msg':<提示信息>,
                },
                <上次更新的毫秒时间戳>
            ]
        '''

        if (
                # 无缓存数据
                not hasattr(self, '_exchangeInfo_caches')
                or
                # 缓存数据过期
                getattr(self, '_exchangeInfo_caches')[1] - time.time() * 1000 >= expire_seconds
        ):
            # 更新数据并设置时间戳
            setattr(self, '_exchangeInfo_caches',
                    [self.publicAPI.get_instruments(instType=self.instType, uly=uly), time.time() * 1000])
        # 返回缓存数据
        return getattr(self, '_exchangeInfo_caches')[0]

    # 以缓存的方式获取单个交易产品基础信息
    def get_exchangeInfo(
            self,
            instId: str,
            expire_seconds: int = 60 * 5,
            uly: str = '',
    ):
        '''
        :param instId: 产品
        :param expire_seconds: 缓存时间（秒）
        :param uly: 标的指数，仅适用于交割/永续/期权，期权必填
        '''
        exchangeInfos_result = self.get_exchangeInfos(uly=uly, expire_seconds=expire_seconds)
        # [ERROR RETURN] 异常交易规则与交易
        if exchangeInfos_result['code'] != '0':
            return exchangeInfos_result
        # 寻找instId的信息
        for instId_data in exchangeInfos_result['data']:
            if instId_data['instId'] == instId:
                instId_data = instId_data
                break
        else:
            instId_data = None
        # [ERROR RETURN] 没有找到instId的交易规则与交易对信息
        if instId_data == None:
            result = {
                'code': code.EXCHANGE_INFO_ERROR[0],
                'data': exchangeInfos_result['data'],
                'msg': f'Symbol not found instId={instId}'
            }
            return result
        # 将filters中的列表转换为字典，里面可能包含下单价格与数量精度
        result = {
            'code': '0',
            'data': instId_data,
            'msg': '',
        }
        return result

    # 获取可以交易的产品列表
    def get_instIds_trading_on(
            self,
            expire_seconds: int = 60 * 5,
            uly: str = '',
    ) -> dict:
        '''
        :param expire_seconds: 缓存时间（秒）
        :param uly: 标的指数，仅适用于交割/永续/期权，期权必填
        '''
        exchangeInfos_result = self.get_exchangeInfos(uly=uly, expire_seconds=expire_seconds)
        # [ERROR RETURN] 异常交易规则与交易
        if exchangeInfos_result['code'] != '0':
            return exchangeInfos_result
        status_name = 'state'

        instIds = [
            data['instId']
            for data in exchangeInfos_result['data']
            if data[status_name] == 'live'
        ]
        # [RETURN]
        result = {
            'code': '0',
            'data': instIds,
            'msg': ''
        }
        return result

    # 获取不可交易的产品列表
    def get_instIds_trading_off(
            self,
            expire_seconds: int = 60 * 5,
            uly: str = '',
    ) -> dict:
        '''
        :param expire_seconds: 缓存时间（秒）
        :param uly: 标的指数，仅适用于交割/永续/期权，期权必填
        '''
        exchangeInfos_result = self.get_exchangeInfos(uly=uly, expire_seconds=expire_seconds)
        # [ERROR RETURN] 异常交易规则与交易
        if exchangeInfos_result['code'] != '0':
            return exchangeInfos_result
        status_name = 'state'

        instIds = [
            data['instId']
            for data in exchangeInfos_result['data']
            if data[status_name] != 'live'
        ]
        # [RETURN]
        result = {
            'code': '0',
            'data': instIds,
            'msg': ''
        }
        return result

    # 获取可以交易的产品列表
    def get_instIds_all(
            self,
            expire_seconds: int = 60 * 5,
            uly: str = '',
    ) -> dict:
        '''
        :param expire_seconds: 缓存时间（秒）
        :param uly: 标的指数，仅适用于交割/永续/期权，期权必填
        '''
        exchangeInfos_result = self.get_exchangeInfos(uly=uly, expire_seconds=expire_seconds)
        # [ERROR RETURN] 异常交易规则与交易
        if exchangeInfos_result['code'] != '0':
            return exchangeInfos_result
        instIds = [
            data['instId'] for data in exchangeInfos_result['data']
        ]
        # [RETURN]
        result = {
            'code': '0',
            'data': instIds,
            'msg': ''
        }
        return result

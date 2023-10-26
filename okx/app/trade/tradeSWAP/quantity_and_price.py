import math
from typing import Literal, Union
from paux import order as _order
from paux.digit import origin_float
from okx.app.trade.tradeSWAP._base import TradeBase
from okx.app import exception
from okx.app import code


class TradeQuantityAndPrice(TradeBase):
    # 下单数量圆整
    # Weight 0 | 1
    def round_quantity(
            self,
            quantity: Union[int, float, str, origin_float],
            instId: str,
            ordType: str,
            expire_seconds=60 * 5,
    ) -> dict:
        '''
        :param quantity: 下单数量
        :param instId: 产品
        :param ordType:  订单类型 limit market

        :param expire_seconds: 缓存过期时间 (秒)
        '''

        exchangeInfo = self._market.get_exchangeInfo(instId=instId, expire_seconds=expire_seconds)
        if exchangeInfo['code'] != '0':
            return exchangeInfo

        lotSz = exchangeInfo['data']['lotSz']  # 下单数量精度
        minSz = exchangeInfo['data']['minSz']  # 最小下单数量
        if ordType == 'limit':
            maxSz = exchangeInfo['data']['maxLmtSz']  # 合约或现货限价单的单笔最大委托数量
        elif ordType == 'market':
            maxSz = exchangeInfo['data']['maxMktSz']  # 合约或现货市价单的单笔最大委托数量
        else:
            msg = 'ordType must in ["limit","market"].'
            raise exception.ParamException(msg)
        stepSize = lotSz
        minQty = minSz
        maxQty = maxSz
        # code = 0 | -1 | -2
        round_quantity_result = _order.round_quantity(
            quantity=quantity,
            stepSize=stepSize,
            minQty=minQty,
            maxQty=maxQty
        )
        # code -> [200,code.ROUND_QUANTITY_ERROR[0]]
        if round_quantity_result['code'] == 0:
            round_quantity_result['code'] = '0'
        else:
            round_quantity_result['code'] = code.ROUND_QUANTITY_ERROR[0]
            round_quantity_result['msg'] = f'instId={instId} ' + round_quantity_result['msg']
        return round_quantity_result

    # 价格圆整
    # Weight 0 | 1
    def round_price(
            self,
            price: Union[int, float],
            instId: str,
            type: Literal['CEIL', 'FLOOR', 'ceil', 'floor'],
            expire_seconds=60 * 5,
    ) -> dict:
        '''
        :param price: 价格
        :param instId: 合约产品
        :param type: 圆整方式
                CEIL:   向上圆整
                FLOOR:  向下圆整
        :param expire_seconds: 缓存过期时间 (秒)
        '''
        # 验证type
        if type not in ['CEIL', 'FLOOR']:
            raise exception.ParamRoundPriceTypeException(type=type)

        exchangeInfo = self._market.get_exchangeInfo(
            instId=instId,
            expire_seconds=expire_seconds
        )
        if exchangeInfo['code'] != '0':
            return exchangeInfo

        tickSz = exchangeInfo['data']['tickSz']
        tickSize = tickSz
        # code = 0 | -1 | -2
        round_price_result = _order.round_price(
            price=price,
            type=type,
            tickSize=tickSize,
            minPrice=None,
            maxPrice=None
        )
        # code -> [200,code.ROUND_PRICE_ERROR[0]]
        if round_price_result['code'] == 0:
            round_price_result['code'] = '0'
        else:
            round_price_result['code'] = code.ROUND_PRICE_ERROR[0]
            round_price_result['msg'] = f'instId={instId} ' + round_price_result['msg']
        return round_price_result

    # 货币数量转化为合约张数
    def get_quantity_ctVal(
            self,
            quantity: Union[int, float],
            instId: str,
            ordType:str,
            expire_seconds=60 * 5
    ):
        '''
        :param quantity: 货币数量
        :param instId: 产品ID
        :param ordType: 订单类型 limit market
        '''
        exchangeInfo = self._market.get_exchangeInfo(
            instId=instId,
            expire_seconds=expire_seconds
        )
        if exchangeInfo['code'] != '0':
            return exchangeInfo
        ctVal = exchangeInfo['data']['ctVal']  # 合约面值 不为空表示合约
        quantity_ctVal = math.floor(quantity / float(ctVal))
        round_quantity_result = self.round_quantity(
            quantity=quantity_ctVal,
            instId=instId,
            ordType=ordType,
            expire_seconds=expire_seconds
        )
        return round_quantity_result


    # 根据合约产品的开仓金额、杠杆倍数、开仓价格获取购买数量
    # Weight 0 | 1
    def get_quantity(
            self,
            openPrice: Union[int, float],
            openMoney: Union[int, float],
            instId: str,
            ordType: str,
            leverage: int = 1,
            expire_seconds=60 * 5,
    ) -> dict:
        '''
        :param openPrice: 开仓价格
        :param openMoney: 开仓金额
        :param instId: 产品
        :param leverage: 杠杆数量
        :param expire_seconds: 缓存过期时间 (秒)
        '''
        exchangeInfo = self._market.get_exchangeInfo(
            instId=instId,
            expire_seconds=expire_seconds
        )
        if exchangeInfo['code'] != '0':
            return exchangeInfo

        ctVal = exchangeInfo['data']['ctVal']  # 合约面值 不为空表示合约
        # 有合约面值 -> 合约
        if ctVal:
            # 合约张数取整
            quantity = math.floor(openMoney * leverage / openPrice / float(ctVal))
            quantity_result = {
                'code': '0',
                'data': quantity,
                'msg': '',
            }
        # 无合约面值 -> 非合约
        else:
            quantity = openMoney * leverage / openPrice
            quantity_result = self.round_quantity(
                quantity=quantity,
                instId=instId,
                ordType=ordType,
            )
        return quantity_result

    # 将下单数量转化为字符串
    # Weight 0 | 1
    def quantity_to_f(
            self,
            quantity: Union[int, float],
            instId: str,
            expire_seconds=60 * 5,

    ) -> dict:
        '''
        :param quantity: 下单数量
        :param instId: 合约产品
        :param expire_seconds: 缓存过期时间 (秒)
        '''
        exchangeInfo = self._market.get_exchangeInfo(
            instId=instId,
            expire_seconds=expire_seconds
        )
        if exchangeInfo['code'] != '0':
            return exchangeInfo

        stepSize = lotSz = exchangeInfo['data']['lotSz']
        # code : 0 | -1
        quantity_to_f_result = _order.quantity_to_f(
            quantity=quantity,
            stepSize=stepSize,
        )
        # code -> [200,code.QUANTITY_TO_F_ERROR[0]]
        if quantity_to_f_result['code'] == 0:
            quantity_to_f_result['code'] = '0'
        else:
            quantity_to_f_result['code'] = code.QUANTITY_TO_F_ERROR[0]
            quantity_to_f_result['msg'] = f'instId={instId} ' + quantity_to_f_result['msg']
        return quantity_to_f_result

    # 将价格转化为字符串
    # Weight 0 | 1
    def price_to_f(
            self,
            price: Union[int, float],
            instId: str,
            expire_seconds=60 * 5,
    ) -> dict:
        '''
        :param price: 价格
        :param instId: 合约产品
        :param expire_seconds: 缓存过期时间 (秒)
        '''
        exchangeInfo = self._market.get_exchangeInfo(
            instId=instId,
            expire_seconds=expire_seconds
        )
        if exchangeInfo['code'] != '0':
            return exchangeInfo

        tickSize = tickSz = exchangeInfo['data']['tickSz']
        # code : 0 | -1
        price_to_f_result = _order.price_to_f(
            price=price,
            tickSize=tickSize
        )
        # code->[200,code.PRICE_TO_F_ERROR[0]]
        if price_to_f_result['code'] == 0:
            price_to_f_result['code'] = '0'
        else:
            price_to_f_result['code'] = code.PRICE_TO_F_ERROR[0]
            price_to_f_result['msg'] = f'instId={instId} ' + price_to_f_result['msg']
        return price_to_f_result

from typing import Union
import traceback
from threading import Thread
from paux.digit import origin_float, origin_int
from okx.app import code
from okx.app import exception
from okx.app.trade.tradeSWAP.order import TradeOrder
from okx.app.trade.tradeSWAP.quantity_and_price import TradeQuantityAndPrice


class TradeClose(TradeOrder, TradeQuantityAndPrice):
    # 限价单平仓
    def close_limit(
            self,
            instId: str,
            tdMode: str,
            posSide: str,
            closePrice: Union[int, float, str, origin_float, origin_int, None] = None,
            tpRate: Union[int, float, None] = None,
            quantityCT: Union[int, float, str, origin_float, origin_int] = 'all',
            meta: dict = {},
            block: bool = False,
            timeout: Union[int, float] = 60,
            delay: Union[int, float] = 0.2,
            cancel: bool = True,
            clOrdId: str = '',
            tag: str = '',
            newThread: bool = False,
            callback: object = None,
            errorback: object = None,
    ) -> dict:
        '''
        :param instId: 产品ID
        :param tdMode: 持仓方式
            isolated：逐仓 cross：全仓
        :param posSide: 持仓方向
            long：多单 short：空单
        :param closePrice: 卖出价格
        :param tpRate: 挂单止盈率
            注意：
                1. closePrice 和 tpRate必须填写其中一个
                2. closePrice 和 tpRate的优先级 closePrice > tpRate
                3. 当closePrice为空
                    posSide = 'long'    tpRate = askPrice * (1 + abs(tpRate))
                    posSide = 'short'   tpRate = bidPrice * (1 - abs(tpRate))
        :param quantityCT: 平仓数量
            注意：
                1. quantityCT是合约张数，并不是货币数量
                2. quantityCT = 'all' instId可用合约全部平仓
        :param meta: 回调函数传递参数
        :param block: 是否堵塞
        :param timeout: 订单超时时间 （秒)
        :param delay: 检测订单状态的间隔 (秒)
        :param cancel: 未完全成交是否取消订单
        :param clOrdId: 客户自定义订单ID
            字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间
        :param tag: 订单标签
            字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间
        :param newThread: 是否开启新线程执行
        :param callback: 非执行异常的回调函数
        :param errorback: 执行异常的回调函数
        '''

        # 常量参数
        ORDTYPE = 'limit'

        # 记录信息
        information = {
            'instType': 'SWAP',
            'instId': instId,
            'state': None,
            'ordId': None,
            'meta': meta,
            'request_param': None,
            'func_param': None,
            'get_order_result': None,
            'set_order_result': None,
            'error_result': None,
            'cancel_result': None,
        }

        # 函数的参数
        information['func_param'] = dict(
            instId=instId,
            tdMode=tdMode,
            posSide=posSide,
            closePrice=closePrice,
            tpRate=tpRate,
            quantityCT=quantityCT,
            meta=meta,
            block=block,
            timeout=timeout,
            delay=delay,
            cancel=cancel,
            clOrdId=clOrdId,
            tag=tag,
            newThread=newThread,
            callback=callback,
            errorback=errorback,
        )
        # meta
        information['meta'] = meta

        def main_func(
                instId=instId,
                tdMode=tdMode,
                posSide=posSide,
                closePrice=closePrice,
                tpRate=tpRate,
                quantityCT=quantityCT,
                clOrdId=clOrdId,
                tag=tag,
                block=block,
                timeout=timeout,
                delay=delay,
                cancel=cancel,
        ):
            # 验证posSide
            if posSide not in ['long', 'short']:
                msg = 'posSide must in ["long","short"].'
                raise exception.ParamException(msg)
            # 验证tdMode
            if tdMode not in ['isolated', 'cross']:
                msg = 'tdMode must in ["isolated","cross"].'
                raise exception.ParamException(msg)
            # closePrice和tpLine不能同时为空
            if closePrice in [None, ''] and tpRate in [None, '']:
                msg = 'closePrice and tpRate can not be empty together'
                raise exception.ParamException(msg)
            # 设置sell
            if posSide == 'long':
                side = 'sell'  # 卖出平多
            else:
                side = 'buy'  # 买入平空
            # 【卖出价格】 closePrice closePrice_f
            # 字符串
            if isinstance(closePrice, str):
                closePrice_f = closePrice
                closePrice = float(closePrice)
            # origin
            elif isinstance(closePrice, origin_float) or isinstance(closePrice, origin_int):
                closePrice_f = closePrice.origin()
                closePrice = closePrice
            # 数字对象和None
            else:
                # 如果没有closePrice，根据tpRate计算closePrice
                if not closePrice:
                    get_ticker_result = self._market.get_ticker(instId=instId)
                    # [ERROR RETURN]
                    if get_ticker_result['code'] != '0':
                        return get_ticker_result
                    # posSide = 'long' 使用卖出价格
                    if posSide == 'long':
                        askPx = get_ticker_result['data']['askPx']
                        askPx = float(askPx)
                        closePrice = askPx * (1 + abs(tpRate))
                    # posSide = 'short' 使用买入价格
                    else:
                        bidPx = get_ticker_result['data']['bidPx']
                        bidPx = float(bidPx)
                        closePrice = bidPx * (1 - abs(tpRate))
                # 圆整 -> closePrice
                # 卖出平多 价格向上圆整 买入平空 价格向下圆整
                round_price_result = self.round_price(
                    price=closePrice,
                    instId=instId,
                    type='CEIL' if posSide == 'long' else 'FLOOR'
                )
                # [ERROR RETURN]
                if round_price_result['code'] != '0':
                    return round_price_result
                closePrice = round_price_result['data']
                # 转化为字符串 closePrice_f
                closePrice_f_result = self.price_to_f(
                    price=closePrice,
                    instId=instId,
                )
                # [ERROR RETURN]
                if closePrice_f_result['code'] != '0':
                    return closePrice_f_result
                closePrice_f = closePrice_f_result['data']
            # 【卖出数量】 quantity quantity_f
            # 全部
            if quantityCT == 'all':
                positionMap_result = self._account.get_positionsMap()
                # [ERROR RETURN]
                if positionMap_result['code'] != '0':
                    return positionMap_result
                availPos = positionMap_result['data'][tdMode][posSide][instId]['availPos']
                availPos = origin_float(availPos)
                quantityCT = availPos
                quantityCT_f = availPos.origin()
            # 数值字符串
            elif isinstance(quantityCT, str):
                quantityCT_f = quantityCT
                quantityCT = float(quantityCT)
            # origin
            elif isinstance(quantityCT, origin_float) or isinstance(quantityCT, origin_int):
                quantityCT_f = quantityCT.origin()
            # 数字对象 圆整 转化为字符串
            else:
                round_quantity_result = self.round_quantity(
                    quantity=quantityCT, instId=instId,
                    ordType=ORDTYPE,
                )
                # [ERROR RETURN]
                if round_quantity_result['code'] != '0':
                    return round_quantity_result
                quantityCT = round_quantity_result['data']
                quantity_to_f_result = self.quantity_to_f(
                    quantity=quantityCT, instId=instId,
                )
                # [ERROR RETURN]
                if quantity_to_f_result['code'] != '0':
                    return quantity_to_f_result
                quantityCT_f = quantity_to_f_result['data']

            request_param = dict(
                instId=instId,
                tdMode=tdMode,
                posSide=posSide,
                side=side,
                ordType=ORDTYPE,
                sz=quantityCT_f,
                clOrdId=clOrdId,
                tag=tag,
                px=closePrice_f,
            )
            information['request_param'] = request_param
            set_order_result = self.set_order(**request_param)
            information['set_order_result'] = set_order_result
            ordId = set_order_result['data']['ordId']
            information['ordId'] = ordId
            # [ERROR RETURN]
            if set_order_result['code'] != '0':
                return set_order_result

            # 是否时堵塞模式
            if not block:
                return None

            order_result = self.wait_order_FILLED(
                instId=instId,
                ordId=ordId,
                timeout=timeout,
                delay=delay,
            )
            information['get_order_result'] = order_result
            information['state'] = order_result['data']['state']

            if order_result['data']['state'] == self.ORDER_STATUS.FILLED:
                # [SUC RETURN]
                return None
            if cancel:
                # 订单取消失败
                cancel_order_result = self.cancel_order(instId=instId, ordId=ordId)
                information['cancel_result'] = cancel_order_result
                # [ERROR RETURN]
                if cancel_order_result['code'] != '0':
                    return cancel_order_result
                # 查看订单结果
                get_order_result = self.get_order(
                    instId=instId, ordId=ordId
                )
                if get_order_result['code'] != '0':
                    return get_order_result
                information['get_order_result'] = get_order_result
                information['state'] = get_order_result['data']['state']
            return None

        main_data = dict(
            instId=instId,
            tdMode=tdMode,
            posSide=posSide,
            closePrice=closePrice,
            tpRate=tpRate,
            quantityCT=quantityCT,
            clOrdId=clOrdId,
            tag=tag,
            block=block,
            timeout=timeout,
            delay=delay,
            cancel=cancel,
        )

        def inner_func():
            try:
                error_result = main_func(**main_data)
                information['error_result'] = error_result
            except:
                error_msg = str(traceback.format_exc())
                error_result = {
                    'code': code.FUNC_EXCEPTION[0],
                    'data': {},
                    'msg': error_msg,
                }
                information['error_result'] = error_result

            if information['error_result']:
                if errorback:
                    errorback(information)
            else:
                if callback:
                    callback(information)
            return information

        if newThread == False:
            return inner_func()
        else:
            t = Thread(target=inner_func)
            t.start()
            return t

    # 市价单平仓
    def close_market(
            self,
            instId: str,
            tdMode: str,
            posSide: str,
            quantityCT: Union[int, float, str, origin_float, origin_int] = 'all',
            meta: dict = {},
            timeout: Union[int, float] = 60,
            delay: Union[int, float] = 0.2,
            cancel: bool = True,
            clOrdId: str = '',
            tag: str = '',
            newThread: bool = False,
            callback: object = None,
            errorback: object = None,
    ) -> dict:
        '''
        :param instId: 产品ID
        :param tdMode: 持仓方式
            isolated：逐仓 cross：全仓
        :param posSide: 持仓方向
            long：多单 short：空单
        :param quantityCT: 平仓数量
            注意：
                1. quantityCT是合约张数，并不是货币数量
                2. quantityCT = 'all' 表示持仓的全部张数
        :param meta: 回调函数传递参数
        :param timeout: 订单超时时间 （秒)
        :param delay: 检测订单状态的间隔 (秒)
        :param cancel: 未完全成交是否取消订单
        :param clOrdId: 客户自定义订单ID
            字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间
        :param tag: 订单标签
            字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间
        :param newThread: 是否开启新线程执行
        :param callback: 非执行异常的回调函数
        :param errorback: 执行异常的回调函数
        '''
        # 常量参数
        ORDTYPE = 'market'

        # 记录信息
        information = {
            'instType': 'SWAP',
            'instId': instId,
            'state': None,
            'ordId': None,
            'meta': meta,
            'request_param': None,
            'func_param': None,
            'get_order_result': None,
            'set_order_result': None,
            'error_result': None,
            'cancel_result': None,
        }

        # 函数的参数
        information['func_param'] = dict(
            instId=instId,
            tdMode=tdMode,
            posSide=posSide,
            quantityCT=quantityCT,
            meta=meta,
            timeout=timeout,
            delay=delay,
            cancel=cancel,
            clOrdId=clOrdId,
            tag=tag,
            newThread=newThread,
            callback=callback,
            errorback=errorback,
        )

        # meta
        information['meta'] = meta

        def main_func(
                instId=instId,
                tdMode=tdMode,
                posSide=posSide,
                quantityCT=quantityCT,
                clOrdId=clOrdId,
                tag=tag,
                timeout=timeout,
                delay=delay,
                cancel=cancel,
        ):
            # 验证posSide
            if posSide not in ['long', 'short']:
                msg = 'posSide must in ["long","short"].'
                raise exception.ParamException(msg)
            # 验证tdMode
            if tdMode not in ['isolated', 'cross']:
                msg = 'tdMode must in ["isolated","cross"].'
                raise exception.ParamException(msg)
            # 设置sell
            if posSide == 'long':
                side = 'sell'  # 卖出平多
            else:
                side = 'buy'  # 买入平空
            # 【平仓数量】 quantityCT quantityCT_f
            # 全部
            if quantityCT == 'all':
                positionMap_result = self._account.get_positionsMap()
                # [ERROR RETURN]
                if positionMap_result['code'] != '0':
                    return positionMap_result
                availPos = positionMap_result['data'][tdMode][posSide][instId]['availPos']
                availPos = origin_float(availPos)
                quantityCT = availPos
                quantityCT_f = availPos.origin()
            # 数值字符串
            elif isinstance(quantityCT, str):
                quantityCT_f = quantityCT
                quantityCT = float(quantityCT)
            # 数值
            else:
                # 圆整 -> quantityCT
                round_quantity_result = self.round_quantity(
                    quantity=quantityCT, instId=instId,
                    ordType='market',
                )
                # [ERROR RETURN]
                if round_quantity_result['code'] != '0':
                    return round_quantity_result
                quantityCT = round_quantity_result['data']
                # 转化为字符串 -> quantityCT_f
                quantity_f_result = self.quantity_to_f(
                    quantity=quantityCT,
                    instId=instId,
                )
                # [ERROR RETURN]
                if quantity_f_result['code'] != '0':
                    return quantity_f_result
                quantityCT_f = quantity_f_result['data']
            # API下单请求参数
            request_param = dict(
                instId=instId,
                tdMode=tdMode,
                posSide=posSide,
                side=side,
                ordType=ORDTYPE,
                sz=quantityCT_f,
                clOrdId=clOrdId,
                tag=tag,
            )
            information['request_param'] = request_param
            set_order_result = self.set_order(**request_param)
            information['set_order_result'] = set_order_result
            ordId = set_order_result['data']['ordId']
            information['ordId'] = ordId
            # [ERROR RETURN]
            if set_order_result['code'] != '0':
                return set_order_result

            order_result = self.wait_order_FILLED(
                instId=instId,
                ordId=ordId,
                timeout=timeout,
                delay=delay,
            )

            information['get_order_result'] = order_result
            information['state'] = order_result['data']['state']

            if order_result['data']['state'] == self.ORDER_STATUS.FILLED:
                # [SUC RETURN]
                return None
            if cancel:
                cancel_order_result = self.cancel_order(
                    instId=instId, ordId=ordId,
                )
                information['cancel_result'] = cancel_order_result
                # [ERROR RETURN]
                if cancel_order_result['code'] != '0':
                    return cancel_order_result
                # 查看订单结果
                get_order_result = self.get_order(instId=instId, ordId=ordId)
                if get_order_result['code'] != '0':
                    return get_order_result
                information['get_order_result'] = get_order_result
                information['state'] = get_order_result['data']['state']
            return None

        main_data = dict(
            instId=instId,
            tdMode=tdMode,
            posSide=posSide,
            quantityCT=quantityCT,
            clOrdId=clOrdId,
            tag=tag,
            timeout=timeout,
            delay=delay,
            cancel=cancel,
        )

        def inner_func():
            try:
                error_result = main_func(**main_data)
                information['error_result'] = error_result
            except:
                error_msg = str(traceback.format_exc())
                error_result = {
                    'code': code.FUNC_EXCEPTION[0],
                    'data': {},
                    'msg': error_msg,
                }
                information['error_result'] = error_result

            if information['error_result']:
                if errorback:
                    errorback(information)
            else:
                if callback:
                    callback(information)
            return information

        if newThread == False:
            return inner_func()
        else:
            t = Thread(target=inner_func)
            t.start()
            return t

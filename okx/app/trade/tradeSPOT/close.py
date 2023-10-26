from typing import Union
import traceback
from threading import Thread
from paux.digit import origin_float, origin_int
from okx.app import code
from okx.app import exception
from okx.app.trade.tradeSPOT.order import TradeOrder
from okx.app.trade.tradeSPOT.quantity_and_price import TradeQuantityAndPrice


class TradeClose(TradeOrder, TradeQuantityAndPrice):
    # 限价单平仓
    def close_limit(
            self,
            instId: str,
            closePrice: Union[int, float, str, origin_float, origin_int, None] = None,
            tpRate: Union[int, float, None] = None,
            quantity: Union[int, float, str, origin_float, origin_int] = 'all',
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
        :param closePrice: 平仓价格
        :param tpRate: 挂单止盈率
            注意：
                1. closePrice 和 tpRate必须填写其中一个
                2. closePrice 和 tpRate的优先级 closePrice > tpRate
                3. 当closePrice为空，tpRate = askPrice * (1 + abs(tpRate))
        :param quantity: 平仓数量
            注意：
                1. quantity是货币数量
                2. quantity = 'all' instId可用现货全部平仓
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
        SIDE = 'sell'
        TDMODE = 'cash'

        # 记录信息
        information = {
            'instType': 'SPOT',
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
            closePrice=closePrice,
            tpRate=tpRate,
            quantity=quantity,
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

        def main_func(
                instId=instId,
                closePrice=closePrice,
                tpRate=tpRate,
                quantity=quantity,
                clOrdId=clOrdId,
                tag=tag,
                block=block,
                timeout=timeout,
                delay=delay,
                cancel=cancel,
        ):
            # closePrice和tpLine不能同时为空
            if closePrice in [None, ''] and tpRate in [None, '']:
                msg = 'closePrice and tpRate can not be empty together'
                raise exception.ParamException(msg)
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
                    askPx = get_ticker_result['data']['askPx']
                    askPx = float(askPx)
                    closePrice = askPx * (1 + abs(tpRate))
                # 圆整 -> closePrice
                # 价格向上圆整
                round_price_result = self.round_price(
                    price=closePrice,
                    instId=instId,
                    type='CEIL',
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
            if quantity == 'all':
                get_balance_result = self._account.get_balance(instId=instId)
                # [ERROR RETURN]
                if get_balance_result['code'] != '0':
                    return get_balance_result
                availBal = get_balance_result['data']['details']['availBal']  # 可用余额
                quantity = origin_float(availBal)
                quantity_f = quantity.origin()
            # 数值字符串
            elif isinstance(quantity, str):
                quantity_f = quantity
                quantity = float(quantity)
            # origin
            elif isinstance(quantity, origin_float) or isinstance(quantity, origin_int):
                quantity_f = quantity.origin()
            # 数字对象 圆整 转化为字符串
            else:
                round_quantity_result = self.round_quantity(
                    quantity=quantity, instId=instId,
                    ordType=ORDTYPE,
                )
                # [ERROR RETURN]
                if round_quantity_result['code'] != '0':
                    return round_quantity_result
                quantity = round_quantity_result['data']
                quantity_to_f_result = self.quantity_to_f(
                    quantity=quantity, instId=instId,
                )
                # [ERROR RETURN]
                if quantity_to_f_result['code'] != '0':
                    return quantity_to_f_result
                quantity_f = quantity_to_f_result['data']

            request_param = dict(
                instId=instId,
                tdMode=TDMODE,
                side=SIDE,
                ordType=ORDTYPE,
                sz=quantity_f,
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
                cancel_order_result = self.cancel_order(instId=instId, ordId=ordId)
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
            closePrice=closePrice,
            tpRate=tpRate,
            quantity=quantity,
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
            quantity: Union[int, float, str, origin_float, origin_int] = 'all',
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
        :param quantity: 平仓数量
            注意：
                1. quantity是货币数量
                2. quantity = 'all' instId可用现货全部平仓
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
        SIDE = 'sell'
        TDMODE = 'cash'

        # 记录信息
        information = {
            'instType': 'SPOT',
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
            quantity=quantity,
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


        def main_func(
                instId=instId,
                quantity=quantity,
                clOrdId=clOrdId,
                tag=tag,
                timeout=timeout,
                delay=delay,
                cancel=cancel,
        ):
            # 【平仓数量】 quantity quantity_f
            # 全部
            if quantity == 'all':
                get_balance_result = self._account.get_balance(instId=instId)
                # [ERROR RETURN]
                if get_balance_result['code'] != '0':
                    return get_balance_result

                availBal = get_balance_result['data']['details']['availBal']  # 可用余额
                quantity = origin_float(availBal)
                quantity_f = quantity.origin()

            # 数值字符串
            elif isinstance(quantity, str):
                quantity_f = quantity
                quantity = float(quantity)
            # 数值
            else:
                # 圆整 -> quantity
                round_quantity_result = self.round_quantity(
                    quantity=quantity, instId=instId,
                    ordType='market',
                )
                # [ERROR RETURN]
                if round_quantity_result['code'] != '0':
                    return round_quantity_result
                quantity = round_quantity_result['data']
                # 转化为字符串 -> quantity_f
                quantity_f_result = self.quantity_to_f(
                    quantity=quantity,
                    instId=instId,
                )
                # [ERROR RETURN]
                if quantity_f_result['code'] != '0':
                    return quantity_f_result
                quantity_f = quantity_f_result['data']

            request_param = dict(
                instId=instId,
                tdMode=TDMODE,
                side=SIDE,
                ordType=ORDTYPE,
                sz=quantity_f,
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
            quantity=quantity,
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

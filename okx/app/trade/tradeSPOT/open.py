from typing import Union
import traceback
from threading import Thread
from paux.digit import origin_float, origin_int
from okx.app import code
from okx.app import exception
from okx.app.trade.tradeSPOT.order import TradeOrder
from okx.app.trade.tradeSPOT.quantity_and_price import TradeQuantityAndPrice


class TradeOpen(TradeOrder, TradeQuantityAndPrice):

    # 限价单购买 Weight > 1
    def open_limit(
            self,
            instId: str,
            openPrice: Union[int, float, str, origin_float, origin_int],
            openMoney: Union[int, float, None] = None,
            quantity: Union[int, float, str, origin_float, origin_int, None] = None,
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
        :param instId: 产品
        :param openPrice: 开仓价格
        :param openMoney: 开仓金额
        :param quantity: 下单数量
            注意：
                1. quantity是货币数量
                2. openMoney 和 quantity必须填写其中一个
                3. 当openMoney 和 quantity同时填写，优先级 quantityCT > openMoney
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
        SIDE = 'buy'
        TDMODE = 'cash'
        LEVERAGE = 1  # 现货交易视为1倍杠杆

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
            openPrice=openPrice,
            openMoney=openMoney,
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
                openPrice=openPrice,
                openMoney=openMoney,
                quantity=quantity,
                clOrdId=clOrdId,
                tag=tag,
                block=block,
                timeout=timeout,
                delay=delay,
                cancel=cancel,
        ):
            # 【开仓价格】 -> openPrice openPrice_f
            # 字符串
            if isinstance(openPrice, str):
                openPrice_f = openPrice
                openPrice = float(openPrice)
            # origin
            elif isinstance(openPrice, origin_float) or isinstance(openPrice, origin_int):
                openPrice_f = openPrice.origin()
                openPrice = openPrice
            # 数字对象
            else:
                # 圆整 -> openPrice
                round_price_result = self.round_price(
                    price=openPrice,
                    instId=instId,
                    type='FLOOR',
                )
                # [ERROR RETURN]
                if round_price_result['code'] != '0':
                    return round_price_result
                # 转化为字符串 -> openPrice_f
                openPrice = round_price_result['data']
                openPrice_f_result = self.price_to_f(price=openPrice, instId=instId)
                # [ERROR RETURN]
                if openPrice_f_result['code'] != '0':
                    return openPrice_f_result
                openPrice_f = openPrice_f_result['data']
            # 【开仓数量】 quantity quantity_f
            # 字符串
            if isinstance(quantity, str):
                quantity_f = quantity
                quantity = float(quantity)
            # origin
            elif isinstance(quantity, origin_float) or isinstance(quantity, origin_int):
                quantity_f = quantity.origin()
            # 数字对象和None
            else:
                # None 通过openMoney获取quantity
                if quantity == None:
                    get_quantity_result = self.get_quantity(
                        openPrice=openPrice, openMoney=openMoney,
                        instId=instId, ordType=ORDTYPE,
                        leverage=LEVERAGE,
                    )

                    # [ERROR RETURN]
                    if get_quantity_result['code'] != '0':
                        return get_quantity_result
                    quantity = get_quantity_result['data']
                # 数字对象 圆整quantity
                else:
                    round_quantity_result = self.round_quantity(
                        quantity=quantity,
                        instId=instId,
                        ordType=ORDTYPE,
                    )
                    # [ERROR RETURN]
                    if round_quantity_result['code'] != '0':
                        return round_quantity_result
                    quantity = round_quantity_result['data']
                # 转化为字符串 -> quantity_f
                quantity_f_result = self.quantity_to_f(quantity=quantity, instId=instId)
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
                px=openPrice_f,
            )
            information['request_param'] = request_param
            set_order_result = self.set_order(**request_param)  # 下单
            information['set_order_result'] = set_order_result
            # [ERROR RETURN]
            if set_order_result['code'] != '0':
                return set_order_result
            # ordId
            ordId = set_order_result['data']['ordId']
            information['ordId'] = ordId
            # 是否时堵塞模式
            if not block:
                return None
            # 只有堵塞模式才查询订单 并 更新订单状态
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
                cancel_order_result = self.cancel_order(
                    instId=instId, ordId=ordId,
                )
                information['cancel_result'] = cancel_order_result
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
            openPrice=openPrice,
            openMoney=openMoney,
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

    # 市价单购买 Weight > 1
    def open_market(
            self,
            instId: str,
            openMoney: Union[int, float, None] = None,
            quantity: Union[int, float, str, origin_float, origin_int] = None,
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
        :param openMoney: 开仓金额
        :param quantity: 下单数量
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
        SIDE = 'buy'
        TDMODE = 'cash'
        # 官方解释：市价单委托数量sz的单位，仅适用于币币市价订单 base_ccy: 交易货币 ；quote_ccy：计价货币 买单默认quote_ccy， 卖单默认base_ccy
        # 使用base_ccy
        TGTCCY = 'base_ccy'
        LEVERAGE = 1

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

        # 函数参数
        information['func_param'] = dict(
            instId=instId,
            openMoney=openMoney,
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
                openMoney=openMoney,
                quantity=quantity,
                clOrdId=clOrdId,
                tag=tag,
                timeout=timeout,
                delay=delay,
                cancel=cancel,
        ):
            if quantity == None and openMoney == None:
                msg = 'quantity and openMoney can not be empty together.'
                raise exception.ParamException(msg)

            get_ticker_result = self._market.get_ticker(instId=instId)
            # [ERROR RETURN]
            if get_ticker_result['code'] != '0':
                return get_ticker_result
            openPrice = origin_float(get_ticker_result['data']['askPx'])
            '''
            # 通过交易货币数量算计价货币数量
            if quantity != None:
                openMoney = float(quantity) * openPrice  # 圆整之前
            else:
                openMoney = openMoney  # int | float

            round_quantity_result = self.round_quantity(
                quantity=openMoney,  # 币币购买，quantity为购买金额
                instId=instId,
                ordType=ORDTYPE,
            )
            if round_quantity_result['code'] != '0':
                return round_quantity_result
            
            openMoney = round_quantity_result['data']  # openMoney 圆整之后
            quantity_to_f_result = self.quantity_to_f(
                quantity=openMoney,
                instId=instId,
            )
            if quantity_to_f_result['code'] != '0':
                return quantity_to_f_result
            quantity_f = quantity_to_f_result['data']  # openMoney转换为字符串
            '''
            # 【开仓数量】 quantity quantity_f
            # 字符串
            if isinstance(quantity, str):
                quantity_f = quantity
                quantity = float(quantity)
            # origin
            elif isinstance(quantity, origin_float) or isinstance(quantity, origin_int):
                quantity_f = quantity.origin()
            # 数字对象和None
            else:
                # None 通过openMoney获取quantity
                if quantity == None:
                    get_quantity_result = self.get_quantity(
                        openPrice=openPrice, openMoney=openMoney,
                        instId=instId, ordType=ORDTYPE,
                        leverage=LEVERAGE,
                    )

                    # [ERROR RETURN]
                    if get_quantity_result['code'] != '0':
                        return get_quantity_result
                    quantity = get_quantity_result['data']
                # 数字对象 圆整quantity
                else:
                    round_quantity_result = self.round_quantity(
                        quantity=quantity,
                        instId=instId,
                        ordType=ORDTYPE,
                    )
                    # [ERROR RETURN]
                    if round_quantity_result['code'] != '0':
                        return round_quantity_result
                    quantity = round_quantity_result['data']
                # 转化为字符串 -> quantity_f
                quantity_f_result = self.quantity_to_f(quantity=quantity, instId=instId)
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
                tgtCcy = TGTCCY,
            )

            # 购买
            information['request_param'] = request_param
            set_order_result = self.set_order(**request_param)
            information['set_order_result'] = set_order_result

            # [ERROR RETURN]
            if set_order_result['code'] != '0':
                return set_order_result

            ordId = set_order_result['data']['ordId']
            information['ordId'] = ordId
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
            openMoney=openMoney,
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

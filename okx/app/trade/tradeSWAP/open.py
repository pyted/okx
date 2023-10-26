import traceback
from typing import Union
from threading import Thread
from paux.digit import origin_float, origin_int
from okx.app import code
from okx.app import exception
from okx.app.trade.tradeSWAP.order import TradeOrder
from okx.app.trade.tradeSWAP.quantity_and_price import TradeQuantityAndPrice


class TradeOpen(TradeOrder, TradeQuantityAndPrice):

    # 限价单开仓
    def open_limit(
            self,
            instId: str,
            openPrice: Union[int, float, str, origin_float, origin_int],
            tdMode: str,
            posSide: str,
            lever: int,
            openMoney: Union[int, float, None] = None,
            quantityCT: Union[int, float, str, origin_float, origin_int, None] = None,
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
        :param openPrice: 开仓价格
        :param tdMode: 持仓方式
            isolated：逐仓 cross：全仓
        :param posSide: 持仓方向
            long：多单 short：空单
        :param lever: 杠杆
        :param openMoney: 开仓金额
        :param quantityCT: 开仓数量
            注意：
                1. quantityCT是合约张数，并不是货币数量
                2. openMoney 和 quantityCT必须填写其中一个
                3. 当openMoney 和 quantityCT同时填写，优先级 quantityCT > openMoney
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
        ORDTYPE = 'limit'  # 订单类型 限价单

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
            lever=lever,
            openPrice=openPrice,
            openMoney=openMoney,
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
        # 主函数
        def main_func(
                instId=instId,
                tdMode=tdMode,
                posSide=posSide,
                lever=lever,
                openPrice=openPrice,
                openMoney=openMoney,
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
            # 设置side
            if posSide == 'long':
                side = 'buy'  # 买入开多
            else:
                side = 'sell'  # 卖出开空
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
                    # 多单开仓价格向下取 空单开仓价格向上取
                    type='FLOOR' if posSide == 'long' else 'CEIL',
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
            # 【开仓数量】 quantityCT quantityCT_f
            # 字符串
            if isinstance(quantityCT, str):
                quantityCT_f = quantityCT
                quantityCT = float(quantityCT)
            # origin
            elif isinstance(quantityCT, origin_float) or isinstance(quantityCT, origin_int):
                quantityCT_f = quantityCT.origin()
            # 数字对象和None
            else:
                # None 通过openMoney获取quantityCT
                if quantityCT == None:
                    get_quantity_result = self.get_quantity(
                        openPrice=openPrice, openMoney=openMoney,
                        instId=instId, ordType=ORDTYPE,
                        leverage=lever,
                    )
                    # [ERROR RETURN]
                    if get_quantity_result['code'] != '0':
                        return get_quantity_result
                    quantityCT = get_quantity_result['data']
                # 数字对象 圆整quantityCT
                else:
                    round_quantity_result = self.round_quantity(
                        quantity=quantityCT,
                        instId=instId,
                        ordType=ORDTYPE,
                    )
                    # [ERROR RETURN]
                    if round_quantity_result['code'] != '0':
                        return round_quantity_result
                    quantityCT = round_quantity_result['data']
                # 转化为字符串 -> quantity_f
                quantity_f_result = self.quantity_to_f(
                    quantity=quantityCT, instId=instId
                )
                # [ERROR RETURN]
                if quantity_f_result['code'] != '0':
                    return quantity_f_result
                quantityCT_f = quantity_f_result['data']
            # 获取杠杆
            get_leverage_result = self._account.get_leverage(
                instId=instId,
                mgnMode=tdMode
            )
            if get_leverage_result['code'] != '0':
                return get_leverage_result
            # 当前杠杆
            this_lever = int(get_leverage_result['data'][posSide]['lever'])
            # 当前杠杆不等于开仓杠杆
            if this_lever != int(lever):
                # 设置杠杆
                set_leverage_result = self._account.set_leverage(
                    lever=lever,
                    mgnMode=tdMode,
                    instId=instId,
                    posSide=posSide if tdMode == 'isolated' else ''  # 全仓不指定posSide
                )
                if set_leverage_result['code'] != '0':
                    return set_leverage_result
            # API请求参数
            request_param = dict(
                instId=instId,
                tdMode=tdMode,
                posSide=posSide,
                side=side,
                ordType=ORDTYPE,
                sz=quantityCT_f,
                clOrdId=clOrdId,
                tag=tag,
                px=openPrice_f,
            )
            information['request_param'] = request_param
            set_order_result = self.set_order(**request_param)  # 下单
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
                # 取消订单
                cancel_order_result = self.cancel_order(
                    instId=instId, ordId=ordId,
                )
                information['cancel_result'] = cancel_order_result
                # 订单取消失败
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
            lever=lever,
            openPrice=openPrice,
            openMoney=openMoney,
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

    # 市价单开仓
    def open_market(
            self,
            instId: str,
            tdMode: str,
            posSide: str,
            lever: int,
            openMoney: Union[int, float, None] = None,
            quantityCT: Union[int, float, str, origin_float, origin_int] = None,
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
        :param lever: 杠杆
        :param openMoney: 开仓金额
        :param quantityCT: 开仓数量
            注意：
                1. quantityCT是合约张数，并不是货币数量
                2. openMoney 和 quantityCT必须填写其中一个
                3. 当openMoney 和 quantityCT同时填写，优先级 quantityCT > openMoney
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

        ORDTYPE = 'market'  # 订单类型 市价单

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

        # 函数参数
        information['func_param'] = dict(
            instId=instId,
            tdMode=tdMode,
            posSide=posSide,
            lever=lever,
            openMoney=openMoney,
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
                lever=lever,
                openMoney=openMoney,
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
            # 设置side
            if posSide == 'long':
                side = 'buy'  # 买入开多
            else:
                side = 'sell'  # 卖出开空
            # 【开仓数量】 quantityCT quantityCT_f
            # 字符串
            if isinstance(quantityCT, str):
                quantityCT_f = quantityCT
                quantityCT = float(quantityCT)
            # origin
            elif isinstance(quantityCT, origin_float) or isinstance(quantityCT, origin_int):
                quantityCT_f = quantityCT.origin()
                quantityCT = quantityCT
            # 数字对象和None
            else:
                # None 按照最优购买价格 计算下单数量
                if quantityCT == None:
                    get_ticker_result = self._market.get_ticker(instId=instId)
                    # [ERROR RETURN]
                    if get_ticker_result['code'] != '0':
                        return get_ticker_result

                    # posSide = 'long' 使用卖出价格
                    if posSide == 'long':
                        askPx = get_ticker_result['data']['askPx']
                        openPrice = origin_float(askPx)
                    # posSide = 'short' 使用买入价格
                    else:
                        bidPx = get_ticker_result['data']['bidPx']
                        openPrice = origin_float(bidPx)
                    get_quantity_result = self.get_quantity(
                        openPrice=openPrice, openMoney=openMoney,
                        instId=instId, ordType=ORDTYPE,
                        leverage=lever,
                    )
                    # [ERROR RETURN]
                    if get_quantity_result['code'] != '0':
                        return get_quantity_result
                    quantityCT = get_quantity_result['data']
                # 数字对象 圆整下单数量
                else:
                    round_quantity_result = self.round_quantity(
                        quantity=quantityCT,
                        instId=instId,
                        ordType=ORDTYPE,
                    )
                    # [ERROR RETURN]
                    if round_quantity_result['code'] != '0':
                        return round_quantity_result
                    quantityCT = round_quantity_result['data']
                # 下单数量转化为字符串
                quantity_f_result = self.quantity_to_f(quantity=quantityCT, instId=instId)
                # [ERROR RETURN]
                if quantity_f_result['code'] != '0':
                    return quantity_f_result
                quantityCT_f = quantity_f_result['data']
            # 获取杠杆
            get_leverage_result = self._account.get_leverage(
                instId=instId,
                mgnMode=tdMode
            )
            if get_leverage_result['code'] != '0':
                return get_leverage_result
            # 当前杠杆
            this_lever = int(get_leverage_result['data'][posSide]['lever'])
            # 当前杠杆不等于开仓杠杆
            if this_lever != int(lever):
                # 设置杠杆
                set_leverage_result = self._account.set_leverage(
                    lever=lever,
                    mgnMode=tdMode,
                    instId=instId,
                    posSide=posSide if tdMode == 'isolated' else ''  # 全仓不指定posSide
                )
                if set_leverage_result['code'] != '0':
                    return set_leverage_result
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
            # 购买
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
            tdMode=tdMode,
            posSide=posSide,
            lever=lever,
            openMoney=openMoney,
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

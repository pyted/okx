import time
from okx.app.trade.tradeSWAP._base import TradeBase
from paux.param import to_local
from okx.app import exception


class TradeOrder(TradeBase):
    # 订单状态
    class ORDER_STATUS():
        CANCELED = 'canceled'  # 撤单成功
        LIVE = 'live'  # 等待成交
        PARTIALLY_FILLED = 'partially_filled'  # 部分成交
        FILLED = 'filled'  # 完全成交

    # 下单
    def set_order(
            self,
            instId: str,
            tdMode: str,
            side: str,
            ordType: str,
            sz: str,
            ccy: str = '',
            clOrdId: str = '',
            tag: str = '',
            posSide: str = '',
            px: str = '',
            reduceOnly: bool = '',
            tgtCcy: str = '',
            banAmend: bool = '',
            tpTriggerPx: str = '',
            tpOrdPx: str = '',
            slTriggerPx: str = '',
            slOrdPx: str = '',
            tpTriggerPxType: str = '',
            slTriggerPxType: str = '',
            quickMgnType: str = ''
    ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-place-order

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-190927-5000-C
        tdMode            	String  	是       	交易模式保证金模式：isolated：逐仓 ；cross：全仓非保证金模式：cash：非保证金
        side              	String  	是       	订单方向buy：买，sell：卖
        ordType           	String  	是       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）
        sz                	String  	是       	委托数量
        ccy               	String  	否       	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        clOrdId           	String  	否       	客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        posSide           	String  	可选      	持仓方向在双向持仓模式下必填，且仅可选择long或short。 仅适用交割、永续。
        px                	String  	可选      	委托价格，仅适用于limit、post_only、fok、ioc类型的订单
        reduceOnly        	Boolean 	否       	是否只减仓，true或false，默认false仅适用于币币杠杆，以及买卖模式下的交割/永续仅适用于单币种保证金模式和跨币种保证金模式
        tgtCcy            	String  	否       	市价单委托数量sz的单位，仅适用于币币市价订单base_ccy: 交易货币 ；quote_ccy：计价货币买单默认quote_ccy， 卖单默认base_ccy
        banAmend          	Boolean 	否       	是否禁止币币市价改单，true 或 false，默认false为true时，余额不足时，系统不会改单，下单会失败，仅适用于币币市价单
        tpTriggerPx       	String  	否       	止盈触发价，如果填写此参数，必须填写 止盈委托价
        tpOrdPx           	String  	否       	止盈委托价，如果填写此参数，必须填写 止盈触发价委托价格为-1时，执行市价止盈
        slTriggerPx       	String  	否       	止损触发价，如果填写此参数，必须填写 止损委托价
        slOrdPx           	String  	否       	止损委托价，如果填写此参数，必须填写 止损触发价委托价格为-1时，执行市价止损
        tpTriggerPxType   	String  	否       	止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        slTriggerPxType   	String  	否       	止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        quickMgnType      	String  	否       	一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动
        '''
        result = self.api.set_order(**to_local(locals()))
        if result['code'] != '0':
            return result
        result['data'] = result['data'][0]
        return result

    # 获取订单信息
    def get_order(
            self,
            instId: str,
            ordId: str = '',
            clOrdId: str = ''
    ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-order-details

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID ，如BTC-USD-190927
        ordId             	String  	可选      	订单ID ，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID
        '''
        result = self.api.get_order(**to_local(locals()))
        if result['code'] != '0':
            return result
        result['data'] = result['data'][0]
        return result

    # 获取未成交订单列表
    def get_orders_pending(
            self,
            uly: str = '',
            instFamily: str = '',
            instId: str = '',
            ordType: str = '',
            state: str = '',
            after: str = '',
            before: str = '',
            limit: str = '',
    ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-order-list

        请求参数：
        Parameter         	Type    	Required	Description
        uly               	String  	否       	标的指数
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品ID，如BTC-USD-200927
        ordType           	String  	否       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）
        state             	String  	否       	订单状态live：等待成交partially_filled：部分成交
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        # 产品类型
        instType = 'SWAP'
        return self.api.get_orders_pending(**to_local(locals()))

    # 获取未成交的开仓订单列表
    def get_orders_pending_open(
            self,
            posSide='',
            uly: str = '',
            instFamily: str = '',
            instId: str = '',
            ordType: str = '',
            state: str = '',
            after: str = '',
            before: str = '',
            limit: str = '',
    ):
        '''
        :param posSide: 持仓方向
            posSide = 'long'    多单
            posSide = 'short'   空单
            posSide = ''        全部
        '''
        # 验证posSide
        if posSide not in ['long', 'short', '']:
            msg = 'posSide must in ["long","short",""].'
            raise exception.ParamException(msg)
        # 通过posSide选择side
        if posSide == 'long':  # 买入开多
            side = 'buy'
        elif posSide == 'short':  # 卖出开空
            side = 'sell'
        else:
            side = None
        # 获取未成交订单列表
        result = self.get_orders_pending(
            uly=uly,
            instFamily=instFamily,
            instId=instId,
            ordType=ordType,
            state=state,
            after=after,
            before=before,
            limit=limit,
        )
        # [ERROR RETURN]
        if result['code'] != '0':
            return result
        # 按照posSide与side筛选
        datas_open = []
        for data in result['data']:
            if posSide:
                if data['posSide'] == posSide and data['side'] == side:
                    datas_open.append(data)
            else:
                if (
                        # 买入开多
                        ((data['posSide'] == 'long') and (data['side'] == 'buy')) or
                        # 卖出开空
                        ((data['posSide'] == 'short') and (data['side'] == 'sell'))
                ):
                    datas_open.append(data)

        result['data'] = datas_open
        return result

    # 获取未成交的平仓订单列表
    def get_orders_pending_close(
            self,
            posSide='',
            uly: str = '',
            instFamily: str = '',
            instId: str = '',
            ordType: str = '',
            state: str = '',
            after: str = '',
            before: str = '',
            limit: str = '',
    ):
        '''
        :param posSide: 持仓方向
            posSide = 'long'    多单
            posSide = 'short'   空单
            posSide = ''        全部
        '''
        # 验证posSide
        if posSide not in ['long', 'short', '']:
            msg = 'posSide must in ["long","short",""].'
            raise exception.ParamException(msg)
        # 通过posSide选择side
        if posSide == 'long':  # 卖出平多
            side = 'sell'
        elif posSide == 'short':  # 买入平空
            side = 'buy'
        else:
            side = None
        # 获取未成交订单列表
        result = self.get_orders_pending(
            uly=uly,
            instFamily=instFamily,
            instId=instId,
            ordType=ordType,
            state=state,
            after=after,
            before=before,
            limit=limit,
        )
        # [ERROR RETURN]
        if result['code'] != '0':
            return result
        # 按照posSide与side筛选
        datas_open = []
        for data in result['data']:
            if posSide:
                if data['posSide'] == posSide and data['side'] == side:
                    datas_open.append(data)
            else:
                if (
                        # 卖出平多
                        ((data['posSide'] == 'long') and (data['side'] == 'sell')) or
                        # 买入平空
                        ((data['posSide'] == 'short') and (data['side'] == 'buy'))
                ):
                    datas_open.append(data)
        result['data'] = datas_open
        return result

    # 撤单
    def cancel_order(
            self,
            instId: str,
            ordId: str = '',
            clOrdId: str = ''
    ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-cancel-order

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-190927
        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID
        '''
        result = self.api.set_cancel_order(**to_local(locals()))
        if result['code'] != '0':
            return result
        result['data'] = result['data'][0]
        return result

    # 等待订单成交
    def wait_order_FILLED(
            self,
            instId: str,
            ordId: str = '',
            clOrdId: str = '',
            timeout=60,
            delay=0.2
    ):
        '''
        :param instId: 产品ID
        :param ordId: 订单ID
        :param clOrdId: 客户自定义订单ID
        :param timeout: 超时时间（秒）
        :param delay: 检查订单状态间隔时间（秒）
        :return 订单状态
        '''
        start_time = time.time()
        while True:
            # 查询订单
            order_result = self.get_order(
                instId=instId,
                ordId=ordId,
                clOrdId=clOrdId,
            )
            # [ERROR_RETURN] code异常
            if order_result['code'] != '0':
                return order_result
            # [SUCCESS_RETURN] 全部成交
            if order_result['data']['state'] == self.ORDER_STATUS.FILLED:
                return order_result
            # [TIMEOUT_RETURN] 超时
            if time.time() - start_time >= timeout:
                return order_result
            time.sleep(delay)

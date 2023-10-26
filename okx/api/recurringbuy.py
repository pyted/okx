'''
定投
https://www.okx.com/docs-v5/zh/#order-book-trading-recurring-buy
'''
from paux.param import to_local
from okx.api._client import Client


class _RecurringBuyEndpoints():
    set_order_algo = ['/api/v5/tradingBot/recurring/order-algo', 'POST']  # POST / 定投策略委托下单
    set_amend_order_algo = ['/api/v5/tradingBot/recurring/amend-order-algo', 'POST']  # POST / 修改定投策略订单
    set_stop_order_algo = ['/api/v5/tradingBot/recurring/stop-order-algo', 'POST']  # POST / 定投策略停止
    get_orders_algo_pending = ['/api/v5/tradingBot/recurring/orders-algo-pending', 'GET']  # GET / 获取未完成定投策略委托单列表
    get_orders_algo_history = ['/api/v5/tradingBot/recurring/orders-algo-history', 'GET']  # GET / 获取历史定投策略委托单列表
    get_orders_algo_details = ['/api/v5/tradingBot/recurring/orders-algo-details', 'GET']  # GET / 获取定投策略委托订单详情
    get_sub_orders = ['/api/v5/tradingBot/recurring/sub-orders', 'GET']  # GET / 获取定投策略子订单信息


class RecurringBuy(Client):

    # POST / 定投策略委托下单
    def set_order_algo(self, stgyName: str, recurringList: object, period: str, recurringDay: str, recurringTime: str,
                       timeZone: str, amt: str, investmentCcy: str, tdMode: str, algoClOrdId: str = '', tag: str = '',
                       proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/tradingBot/recurring/order-algo
        https://www.okx.com/docs-v5/zh/#order-book-trading-recurring-buy-post-place-recurring-buy-order
        
        限速：20次/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        stgyName          	String  	是       	策略自定义名称，不超过40个字符
        recurringList     	Array of object	是       	定投信息
        > ccy             	String  	是       	定投币种，如BTC
        > ratio           	String  	是       	定投币种资产占比，如 "0.2"代表占比20%
        period            	String  	是       	周期类型每月：monthly每周：weekly每日：daily
        recurringDay      	String  	是       	投资日当周期类型为monthly，则取值范围是 [1,28] 的整数当周期类型为weekly，则取值范围是 [1,7] 的整数当周期类型为daily，则取值为1
        recurringTime     	String  	是       	投资时间，取值范围是 [0,23] 的整数
        timeZone          	String  	是       	时区（UTC），取值范围是 [-12,14] 的整数如8表示UTC+8（东8区），北京时间
        amt               	String  	是       	每期投入数量
        investmentCcy     	String  	是       	投入数量单位，只能是USDT/USDC
        tdMode            	String  	是       	交易模式跨币种/PM保证金模式下选择 全仓：cross简单/单币种模式下选择 非保证金：cash
        algoClOrdId       	String  	否       	客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	客户自定义订单ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        '''
        return self.send_request(*_RecurringBuyEndpoints.set_order_algo, **to_local(locals()))

    # POST / 修改定投策略订单
    def set_amend_order_algo(self, algoId: str, stgyName: str, proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/tradingBot/recurring/amend-order-algo
        https://www.okx.com/docs-v5/zh/#order-book-trading-recurring-buy-post-amend-recurring-buy-order
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        stgyName          	String  	是       	调整后的策略自定义名称
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	客户自定义订单ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        '''
        return self.send_request(*_RecurringBuyEndpoints.set_amend_order_algo, **to_local(locals()))

    # POST / 定投策略停止
    def set_stop_order_algo(self, algoId: str, proxies={}, proxy_host: str = None):
        '''
        每次最多可以撤销10个定投策略订单。
        https://www.okx.com/docs-v5/zh/#order-book-trading-recurring-buy-post-stop-recurring-buy-order
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	客户自定义订单ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        '''
        return self.send_request(*_RecurringBuyEndpoints.set_stop_order_algo, **to_local(locals()))

    # GET / 获取未完成定投策略委托单列表
    def get_orders_algo_pending(self, algoId: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                                proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/recurring/orders-algo-pending
        https://www.okx.com/docs-v5/zh/#order-book-trading-recurring-buy-get-recurring-buy-order-list
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	否       	策略订单ID
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	客户自定义订单ID
        instType          	String  	产品类型SPOT：现货
        cTime             	String  	策略订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	策略订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        algoOrdType       	String  	策略订单类型recurring：定投
        state             	String  	订单状态running：运行中stopping：终止中
        stgyName          	String  	策略自定义名称，不超过40个字符
        recurringList     	Array of object	定投信息
        > ccy             	String  	定投币种，如BTC
        > ratio           	String  	定投币种资产占比，如 "0.2"代表占比20%
        period            	String  	周期类型每月：monthly每周：weekly每日：daily
        recurringDay      	String  	投资日当周期类型为monthly，则取值范围是 [1,28] 的整数当周期类型为weekly，则取值范围是 [1,7] 的整数当周期类型为daily，则取值为1
        recurringTime     	String  	投资时间，取值范围是 [0,23] 的整数
        timeZone          	String  	时区（UTC），取值范围是 [-12,14] 的整数如8表示UTC+8（东8区），北京时间
        amt               	String  	每期投入数量
        investmentAmt     	String  	累计投入数量
        investmentCcy     	String  	投入数量单位，只能是USDT/USDC
        totalPnl          	String  	总收益
        totalAnnRate      	String  	总年化
        pnlRatio          	String  	收益率
        mktCap            	String  	当前总市值，单位为USDT
        cycles            	String  	定投累计轮数
        tag               	String  	订单标签
        '''
        return self.send_request(*_RecurringBuyEndpoints.get_orders_algo_pending, **to_local(locals()))

    # GET / 获取历史定投策略委托单列表
    def get_orders_algo_history(self, algoId: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                                proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/recurring/orders-algo-history
        https://www.okx.com/docs-v5/zh/#order-book-trading-recurring-buy-get-recurring-buy-order-history
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	否       	策略订单ID
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	客户自定义订单ID
        instType          	String  	产品类型SPOT：现货
        cTime             	String  	策略订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	策略订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        algoOrdType       	String  	策略订单类型recurring：定投
        state             	String  	订单状态stopped：已停止
        stgyName          	String  	策略自定义名称，不超过40个字符
        recurringList     	Array of object	定投信息
        > ccy             	String  	定投币种，如BTC
        > ratio           	String  	定投币种资产占比，如 "0.2"代表占比20%
        period            	String  	周期类型每月：monthly每周：weekly每日：daily
        recurringDay      	String  	投资日当周期类型为monthly，则取值范围是 [1,28] 的整数当周期类型为weekly，则取值范围是 [1,7] 的整数当周期类型为daily，则取值为1
        recurringTime     	String  	投资时间，取值范围是 [0,23] 的整数
        timeZone          	String  	时区（UTC），取值范围是 [-12,14] 的整数如8表示UTC+8（东8区），北京时间
        amt               	String  	每期投入数量
        investmentAmt     	String  	累计投入数量
        investmentCcy     	String  	投入数量单位，只能是USDT/USDC
        totalPnl          	String  	总收益
        totalAnnRate      	String  	总年化
        pnlRatio          	String  	收益率
        mktCap            	String  	当前总市值，单位为USDT
        cycles            	String  	定投累计轮数
        tag               	String  	订单标签
        '''
        return self.send_request(*_RecurringBuyEndpoints.get_orders_algo_history, **to_local(locals()))

    # GET / 获取定投策略委托订单详情
    def get_orders_algo_details(self, algoId: str, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/recurring/orders-algo-details
        https://www.okx.com/docs-v5/zh/#order-book-trading-recurring-buy-get-recurring-buy-order-details
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	客户自定义订单ID
        instType          	String  	产品类型SPOT：现货
        cTime             	String  	策略订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	策略订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        algoOrdType       	String  	策略订单类型recurring：定投
        state             	String  	订单状态running：运行中stopping：终止中stopped：已停止
        stgyName          	String  	策略自定义名称，不超过40个字符
        recurringList     	Array of object	定投信息
        > ccy             	String  	定投币种，如BTC
        > ratio           	String  	定投币种资产占比，如 "0.2"代表占比20%
        > totalAmt        	String  	累计购入定投币种的数量
        > profit          	String  	定投收益，单位为investmentCcy
        > avgPx           	String  	定投均价，计价单位为investmentCcy
        > px              	String  	当前价格，计价单位为investmentCcy
        period            	String  	周期类型每月：monthly每周：weekly每日：daily
        recurringDay      	String  	投资日当周期类型为monthly，则取值范围是 [1,28] 的整数当周期类型为weekly，则取值范围是 [1,7] 的整数当周期类型为daily，则取值为1
        recurringTime     	String  	投资时间，取值范围是 [0,23] 的整数
        timeZone          	String  	时区（UTC），取值范围是 [-12,14] 的整数如8表示UTC+8（东8区），北京时间
        amt               	String  	每期投入数量
        investmentAmt     	String  	累计投入数量
        investmentCcy     	String  	投入数量单位，只能是USDT/USDC
        totalPnl          	String  	总收益
        totalAnnRate      	String  	总年化
        pnlRatio          	String  	收益率
        mktCap            	String  	当前总市值，单位为USDT
        cycles            	String  	定投累计轮数
        tag               	String  	订单标签
        '''
        return self.send_request(*_RecurringBuyEndpoints.get_orders_algo_details, **to_local(locals()))

    # GET / 获取定投策略子订单信息
    def get_sub_orders(self, algoId: str, ordId: str = '', after: str = '', before: str = '', limit: str = '',
                       proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/recurring/sub-orders
        https://www.okx.com/docs-v5/zh/#order-book-trading-recurring-buy-get-recurring-buy-sub-orders
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        ordId             	String  	否       	子订单ID
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，最大为300，默认300条
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        instType          	String  	产品类型
        instId            	String  	产品ID
        algoOrdType       	String  	策略订单类型recurring：定投
        ordId             	String  	子订单ID
        cTime             	String  	子订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	子订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        tdMode            	String  	子订单交易模式cross：全仓cash：非保证金
        ordType           	String  	子订单类型market：市价单
        sz                	String  	子订单委托数量
        state             	String  	子订单状态canceled：撤单成功live：等待成交partially_filled：部分成交filled：完全成交cancelling：撤单中
        side              	String  	子订单订单方向buy：买sell：卖
        px                	String  	子订单委托价格市价委托时为"-1"
        fee               	String  	子订单手续费数量
        feeCcy            	String  	子订单手续费币种
        avgPx             	String  	子订单平均成交价格
        accFillSz         	String  	子订单累计成交数量
        tag               	String  	订单标签
        '''
        return self.send_request(*_RecurringBuyEndpoints.get_sub_orders, **to_local(locals()))

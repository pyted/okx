'''
网格交易
https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading
'''

from paux.param import to_local
from okx.api._client import Client


class _GridTradeEndpoints():
    set_order_algo = ['/api/v5/tradingBot/grid/order-algo', 'POST']  # POST / 网格策略委托下单
    set_amend_order_algo = ['/api/v5/tradingBot/grid/amend-order-algo', 'POST']  # POST / 修改网格策略订单
    set_stop_order_algo = ['/api/v5/tradingBot/grid/stop-order-algo', 'POST']  # POST / 网格策略停止
    set_close_position = ['/api/v5/tradingBot/grid/close-position', 'POST']  # POST / 合约网格平仓
    set_cancel_close_order = ['/api/v5/tradingBot/grid/cancel-close-order', 'POST']  # POST / 撤销合约网格平仓单
    set_order_instant_trigger = ['/api/v5/tradingBot/grid/order-instant-trigger', 'POST']  # POST / 网格策略立即触发
    get_orders_algo_pending = ['/api/v5/tradingBot/grid/orders-algo-pending', 'GET']  # GET / 获取未完成网格策略委托单列表
    get_orders_algo_history = ['/api/v5/tradingBot/grid/orders-algo-history', 'GET']  # GET / 获取历史网格策略委托单列表
    get_orders_algo_details = ['/api/v5/tradingBot/grid/orders-algo-details', 'GET']  # GET / 获取网格策略委托订单详情
    get_sub_orders = ['/api/v5/tradingBot/grid/sub-orders', 'GET']  # GET / 获取网格策略委托子订单信息
    get_positions = ['/api/v5/tradingBot/grid/positions', 'GET']  # GET / 获取网格策略委托持仓
    set_withdraw_income = ['/api/v5/tradingBot/grid/withdraw-income', 'POST']  # POST / 现货/天地网格提取利润
    set_compute_margin_balance = ['/api/v5/tradingBot/grid/compute-margin-balance', 'POST']  # POST / 调整保证金计算
    set_margin_balance = ['/api/v5/tradingBot/grid/margin-balance', 'POST']  # POST / 调整保证金
    get_ai_param = ['/api/v5/tradingBot/grid/ai-param', 'GET']  # GET / 网格策略智能回测（公共）
    set_min_investment = ['/api/v5/tradingBot/grid/min-investment', 'POST']  # POST / 计算最小投资数量（公共）
    get_rsi_back_testing = ['/api/v5/tradingBot/public/rsi-back-testing', 'GET']  # GET / RSI回测（公共）


class GridTrade(Client):

    # POST / 网格策略委托下单
    def set_order_algo(self, instId: str, algoOrdType: str, maxPx: str, minPx: str, gridNum: str, runType: str = '',
                       tpTriggerPx: str = '', slTriggerPx: str = '', algoClOrdId: str = '', tag: str = '',
                       triggerParams: object = '', proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/tradingBot/grid/order-algo
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-place-grid-algo-order
        
        限速：20次/2s
        限速规则：UserID + Instrument ID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        maxPx             	String  	是       	区间最高价格
        minPx             	String  	是       	区间最低价格
        gridNum           	String  	是       	网格数量
        runType           	String  	否       	网格类型1：等差，2：等比默认为等差天地网格只支持2
        tpTriggerPx       	String  	否       	止盈触发价适用于现货网格/合约网格
        slTriggerPx       	String  	否       	止损触发价适用于现货网格/合约网格
        algoClOrdId       	String  	否       	用户自定义策略ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签
        triggerParams     	Array of object	否       	信号触发参数适用于现货网格/合约网格
        > triggerAction   	String  	是       	触发行为start：网格启动stop：网格停止
        > triggerStrategy 	String  	是       	触发策略instant：立即触发price：价格触发rsi：rsi指标触发默认为instant
        > delaySeconds    	String  	否       	延迟触发时间，单位为秒，默认为0
        > timeframe       	String  	否       	K线种类3m,5m,15m,30m(m代表分钟)1H,4H(H代表小时)1D(D代表天)该字段只在triggerStrategy为rsi时有效
        > thold           	String  	否       	阈值取值[1,100]的整数该字段只在triggerStrategy为rsi时有效
        > triggerCond     	String  	否       	触发条件cross_up：上穿cross_down：下穿above：上方below：下方cross：交叉该字段只在triggerStrategy为rsi时有效
        > timePeriod      	String  	否       	周期14该字段只在triggerStrategy为rsi下有效
        > triggerPx       	String  	否       	触发价格该字段只在triggerStrategy为price下有效
        > stopType        	String  	否       	策略停止类型现货/天地网格1：卖出交易币，2：不卖出交易币合约网格1：停止平仓，2：停止不平仓该字段只在triggerAction为stop时有效
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        tag               	String  	订单标签
        '''
        return self.send_request(*_GridTradeEndpoints.set_order_algo, **to_local(locals()))

    # POST / 修改网格策略订单
    def set_amend_order_algo(self, algoId: str, instId: str, slTriggerPx: str = '', tpTriggerPx: str = '',
                             triggerParams: object = '', proxies={}, proxy_host: str = None):
        '''
        只支持合约网格策略的修改
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-amend-grid-algo-order
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        instId            	String  	是       	产品ID，如BTC-USDT-SWAP
        slTriggerPx       	String  	可选      	新的止损触发价当值为""则代表取消止损触发价slTriggerPx、tpTriggerPx至少要传一个值
        tpTriggerPx       	String  	可选      	新的止盈触发价当值为""则代表取消止盈触发价
        triggerParams     	Array of object	否       	信号触发参数
        > triggerAction   	String  	是       	触发行为start：网格启动stop：网格停止
        > triggerStrategy 	String  	是       	触发策略instant：立即触发price：价格触发rsi：rsi指标触发
        > triggerPx       	String  	否       	触发价格该字段只在triggerStrategy为price下有效
        > stopType        	String  	否       	策略停止类型现货/天地网格1：卖出交易币，2：不卖出交易币合约网格1：停止平仓，2：停止不平仓该字段只在triggerAction为stop时有效
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        tag               	String  	订单标签
        '''
        return self.send_request(*_GridTradeEndpoints.set_amend_order_algo, **to_local(locals()))

    # POST / 网格策略停止
    def set_stop_order_algo(self, algoId: str, instId: str, algoOrdType: str, stopType: str, proxies={},
                            proxy_host: str = None):
        '''
        每次最多可以撤销10个网格策略。
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-stop-grid-algo-order
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        instId            	String  	是       	产品ID，如BTC-USDT
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        stopType          	String  	是       	网格策略停止类型现货网格/天地网格1：卖出交易币，2：不卖出交易币合约网格1：市价全平2：停止不平仓
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        tag               	String  	订单标签
        '''
        return self.send_request(*_GridTradeEndpoints.set_stop_order_algo, **to_local(locals()))

    # POST / 合约网格平仓
    def set_close_position(self, algoId: str, mktClose: bool, sz: str = '', px: str = '', proxies={},
                           proxy_host: str = None):
        '''
        只有处于已停止未平仓状态合约网格可使用该接口
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-close-position-for-contract-grid
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        mktClose          	Boolean 	是       	是否市价全平true：市价全平，false：部分平仓
        sz                	String  	可选      	平仓数量,单位为张部分平仓时必传
        px                	String  	可选      	平仓价格部分平仓时必传
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        ordId             	String  	平仓单ID市价全平时，该字段为""
        algoClOrdId       	String  	用户自定义策略ID
        tag               	String  	订单标签
        '''
        return self.send_request(*_GridTradeEndpoints.set_close_position, **to_local(locals()))

    # POST / 撤销合约网格平仓单
    def set_cancel_close_order(self, algoId: str, ordId: str, proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/tradingBot/grid/cancel-close-order
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-cancel-close-position-order-for-contract-grid
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        ordId             	String  	是       	平仓单ID
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        ordId             	String  	平仓单ID
        algoClOrdId       	String  	用户自定义策略ID
        tag               	String  	订单标签
        '''
        return self.send_request(*_GridTradeEndpoints.set_cancel_close_order, **to_local(locals()))

    # POST / 网格策略立即触发
    def set_order_instant_trigger(self, algoId: str, proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/tradingBot/grid/order-instant-trigger
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-instant-trigger-grid-algo-order
        
        限速：20次/2s
        限速规则：UserID + Instrument ID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        '''
        return self.send_request(*_GridTradeEndpoints.set_order_instant_trigger, **to_local(locals()))

    # GET / 获取未完成网格策略委托单列表
    def get_orders_algo_pending(self, algoOrdType: str, algoId: str = '', instId: str = '', instType: str = '',
                                after: str = '', before: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/grid/orders-algo-pending
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-get-grid-algo-order-list
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        algoId            	String  	否       	策略订单ID
        instId            	String  	否       	产品ID，如BTC-USDT
        instType          	String  	否       	产品类型SPOT：币币MARGIN：杠杆FUTURES：交割合约SWAP：永续合约
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        instType          	String  	产品类型
        instId            	String  	产品ID
        cTime             	String  	策略订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	策略订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        algoOrdType       	String  	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        state             	String  	订单状态starting：启动中running：运行中stopping：终止中no_close_position：已停止未平仓（仅适用于合约网格）
        rebateTrans       	Array of object	返佣划转信息
        > rebate          	String  	返佣数量
        > rebateCcy       	String  	返佣币种
        triggerParams     	Array of object	信号触发参数
        > triggerAction   	String  	触发行为start：网格启动stop：网格停止
        > triggerStrategy 	String  	触发策略instant：立即触发price：价格触发rsi：rsi指标触发
        > delaySeconds    	String  	延迟触发时间，单位为秒
        > triggerTime     	String  	triggerAction实际触发时间，Unix时间戳的毫秒数格式, 如1597026383085
        > triggerType     	String  	triggerAction的实际触发类型manual：手动触发auto: 自动触发
        > timeframe       	String  	K线种类3m,5m,15m,30m(m代表分钟)1H,4H(H代表小时)1D(D代表天)该字段只在triggerStrategy为rsi时有效
        > thold           	String  	阈值取值[1,100]的整数该字段只在triggerStrategy为rsi时有效
        > triggerCond     	String  	触发条件cross_up：上穿cross_down：下穿above：上方below：下方cross：交叉该字段只在triggerStrategy为rsi时有效
        > timePeriod      	String  	周期14该字段只在triggerStrategy为rsi下有效
        > triggerPx       	String  	触发价格该字段只在triggerStrategy为price下有效
        > stopType        	String  	策略停止类型现货/天地网格1：卖出交易币，2：不卖出交易币合约网格1：停止平仓，2：停止不平仓该字段只在triggerAction为stop时有效
        maxPx             	String  	区间最高价格
        minPx             	String  	区间最低价格
        gridNum           	String  	网格数量
        runType           	String  	网格类型1：等差，2：等比
        tpTriggerPx       	String  	止盈触发价
        slTriggerPx       	String  	止损触发价
        arbitrageNum      	String  	网格套利次数
        totalPnl          	String  	总收益
        pnlRatio          	String  	收益率
        investment        	String  	投入金额现货网格如果投入了交易币则折算为计价币
        gridProfit        	String  	网格利润
        floatProfit       	String  	浮动盈亏
        cancelType        	String  	网格策略停止原因0：无1：手动停止2：止盈停止3：止损停止4：风控停止5：交割停止6: 信号停止
        stopType          	String  	网格策略实际停止类型现货网格/天地网格1：卖出交易币，2：不卖出交易币合约网格1：停止平仓，2：停止不平仓
        quoteSz           	String  	计价币投入数量适用于现货网格/天地网格
        baseSz            	String  	交易币投入数量适用于现货网格
        direction         	String  	合约网格类型long：做多，short：做空，neutral：中性仅适用于合约网格
        basePos           	Boolean 	是否开底仓适用于合约网格
        sz                	String  	投入保证金，单位为USDT适用于合约网格
        lever             	String  	杠杆倍数适用于合约网格
        actualLever       	String  	实际杠杆倍数适用于合约网格
        liqPx             	String  	预估强平价格适用于合约网格
        uly               	String  	标的指数适用于合约网格
        instFamily        	String  	交易品种适用于交割/永续/期权，如BTC-USD适用于合约网格
        ordFrozen         	String  	挂单占用适用于合约网格
        availEq           	String  	可用保证金适用于合约网格
        tag               	String  	订单标签
        profitSharingRatio	String  	分润比例取值范围[0,0.3]如果是普通订单（既不是带单也不是跟单），该字段返回""
        copyType          	String  	分润订单类型0：普通订单1：普通跟单2：分润跟单3：带单
        '''
        return self.send_request(*_GridTradeEndpoints.get_orders_algo_pending, **to_local(locals()))

    # GET / 获取历史网格策略委托单列表
    def get_orders_algo_history(self, algoOrdType: str, algoId: str = '', instId: str = '', instType: str = '',
                                after: str = '', before: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/grid/orders-algo-history
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-get-grid-algo-order-history
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        algoId            	String  	否       	策略订单ID
        instId            	String  	否       	产品ID，如BTC-USDT
        instType          	String  	否       	产品类型SPOT：币币MARGIN：杠杆FUTURES：交割合约SWAP：永续合约
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        instType          	String  	产品类型
        instId            	String  	产品ID
        cTime             	String  	策略订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	策略订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        algoOrdType       	String  	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        state             	String  	订单状态stopped：已停止
        rebateTrans       	Array of object	返佣划转信息
        > rebate          	String  	返佣数量
        > rebateCcy       	String  	返佣币种
        triggerParams     	Array of object	信号触发参数
        > triggerAction   	String  	触发行为start：网格启动stop：网格停止
        > triggerStrategy 	String  	触发策略instant：立即触发price：价格触发rsi：rsi指标触发
        > delaySeconds    	String  	延迟触发时间，单位为秒
        > triggerTime     	String  	triggerAction实际触发时间，Unix时间戳的毫秒数格式, 如1597026383085
        > triggerType     	String  	triggerAction的实际触发类型manual：手动触发auto: 自动触发
        > timeframe       	String  	K线种类3m,5m,15m,30m(m代表分钟)1H,4H(H代表小时)1D(D代表天)该字段只在triggerStrategy为rsi时有效
        > thold           	String  	阈值取值[1,100]的整数该字段只在triggerStrategy为rsi时有效
        > triggerCond     	String  	触发条件cross_up：上穿cross_down：下穿above：上方below：下方cross：交叉该字段只在triggerStrategy为rsi时有效
        > timePeriod      	String  	周期14该字段只在triggerStrategy为rsi下有效
        > triggerPx       	String  	触发价格该字段只在triggerStrategy为price下有效
        > stopType        	String  	策略停止类型现货/天地网格1：卖出交易币，2：不卖出交易币合约网格1：停止平仓，2：停止不平仓该字段只在triggerAction为stop时有效
        maxPx             	String  	区间最高价格
        minPx             	String  	区间最低价格
        gridNum           	String  	网格数量
        runType           	String  	网格类型1：等差，2：等比
        tpTriggerPx       	String  	止盈触发价
        slTriggerPx       	String  	止损触发价
        arbitrageNum      	String  	网格套利次数
        totalPnl          	String  	总收益
        pnlRatio          	String  	收益率
        investment        	String  	投入金额现货网格如果投入了交易币则折算为计价币
        gridProfit        	String  	网格利润
        floatProfit       	String  	浮动盈亏
        cancelType        	String  	网格策略停止原因0：无1：手动停止2：止盈停止3：止损停止4：风控停止5：交割停止6: 信号停止
        stopType          	String  	网格策略实际停止类型现货网格/天地网格1：卖出交易币，2：不卖出交易币合约网格1：停止平仓，2：停止不平仓
        quoteSz           	String  	计价币投入数量适用于现货网格/天地网格
        baseSz            	String  	交易币投入数量适用于现货网格
        direction         	String  	合约网格类型long：做多，short：做空，neutral：中性仅适用于合约网格
        basePos           	Boolean 	是否开底仓适用于合约网格
        sz                	String  	投入保证金，单位为USDT适用于合约网格
        lever             	String  	杠杆倍数适用于合约网格
        actualLever       	String  	实际杠杆倍数适用于合约网格
        liqPx             	String  	预估强平价格适用于合约网格
        uly               	String  	标的指数适用于合约网格
        instFamily        	String  	交易品种适用于交割/永续/期权，如BTC-USD适用于合约网格
        ordFrozen         	String  	挂单占用适用于合约网格
        availEq           	String  	可用保证金适用于合约网格
        tag               	String  	订单标签
        profitSharingRatio	String  	分润比例取值范围[0,0.3]如果是普通订单（既不是带单也不是跟单），该字段返回""
        copyType          	String  	分润订单类型0：普通订单1：普通跟单2：分润跟单3：带单
        '''
        return self.send_request(*_GridTradeEndpoints.get_orders_algo_history, **to_local(locals()))

    # GET / 获取网格策略委托订单详情
    def get_orders_algo_details(self, algoOrdType: str, algoId: str, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/grid/orders-algo-details
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-get-grid-algo-order-details
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        algoId            	String  	是       	策略订单ID
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        instType          	String  	产品类型
        instId            	String  	产品ID
        cTime             	String  	策略订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	策略订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        algoOrdType       	String  	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        state             	String  	订单状态starting：启动中running：运行中stopping：终止中no_close_position：已停止未平仓（仅适用于合约网格）stopped：已停止
        rebateTrans       	Array of object	返佣划转信息
        > rebate          	String  	返佣数量
        > rebateCcy       	String  	返佣币种
        triggerParams     	Array of object	信号触发参数
        > triggerAction   	String  	触发行为start：网格启动stop：网格停止
        > triggerStrategy 	String  	触发策略instant：立即触发price：价格触发rsi：rsi指标触发
        > delaySeconds    	String  	延迟触发时间，单位为秒
        > triggerTime     	String  	triggerAction实际触发时间，Unix时间戳的毫秒数格式, 如1597026383085
        > triggerType     	String  	triggerAction的实际触发类型manual：手动触发auto: 自动触发
        > timeframe       	String  	K线种类3m,5m,15m,30m(m代表分钟)1H,4H(H代表小时)1D(D代表天)该字段只在triggerStrategy为rsi时有效
        > thold           	String  	阈值取值[1,100]的整数该字段只在triggerStrategy为rsi时有效
        > triggerCond     	String  	触发条件cross_up：上穿cross_down：下穿above：上方below：下方cross：交叉该字段只在triggerStrategy为rsi时有效
        > timePeriod      	String  	周期14该字段只在triggerStrategy为rsi下有效
        > triggerPx       	String  	触发价格该字段只在triggerStrategy为price下有效
        > stopType        	String  	策略停止类型现货/天地网格1：卖出交易币，2：不卖出交易币合约网格1：停止平仓，2：停止不平仓该字段只在triggerAction为stop时有效
        maxPx             	String  	区间最高价格
        minPx             	String  	区间最低价格
        gridNum           	String  	网格数量
        runType           	String  	网格类型1：等差，2：等比
        tpTriggerPx       	String  	止盈触发价
        slTriggerPx       	String  	止损触发价
        tradeNum          	String  	挂单成交次数
        arbitrageNum      	String  	网格套利次数
        singleAmt         	String  	单网格买卖量
        perMinProfitRate  	String  	预期单网格最低利润率
        perMaxProfitRate  	String  	预期单网格最高利润率
        runPx             	String  	启动时价格
        totalPnl          	String  	总收益
        pnlRatio          	String  	收益率
        investment        	String  	投入金额现货网格如果投入了交易币则折算为计价币
        gridProfit        	String  	网格利润
        floatProfit       	String  	浮动盈亏
        totalAnnualizedRate	String  	总年化
        annualizedRate    	String  	网格年化
        cancelType        	String  	网格策略停止原因0：无1：手动停止2：止盈停止3：止损停止4：风控停止5：交割停止6: 信号停止
        stopType          	String  	网格策略停止类型现货网格/天地网格1：卖出交易币，2：不卖出交易币合约网格1：市价全平，2：停止不平仓
        activeOrdNum      	String  	子订单挂单数量
        quoteSz           	String  	计价币投入数量仅适用于现货网格/天地网格
        baseSz            	String  	交易币投入数量仅适用于现货网格
        curQuoteSz        	String  	当前持有的计价币资产仅适用于现货网格/天地网格
        curBaseSz         	String  	当前持有的交易币资产仅适用于现货网格/天地网格
        profit            	String  	当前可提取利润,单位是计价币仅适用于现货网格/天地网格
        stopResult        	String  	策略停止结果0：默认，1：市价卖币成功-1：市价卖币失败仅适用于现货网格/天地网格
        direction         	String  	合约网格类型long：做多，short：做空，neutral：中性仅适用于合约网格
        basePos           	Boolean 	是否开底仓仅适用于合约网格
        sz                	String  	投入保证金，单位为USDT仅适用于合约网格
        lever             	String  	杠杆倍数仅适用于合约网格
        actualLever       	String  	实际杠杆倍数仅适用于合约网格
        liqPx             	String  	预估强平价格仅适用于合约网格
        uly               	String  	标的指数仅适用于合约网格
        instFamily        	String  	交易品种适用于交割/永续/期权，如BTC-USD适用于合约网格
        ordFrozen         	String  	挂单占用适用于合约网格
        availEq           	String  	可用保证金适用于合约网格
        eq                	String  	策略账户总权益仅适用于合约网格
        tag               	String  	订单标签
        profitSharingRatio	String  	分润比例取值范围[0,0.3]如果是普通订单（既不是带单也不是跟单），该字段返回""
        copyType          	String  	分润订单类型0：普通订单1：普通跟单2：分润跟单3：带单
        '''
        return self.send_request(*_GridTradeEndpoints.get_orders_algo_details, **to_local(locals()))

    # GET / 获取网格策略委托子订单信息
    def get_sub_orders(self, algoId: str, algoOrdType: str, type: str, groupId: str = '', after: str = '',
                       before: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/grid/sub-orders
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-get-grid-algo-sub-orders
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        type              	String  	是       	子订单状态live：未成交filled：已成交
        groupId           	String  	否       	组ID
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        instType          	String  	产品类型
        instId            	String  	产品ID
        algoOrdType       	String  	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        groupId           	String  	组ID
        ordId             	String  	子订单ID
        cTime             	String  	子订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	子订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        tdMode            	String  	子订单交易模式cross：全仓isolated：逐仓cash：非保证金
        ccy               	String  	保证金币种仅适用于单币种保证金模式下的全仓杠杆订单
        ordType           	String  	子订单类型market：市价单limit：限价单
        sz                	String  	子订单委托数量
        state             	String  	子订单状态canceled：撤单成功live：等待成交partially_filled：部分成交filled：完全成交cancelling：撤单中
        side              	String  	子订单订单方向buy：买sell：卖
        px                	String  	子订单委托价格
        fee               	String  	子订单手续费数量
        feeCcy            	String  	子订单手续费币种
        rebate            	String  	子订单返佣数量
        rebateCcy         	String  	子订单返佣币种
        avgPx             	String  	子订单平均成交价格
        accFillSz         	String  	子订单累计成交数量
        posSide           	String  	子订单持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式
        pnl               	String  	子订单收益
        ctVal             	String  	合约面值仅支持FUTURES/SWAP
        lever             	String  	杠杆倍数
        tag               	String  	订单标签
        '''
        return self.send_request(*_GridTradeEndpoints.get_sub_orders, **to_local(locals()))

    # GET / 获取网格策略委托持仓
    def get_positions(self, algoOrdType: str, algoId: str, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/grid/positions
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-get-grid-algo-order-positions
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoOrdType       	String  	是       	订单类型contract_grid：合约网格委托
        algoId            	String  	是       	策略订单ID
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        instType          	String  	产品类型
        instId            	String  	产品ID，如BTC-USDT-SWAP
        cTime             	String  	策略订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	策略订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        avgPx             	String  	开仓均价
        ccy               	String  	保证金币种
        lever             	String  	杠杆倍数
        liqPx             	String  	预估强平价
        posSide           	String  	持仓方向net：买卖模式
        pos               	String  	持仓数量
        mgnMode           	String  	保证金模式cross：全仓isolated：逐仓
        mgnRatio          	String  	保证金率
        imr               	String  	初始保证金
        mmr               	String  	维持保证金
        upl               	String  	未实现收益
        uplRatio          	String  	未实现收益率
        last              	String  	最新成交价
        notionalUsd       	String  	仓位美金价值
        adl               	String  	信号区分为5档，从1到5，数字越小代表adl强度越弱
        markPx            	String  	标记价格
        '''
        return self.send_request(*_GridTradeEndpoints.get_positions, **to_local(locals()))

    # POST / 现货/天地网格提取利润
    def set_withdraw_income(self, algoId: str, proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/tradingBot/grid/withdraw-income
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-spot-moon-grid-withdraw-income
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        profit            	String  	提取的利润
        '''
        return self.send_request(*_GridTradeEndpoints.set_withdraw_income, **to_local(locals()))

    # POST / 调整保证金计算
    def set_compute_margin_balance(self, algoId: str, type: str, amt: str = '', proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/tradingBot/grid/compute-margin-balance
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-compute-margin-balance
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        type              	String  	是       	调整保证金类型add：增加，reduce：减少
        amt               	String  	否       	调整保证金数量
        返回参数:
        Parameter         	Type    	Description
        maxAmt            	String  	最多可调整的保证金数量
        lever             	String  	调整保证金后的杠杠倍数
        '''
        return self.send_request(*_GridTradeEndpoints.set_compute_margin_balance, **to_local(locals()))

    # POST / 调整保证金
    def set_margin_balance(self, algoId: str, type: str, amt: str = '', percent: str = '', proxies={},
                           proxy_host: str = None):
        '''
        POST /api/v5/tradingBot/grid/margin-balance
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-adjust-margin-balance
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        type              	String  	是       	调整保证金类型add：增加，reduce：减少
        amt               	String  	可选      	调整保证金数量amt和percent必须传一个
        percent           	String  	可选      	调整保证金百分比
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        '''
        return self.send_request(*_GridTradeEndpoints.set_margin_balance, **to_local(locals()))

    # GET / 网格策略智能回测（公共）
    def get_ai_param(self, algoOrdType: str, instId: str, direction: str = '', duration: str = '', proxies={},
                     proxy_host: str = None):
        '''
        公共接口无须鉴权
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-get-grid-ai-parameter-public
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        instId            	String  	是       	产品ID，如BTC-USDT
        direction         	String  	可选      	合约网格类型long：做多，short：做空，neutral：中性合约网格必填
        duration          	String  	否       	回测周期7D：7天，30D：30天，180D：180天默认现货网格为7D，天地网格为180D合约网格只支持7D
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        algoOrdType       	String  	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        duration          	String  	回测周期7D：7天，30D：30天，180D：180天
        gridNum           	String  	网格数量
        maxPx             	String  	区间最高价格
        minPx             	String  	区间最低价格
        perMaxProfitRate  	String  	单网格最高利润率
        perMinProfitRate  	String  	单网格最低利润率
        annualizedRate    	String  	网格年化收益率
        minInvestment     	String  	最小投资数量
        ccy               	String  	投资币种
        runType           	String  	网格类型1：等差，2：等比
        direction         	String  	合约网格类型仅适用于合约网格
        lever             	String  	杠杆倍数仅适用于合约网格
        '''
        return self.send_request(*_GridTradeEndpoints.get_ai_param, **to_local(locals()))

    # POST / 计算最小投资数量（公共）
    def set_min_investment(self, instId: str, algoOrdType: str, gridNum: str, maxPx: str, minPx: str, runType: str,
                           direction: str = '', lever: str = '', basePos: bool = '', investmentData: object = '',
                           proxies={}, proxy_host: str = None):
        '''
        公共接口无须鉴权
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-post-compute-min-investment-public
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托
        gridNum           	String  	是       	网格数量
        maxPx             	String  	是       	区间最高价格
        minPx             	String  	是       	区间最低价格
        runType           	String  	是       	网格类型1：等差，2：等比
        direction         	String  	可选      	合约网格类型long：做多，short：做空，neutral：中性适用于合约网格
        lever             	String  	可选      	杠杆倍数适用于合约网格
        basePos           	Boolean 	否       	是否开底仓默认为false
        investmentData    	Array of object	否       	投资信息
        > amt             	String  	是       	投资数量
        > ccy             	String  	是       	投资币种
        返回参数:
        Parameter         	Type    	Description
        investmentData    	Array of object	最小投入信息
        > amt             	String  	最小投入数量
        > ccy             	String  	最小投入币种
        singleAmt         	String  	单网格买卖量现货网格单位为计价币合约网格单位为张
        '''
        return self.send_request(*_GridTradeEndpoints.set_min_investment, **to_local(locals()))

    # GET / RSI回测（公共）
    def get_rsi_back_testing(self, instId: str, timeframe: str, thold: str, timePeriod: str, triggerCond: str = '',
                             duration: str = '', proxies={}, proxy_host: str = None):
        '''
        公共接口无须鉴权
        https://www.okx.com/docs-v5/zh/#order-book-trading-grid-trading-get-rsi-back-testing-public
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT适用于币币
        timeframe         	String  	是       	K线种类3m,5m,15m,30m(m代表分钟)1H,4H(H代表小时)1D(D代表天)
        thold             	String  	是       	阈值取值[1,100]的整数
        timePeriod        	String  	是       	周期14
        triggerCond       	String  	否       	触发条件cross_up：上穿cross_down：下穿above：上方below：下方cross：交叉默认是cross_down
        duration          	String  	否       	回测周期1M：1个月默认1M
        返回参数:
        Parameter         	Type    	Description
        triggerNum        	String  	触发次数
        '''
        return self.send_request(*_GridTradeEndpoints.get_rsi_back_testing, **to_local(locals()))

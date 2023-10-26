'''
信号交易
https://www.okx.com/docs-v5/zh/#order-book-trading-signal-bot-trading
'''
from paux.param import to_local
from okx.api._client import Client


class _SignalBotTradeEndpoints():
    get_orders_algo_details = ['/api/v5/tradingBot/signal/orders-algo-details', 'GET']  # GET / 获取信号策略详情
    get_positions = ['/api/v5/tradingBot/grid/positions', 'GET']  # GET / 获取信号策略持仓
    get_sub_orders = ['/api/v5/tradingBot/signal/sub-orders', 'GET']  # GET / 获取信号策略子订单信息
    get_event_history = ['/api/v5/tradingBot/signal/event-history', 'GET']  # GET / 获取信号策略历史事件


class SignalBotTrade(Client):

    # GET / 获取信号策略详情
    def get_orders_algo_details(self, algoOrdType: str, algoId: str, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/signal/orders-algo-details
        https://www.okx.com/docs-v5/zh/#order-book-trading-signal-bot-trading-get-signal-bot-order-details
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoOrdType       	String  	是       	策略订单类型contract：合约信号
        algoId            	String  	是       	策略订单ID
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        instType          	String  	产品类型
        instIds           	Array of string	该信号支持的产品ID列表
        cTime             	String  	策略订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	策略订单更新时间，Unix时间戳的毫秒数格式，如1597026383085
        algoOrdType       	String  	策略订单类型contract：合约信号
        state             	String  	订单状态starting：启动中running：运行中stopping：终止中stopped：已停止
        cancelType        	String  	策略停止原因0：无1：手动停止
        totalPnl          	String  	总收益
        pnlRatio          	String  	收益率
        totalEq           	String  	当前策略总权益
        floatPnl          	String  	浮动盈亏
        realizedPnl       	String  	已实现盈亏
        frozenBal         	String  	占用保证金
        availBal          	String  	可用保证金
        lever             	String  	杠杆倍数仅适用于合约信号
        investAmt         	String  	投入金额
        subOrdType        	String  	委托类型1：限价2：市价9：tradingView信号
        ratio             	String  	限价单的委托价格距离买一/卖一价的百分比当委托类型为限价时，该字段有效，无效则返回""。
        entrySettingParam 	Object  	进场参数设定
        > allowMultipleEntry	Boolean 	是否允许多次进场true：允许false：不允许
        > entryType       	String  	单次委托类型1：单次委托量具体数值将从 TradingView 信号中传入2：单次委托量为固定数量的保证金3：单次委托量为固定的合约张数4：单次委托量基于在收到触发信号时策略中可用保证金的百分比5：单次委托量基于在创建策略时设置的初始投入保证金的百分比
        > amt             	String  	单笔委托量在单次委托类型是 固定保证金 / 合约张数 下该字段有效，无效的时候返回""
        > ratio           	String  	单笔委托数量百分比在单次委托类型是 占用保证金比例 / 初始投资比例 下该字段有效，无效的时候返回""
        exitSettingParam  	Object  	离场参数设定
        > tpSlType        	String  	止盈止损类型，该参数用户确定设置止盈止损的触发价格计算的方式pnl：基于平均持仓成本和预期收益率price：基于相对于平均持仓成本的涨跌幅
        > tpPct           	String  	止盈百分比
        > slPct           	String  	止损百分比
        signalChanId      	String  	信号ID
        signalChanName    	String  	信号名称
        signalSourceType  	String  	信号来源类型1：自己创建的2：订阅他人3：免费信号
        '''
        return self.send_request(*_SignalBotTradeEndpoints.get_orders_algo_details, **to_local(locals()))

    # GET / 获取信号策略持仓
    def get_positions(self, algoOrdType: str, algoId: str, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/grid/positions
        https://www.okx.com/docs-v5/zh/#order-book-trading-signal-bot-trading-get-signal-bot-order-positions
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoOrdType       	String  	是       	订单类型contract：合约信号
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
        return self.send_request(*_SignalBotTradeEndpoints.get_positions, **to_local(locals()))

    # GET / 获取信号策略子订单信息
    def get_sub_orders(self, algoId: str, algoOrdType: str, type: str = '', clOrdId: str = '', after: str = '',
                       before: str = '', begin: str = '', end: str = '', limit: str = '', proxies={},
                       proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/signal/sub-orders
        https://www.okx.com/docs-v5/zh/#order-book-trading-signal-bot-trading-get-signal-bot-sub-orders
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        algoOrdType       	String  	是       	策略订单类型contract：合约信号
        type              	String  	可选      	子订单状态live：未成交filled：已成交type和clOrdId必须传一个，如果都传只认clOrdId
        clOrdId           	String  	可选      	子订单自定义订单ID
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        begin             	String  	否       	请求cTime在此时间戳之后(包含)的数据，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        end               	String  	否       	请求cTime在此时间戳之前(包含)的数据，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        algoClOrdId       	String  	用户自定义策略ID
        instType          	String  	产品类型
        instId            	String  	交易产品ID
        algoOrdType       	String  	策略订单类型contract：合约信号
        ordId             	String  	子订单ID
        clOrdId           	String  	子订单自定义ID
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
        avgPx             	String  	子订单平均成交价格
        accFillSz         	String  	子订单累计成交数量
        posSide           	String  	子订单持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式
        pnl               	String  	子订单收益
        ctVal             	String  	合约面值仅支持FUTURES/SWAP
        lever             	String  	杠杆倍数
        tag               	String  	订单标签
        '''
        return self.send_request(*_SignalBotTradeEndpoints.get_sub_orders, **to_local(locals()))

    # GET / 获取信号策略历史事件
    def get_event_history(self, algoId: str, after: str = '', before: str = '', limit: str = '', proxies={},
                          proxy_host: str = None):
        '''
        GET /api/v5/tradingBot/signal/event-history
        https://www.okx.com/docs-v5/zh/#order-book-trading-signal-bot-trading-get-signal-bot-event-history
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略订单ID
        after             	String  	否       	请求eventCtime在此时间之前（更旧的数据）的分页内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	请求eventCtime此时间之后（更新的数据）的分页内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略订单ID
        eventType         	String  	事件类型system_action：系统行为user_action：用户行为signal_processing：信号下单
        eventCtime        	String  	事件发生时间，Unix时间戳的毫秒数格式，如1597026383085
        eventUtime        	String  	事件更新时间，Unix时间戳的毫秒数格式，如1597026383085
        eventProcessMsg   	String  	事件处理信息
        eventStatus       	String  	事件处理状态success：成功failure：失败
        triggeredOrdData  	Array of object	信号触发的子订单的信息
        > clOrdId         	String  	子订单自定义ID
        '''
        return self.send_request(*_SignalBotTradeEndpoints.get_event_history, **to_local(locals()))

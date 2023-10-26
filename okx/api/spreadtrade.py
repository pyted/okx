'''
价差交易
https://www.okx.com/docs-v5/zh/#spread-trading
'''
from paux.param import to_local
from okx.api._client import Client


class _SpreadTradeEndpoints():
    set_order = ['/api/v5/sprd/order', 'POST']  # 下单
    set_cancel_order = ['/api/v5/sprd/cancel-order', 'POST']  # 撤单
    set_mass_cancel = ['/api/v5/sprd/mass-cancel', 'POST']  # 全部撤单
    get_order = ['/api/v5/sprd/order', 'GET']  # 获取订单信息
    get_orders_pending = ['/api/v5/sprd/orders-pending', 'GET']  # 获取未成交订单列表
    get_orders_history = ['/api/v5/sprd/orders-history', 'GET']  # 获取历史订单记录（近七天)
    get_trades = ['/api/v5/sprd/trades', 'GET']  # 获取历史成交数据（近七天）
    get_spreads = ['/api/v5/sprd/spreads', 'GET']  # 获取Spreads（公共）
    get_books = ['/api/v5/sprd/books', 'GET']  # 获取Spread产品深度（公共）
    get_ticker = ['/api/v5/sprd/ticker', 'GET']  # 获取单个Spread产品行情信息（公共）
    get_public_trades = ['/api/v5/sprd/public-trades', 'GET']  # 获取公共成交数据（公共）


class SpreadTrade(Client):

    # 下单
    def set_order(self, sprdId: str, side: str, ordType: str, sz: str, px: str, clOrdId: str = '', tag: str = '',
                  proxies={}, proxy_host: str = None):
        '''
        下单
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-place-order
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        sprdId            	String  	是       	spread ID，如 BTC-USDT_BTC-USDT-SWAP
        clOrdId           	String  	否       	客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        side              	String  	是       	订单方向buy：买，sell：卖
        ordType           	String  	是       	订单类型limit：限价单post_only：只做maker单
        sz                	String  	是       	委托数量。反向价差的数量单位为USD，正向价差为其对应baseCcy
        px                	String  	是       	委托价格，仅适用于limit,post_only类型的订单
        返回参数:
        Parameter         	Type    	Description
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        tag               	String  	订单标签
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败或成功时的msg
        '''
        return self.send_request(*_SpreadTradeEndpoints.set_order, **to_local(locals()))

    # 撤单
    def set_cancel_order(self, ordId: str = '', clOrdId: str = '', proxies={}, proxy_host: str = None):
        '''
        撤销之前下的未完成订单。
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-cancel-order
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID
        返回参数:
        Parameter         	Type    	Description
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        '''
        return self.send_request(*_SpreadTradeEndpoints.set_cancel_order, **to_local(locals()))

    # 全部撤单
    def set_mass_cancel(self, sprdId: str = '', proxies={}, proxy_host: str = None):
        '''
        撤销所有挂单
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-cancel-all-orders
        
        限速：10次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        sprdId            	String  	否       	spread ID
        返回参数:
        Parameter         	Type    	Description
        result            	Boolean 	请求结果true,false
        '''
        return self.send_request(*_SpreadTradeEndpoints.set_mass_cancel, **to_local(locals()))

    # 获取订单信息
    def get_order(self, ordId: str = '', clOrdId: str = '', proxies={}, proxy_host: str = None):
        '''
        查订单信息
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-get-order-details
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID，如果clOrdId关联了多个订单，只会返回最近的那笔订单
        返回参数:
        Parameter         	Type    	Description
        sprdId            	String  	Spread ID
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        tag               	String  	订单标签
        px                	String  	委托价格
        sz                	String  	委托数量
        ordType           	String  	订单类型limit：限价单
        side              	String  	订单方向
        fillSz            	String  	最新成交数量
        fillPx            	String  	最新成交价格
        tradeId           	String  	最近成交ID
        accFillSz         	String  	累计成交数量
        pendingFillSz     	String  	待成交数量（包括带结算数量）
        pendingSettleSz   	String  	待结算数量
        canceledSz        	String  	被取消数量
        avgPx             	String  	成交均价，如果成交数量为0，该字段为""
        state             	String  	订单状态canceled：撤单成功live：等待成交partially_filled：部分成交filled：完全成交
        cancelSource      	String  	撤单原因0: 系统撤单1: 用户撤单31: 当前只挂单订单 (Post only) 将会吃掉挂单深度32: 自成交保护撤单
        uTime             	String  	订单状态更新时间，Unix时间戳的毫秒数格式，如1597026383085
        cTime             	String  	订单创建时间，Unix时间戳的毫秒数格式， 如1597026383085
        '''
        return self.send_request(*_SpreadTradeEndpoints.get_order, **to_local(locals()))

    # 获取未成交订单列表
    def get_orders_pending(self, sprdId: str = '', ordType: str = '', state: str = '', beginId: str = '',
                           endId: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        获取当前账户下所有未成交订单信息
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-get-active-orders
        
        限速：10次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        sprdId            	String  	否       	spread ID，如BTC-USDT_BTC-USDT-SWAP
        ordType           	String  	否       	订单类型limit：限价单
        state             	String  	否       	订单状态live：等待成交partially_filled：部分成交
        beginId           	String  	否       	请求的起始订单ID，请求此ID之后（更新的数据）的分页内容，不包括 beginId
        endId             	String  	否       	请求的结束订单ID，请求此ID之前（更旧的数据）的分页内容，不包括 endId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        sprdId            	String  	spread ID，如BTC-USDT_BTC-USDT-SWAP
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        tag               	String  	订单标签
        px                	String  	委托价格
        sz                	String  	委托数量
        ordType           	String  	订单类型limit：限价单
        side              	String  	订单方向
        fillSz            	String  	最新成交数量
        fillPx            	String  	最新成交价格
        tradeId           	String  	最近成交ID
        accFillSz         	String  	累计成交数量
        pendingFillSz     	String  	待成交数量（包括带结算数量）
        pendingSettleSz   	String  	待结算数量
        canceledSz        	String  	被取消数量
        avgPx             	String  	成交均价，如果成交数量为0，该字段为""
        state             	String  	订单状态live：等待成交partially_filled：部分成交
        cancelSource      	String  	撤单原因0: 系统撤单1: 用户撤单31: 当前只挂单订单 (Post only) 将会吃掉挂单深度
        uTime             	String  	订单状态更新时间，Unix时间戳的毫秒数格式，如：1597026383085
        cTime             	String  	订单创建时间，Unix时间戳的毫秒数格式，如：1597026383085
        '''
        return self.send_request(*_SpreadTradeEndpoints.get_orders_pending, **to_local(locals()))

    # 获取历史订单记录（近七天)
    def get_orders_history(self, sprdId: str = '', ordType: str = '', state: str = '', beginId: str = '',
                           endId: str = '', begin: str = '', end: str = '', limit: str = '', proxies={},
                           proxy_host: str = None):
        '''
        获取最近7天挂单，且完全成交的订单数据，包括7天以前挂单，但近7天才成交的订单数据。按照订单创建时间倒序排序。
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-get-orders-last-7-days
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        sprdId            	String  	否       	spread ID，如BTC-USDT_BTC-USDT-SWAP
        ordType           	String  	否       	订单类型limit：限价单
        state             	String  	否       	订单状态canceled：撤单成功filled：完全成交
        beginId           	String  	否       	请求的起始订单ID，请求此ID之后（更新的数据）的分页内容，不包括 beginId
        endId             	String  	否       	请求的结束订单ID，请求此ID之前（更旧的数据）的分页内容，不包括 endId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        sprdId            	String  	spread ID，如BTC-USDT_BTC-USDT-SWAP
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        tag               	String  	订单标签
        px                	String  	委托价格
        sz                	String  	委托数量
        ordType           	String  	订单类型limit：限价单
        side              	String  	订单方向
        fillSz            	String  	最新成交数量
        fillPx            	String  	最新成交价格
        tradeId           	String  	最近成交ID
        accFillSz         	String  	累计成交数量
        pendingFillSz     	String  	待成交数量（包括带结算数量）
        pendingSettleSz   	String  	待结算数量
        canceledSz        	String  	被取消数量
        avgPx             	String  	成交均价，如果成交数量为0，该字段为""
        state             	String  	订单状态canceled：撤单成功filled：完全成交
        cancelSource      	String  	撤单原因0: 系统撤单1: 用户撤单31: 当前只挂单订单 (Post only) 将会吃掉挂单深度32: 自成交保护撤单
        uTime             	String  	订单状态更新时间，Unix时间戳的毫秒数格式，如：1597026383085
        cTime             	String  	订单创建时间，Unix时间戳的毫秒数格式， 如 ：1597026383085
        '''
        return self.send_request(*_SpreadTradeEndpoints.get_orders_history, **to_local(locals()))

    # 获取历史成交数据（近七天）
    def get_trades(self, sprdId: str = '', tradeId: str = '', ordId: str = '', beginId: str = '', endId: str = '',
                   begin: str = '', end: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        获取近7天的订单成交明细信息. 结果按时间倒序返回。
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-get-trades-last-7-days
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        sprdId            	String  	否       	spread ID，如BTC-USDT_BTC-USDT-SWAP
        tradeId           	String  	否       	交易 ID
        ordId             	String  	否       	订单 ID
        beginId           	String  	否       	请求的起始交易ID，请求此ID之后（更新的数据）的分页内容，不包括 beginId
        endId             	String  	否       	请求的结束交易ID，请求此ID之前（更旧的数据）的分页内容，不包括 endId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        sprdId            	String  	spread ID，如BTC-USDT_BTC-USDT-SWAP
        tradeId           	String  	交易ID
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        tag               	String  	订单标签
        fillPx            	String  	成交价格
        fillSz            	String  	成交数量
        side              	String  	交易方向buy：买sell：卖
        state             	String  	交易状态filled：已成交rejected：被拒绝
        execType          	String  	流动性方向T：takerM：maker
        ts                	String  	成交明细产生时间，Unix时间戳的毫秒数格式，如1597026383085
        legs              	Array of objects	交易的腿
        > instId          	String  	产品 ID
        > px              	String  	价格
        > sz              	String  	数量
        > side            	String  	交易方向buy：买sell：卖
        > fee             	String  	手续费金额或者返佣金额，手续费扣除为‘负数’，如-0.01；手续费返佣为‘正数’，如 0.01
        > feeCcy          	String  	交易手续费币种或者返佣金币种
        > tradeId         	String  	交易ID
        code              	String  	错误码，默认0
        msg               	String  	错误提示，默认 ""
        '''
        return self.send_request(*_SpreadTradeEndpoints.get_trades, **to_local(locals()))

    # 获取Spreads（公共）
    def get_spreads(self, baseCcy: object = '', instId: str = '', sprdId: str = '', state: object = '', proxies={},
                    proxy_host: str = None):
        '''
        获取可交易的Spreads。
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-get-spreads-public
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        baseCcy           	string  	否       	Spread币种。 例如BTC, ETH
        instId            	String  	否       	Spread里包含的产品ID。
        sprdId            	String  	否       	Spread ID
        state             	string  	否       	Spread状态live：交易中suspend：暂停中expired：订单过期
        返回参数:
        Parameter         	Type    	Description
        sprdId            	String  	spread ID
        sprdType          	String  	Spread类型，有效值为linear,inverse
        state             	String  	Spread状态live：交易中suspend：暂停中expired：已过期
        baseCcy           	String  	Spread币种。 例如BTC, ETH。
        szCcy             	String  	Spread数量单位。 例如USD, BTC, ETH, USD。
        quoteCcy          	String  	Spread计价单位。例如USDT，USD。
        tickSz            	String  	下单价格精度，如 0.0001。单位为Spread计价单位quoteCcy。
        minSz             	String  	最小下单数量。单位为Spread数量单位szCcy。
        lotSz             	String  	下单数量精度。单位为Spread数量单位szCcy。
        listTime          	String  	上线日期。Unix时间戳的毫秒数格式，如1597026383085
        expTime           	String  	失效日期。Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	上次更新时间。Unix时间戳的毫秒数格式，如1597026383085
        legs              	array of objects	腿
        > instId          	String  	产品ID
        > side            	String  	产品方向。buy：买入sell：卖出
        '''
        return self.send_request(*_SpreadTradeEndpoints.get_spreads, **to_local(locals()))

    # 获取Spread产品深度（公共）
    def get_books(self, sprdId: str, sz: str = '', proxies={}, proxy_host: str = None):
        '''
        获取Spread产品深度列表
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-get-order-book-public
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        sprdId            	String  	是       	spread ID，如BTC-USDT_BTC-USDT-SWAP
        sz                	String  	否       	深度档位数量。最大值为400。默认值为5。
        返回参数:
        Parameter         	Type    	Description
        asks              	Array   	卖方深度
        bids              	Array   	买方深度
        ts                	String  	深度产生的时间
        '''
        return self.send_request(*_SpreadTradeEndpoints.get_books, **to_local(locals()))

    # 获取单个Spread产品行情信息（公共）
    def get_ticker(self, sprdId: str, proxies={}, proxy_host: str = None):
        '''
        获取单个Spread产品行情信息，包括最新成交价，买一卖一价及数量。
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-get-ticker-public
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        sprdId            	String  	是       	spread ID, e.g. BTC-USDT_BTC-USDT-SWAP
        返回参数:
        Parameter         	Type    	Description
        sprdId            	String  	spread ID
        last              	String  	最新成交价
        lastSz            	String  	最新成交的数量
        askPx             	String  	卖一价
        askSz             	String  	卖一价对应的数量
        bidPx             	String  	买一价
        bidSz             	String  	买一价对应的数量
        ts                	String  	ticker数据产生时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_SpreadTradeEndpoints.get_ticker, **to_local(locals()))

    # 获取公共成交数据（公共）
    def get_public_trades(self, sprdId: str = '', proxies={}, proxy_host: str = None):
        '''
        查询市场上的Spread成交信息数据，每次请求最多返回500条结果。结果按时间倒序返回。
        https://www.okx.com/docs-v5/zh/#spread-trading-rest-api-get-public-trades-public
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        sprdId            	String  	否       	Spread ID，例如BTC-USDT_BTC-USDT-SWAP
        返回参数:
        Parameter         	Type    	Description
        sprdId            	String  	spread ID
        tradeId           	String  	交易ID
        px                	String  	成交价格
        sz                	String  	成交数量
        side              	String  	Taker的交易方向buy：买sell：卖
        ts                	String  	交易时间，Unix时间戳的毫秒数格式， 如 ：1597026383085
        '''
        return self.send_request(*_SpreadTradeEndpoints.get_public_trades, **to_local(locals()))

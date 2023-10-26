'''
大宗交易
https://www.okx.com/docs-v5/zh/#block-trading-rest-api
'''

from paux.param import to_local
from okx.api._client import Client


class _BlockTradeEndpoints():
    get_counterparties = ['/api/v5/rfq/counterparties', 'GET']  # 获取报价方信息
    set_create_rfq = ['/api/v5/rfq/create-rfq', 'POST']  # 询价
    set_cancel_rfq = ['/api/v5/rfq/cancel-rfq', 'POST']  # 取消询价单
    set_cancel_batch_rfqs = ['/api/v5/rfq/cancel-batch-rfqs', 'POST']  # 批量取消询价单
    set_cancel_all_rfqs = ['/api/v5/rfq/cancel-all-rfqs', 'POST']  # 取消所有询价单
    set_execute_quote = ['/api/v5/rfq/execute-quote', 'POST']  # 执行报价
    get_maker_instrument_settings = ['/api/v5/rfq/maker-instrument-settings', 'GET']  # 获取可报价产品
    set_maker_instrument_settings = ['/api/v5/rfq/maker-instrument-settings', 'POST']  # 设置可报价产品
    set_mmp_reset = ['/api/v5/rfq/mmp-reset', 'POST']  # 重设MMP状态
    set_create_quote = ['/api/v5/rfq/create-quote', 'POST']  # 报价
    set_cancel_quote = ['/api/v5/rfq/cancel-quote', 'POST']  # 取消报价单
    set_cancel_batch_quotes = ['/api/v5/rfq/cancel-batch-quotes', 'POST']  # 批量取消报价单
    set_cancel_all_quotes = ['/api/v5/rfq/cancel-all-quotes', 'POST']  # 取消所有报价单
    get_rfqs = ['/api/v5/rfq/rfqs', 'GET']  # 获取询价单信息
    get_quotes = ['/api/v5/rfq/quotes', 'GET']  # 获取报价单信息
    get_trades = ['/api/v5/rfq/trades', 'GET']  # 获取大宗交易信息
    get_public_trades = ['/api/v5/rfq/public-trades', 'GET']  # 获取大宗交易公共成交数据
    get_block_tickers = ['/api/v5/market/block-tickers', 'GET']  # 获取大宗交易所有产品行情信息
    get_block_ticker = ['/api/v5/market/block-ticker', 'GET']  # 获取大宗交易单个产品行情信息
    get_block_trades = ['/api/v5/market/block-trades', 'GET']  # 获取大宗交易公共成交数据


class BlockTrade(Client):

    # 获取报价方信息
    def get_counterparties(self, proxies={}, proxy_host: str = None):
        '''
        查询可以参与交易的报价方信息。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-get-counterparties
        
        
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        traderName        	String  	报价方名称
        traderCode        	String  	报价方唯一标识代码，公开可见；报价和询价的相关接口都使用该代码代表报价方。
        type              	String  	报价方类型。LP指通过API连接的自动做市商。
        '''
        return self.send_request(*_BlockTradeEndpoints.get_counterparties, **to_local(locals()))

    # 询价
    def set_create_rfq(self, counterparties: object, legs: object, anonymous: bool = '', clRfqId: str = '',
                       tag: str = '', allowPartialExecution: bool = '', proxies={}, proxy_host: str = None):
        '''
        创建一个询价单。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-create-rfq
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        counterparties    	Array of strings	是       	希望收到询价的报价方列表，可通过/api/v5/rfq/counterparties/获取。
        anonymous         	Boolean 	否       	是否匿名询价，true表示匿名询价，false表示公开询价，默认值为false，为true时，即使在交易执行之后，身份也不会透露给报价方。
        clRfqId           	String  	否       	询价单自定义ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	询价单标签，与此询价单关联的大宗交易将有相同的标签。字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        allowPartialExecution	Boolean 	否       	RFQ是否可以被部分执行，如果腿的比例和原RFQ一致。有效值为true或false。默认为false。
        legs              	Array of objects	是       	组合交易，每次最多可以提交15组交易信息
        > instId          	String  	是       	产品ID
        > tdMode          	String  	否       	交易模式保证金模式：cross全仓isolated逐仓非保证金模式：cash非保证金.如未提供，tdMode 将继承系统设置的默认值：单币种保证金模式 & 现货:cash单币种保证金和多币种保证金模式下买入期权：isolated其他情况:cross
        > ccy             	String  	否       	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单在其他情况下该参数将被忽略。
        > sz              	String  	是       	委托数量
        > side            	String  	是       	询价单方向
        > posSide         	String  	否       	持仓方向买卖模式下默认为net。在开平仓模式下仅可选择long或short。如未指定，则处于开平仓模式下的用户始终会开新仓位。仅适用交割、永续。
        > tgtCcy          	String  	否       	委托数量的类型定义sz属性的单位。仅适用于 instType=SPOT。有效值为base_ccy和quote_ccy。未指定时，默认为base_ccy。
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	询价单结果
        > cTime           	String  	询价单创建时间，Unix时间戳的毫秒数格式。
        > uTime           	String  	询价单状态更新时间，Unix时间戳的毫秒数格式。
        > state           	String  	询价单的状态有效值为activecanceledpending_fillfilledexpiredtraded_awayfailedtraded_away仅适用于报价方
        > counterparties  	Array of strings	报价方列表
        > validUntil      	String  	询价单的过期时间，Unix时间戳的毫秒数格式。
        > clRfqId         	String  	询价单自定义ID，为客户端敏感信息，不会公开，对报价方返回""。
        > tag             	String  	RFQ标签，与此RFQ关联的大宗交易将有相同的标签。
        > allowPartialExecution	Boolean 	RFQ是否可以被部分执行，如果腿的比例和原RFQ一致。有效值为true或false。未指定时，默认为false。
        > traderCode      	String  	询价方唯一标识代码。
        > rfqId           	String  	询价单ID
        > legs            	Array of objects	组合交易，每个请求最多可放置15条腿
        >> instId         	String  	产品ID，例如："BTC-USDT-SWAP"
        >> tdMode         	String  	交易模式保证金模式：cross全仓isolated逐仓非保证金模式：cash非保证金.如未提供，tdMode 将继承系统设置的默认值：单币种保证金模式 & 现货:cash单币种保证金和多币种保证金模式下买入期权：isolated其他情况:cross
        >> ccy            	String  	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单在其他情况下该参数将被忽略。
        >> sz             	String  	委托数量
        >> side           	String  	询价单方向有效值为buy和sell。
        >> posSide        	String  	持仓方向买卖模式下默认为net。如未指定，则返回""，相当于net。在开平仓模式下仅可选择long或short。 如未指定，则返回""，对应于为交易开新仓位的方向（买入=>long，卖出=>short）。仅适用交割、永续。
        >> tgtCcy         	String  	委托数量的类型定义sz属性的单位。仅适用于 instType=SPOT。有效值为base_ccy和quote_ccy。未指定时，默认为base_ccy。
        '''
        return self.send_request(*_BlockTradeEndpoints.set_create_rfq, **to_local(locals()))

    # 取消询价单
    def set_cancel_rfq(self, rfqId: str = '', clRfqId: str = '', proxies={}, proxy_host: str = None):
        '''
        取消一个询价单。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-cancel-rfq
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        rfqId             	String  	可选      	询价单ID
        clRfqId           	String  	可选      	询价单自定义ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。当 clRfqId 和 rfqId 都传时，以 rfqId 为准。
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > rfqId           	String  	RFQ ID
        > clRfqId         	String  	由用户设置的 RFQ ID
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败时的msg
        '''
        return self.send_request(*_BlockTradeEndpoints.set_cancel_rfq, **to_local(locals()))

    # 批量取消询价单
    def set_cancel_batch_rfqs(self, rfqIds: object = '', clRfqIds: object = '', proxies={}, proxy_host: str = None):
        '''
        取消一个或多个询价单，每次最多可以撤销100个询价单。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-cancel-multiple-rfqs
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        rfqIds            	Array of strings	可选      	询价单IDs
        clRfqIds          	Array of strings	可选      	询价单自定义ID，当 clRfqIds 和 rfqIds 都传时，以 rfqIds 为准。
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > rfqId           	String  	询价单ID
        > clRfqId         	String  	询价单自定义ID.
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败时的msg
        '''
        return self.send_request(*_BlockTradeEndpoints.set_cancel_batch_rfqs, **to_local(locals()))

    # 取消所有询价单
    def set_cancel_all_rfqs(self, proxies={}, proxy_host: str = None):
        '''
        取消所有询价单
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-cancel-all-rfqs
        
        
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > ts              	String  	成功取消时间，Unix时间戳的毫秒数格式，例如 1597026383085。
        '''
        return self.send_request(*_BlockTradeEndpoints.set_cancel_all_rfqs, **to_local(locals()))

    # 执行报价
    def set_execute_quote(self, rfqId: str, quoteId: str, legs: object = '', proxies={}, proxy_host: str = None):
        '''
        执行报价，仅限询价的创建者使用
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-execute-quote
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        rfqId             	String  	是       	询价单ID
        quoteId           	String  	是       	报价单ID
        legs              	Array of objects	否       	用于部分执行的腿的数量。腿的数量比例必须与原RFQ相同。注意：每条腿的tgtCcy和side和原RFQ一致，px和对应Quote一致。
        > instId          	String  	是       	产品ID, 如 "BTC-USDT-SWAP".
        > sz              	String  	是       	该条腿的部分执行数量
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > cTime           	String  	交易执行的时间，Unix时间戳的毫秒数格式。
        > rfqId           	String  	询价单ID
        > clRfqId         	String  	询价单自定义ID，为客户敏感信息，不会公开，对报价方返回""。
        > quoteId         	String  	报价单ID
        > clQuoteId       	String  	报价单自定义ID，为客户敏感信息，不会公开，对询价方返回""。
        > blockTdId       	String  	大宗交易ID
        > tag             	String  	报价单标签，与此报价单关联的大宗交易将有相同的标签。
        > tTraderCode     	String  	询价价方唯一标识代码。询价时 anonymous 设置为true时不可见。
        > mTraderCode     	String  	报价方唯一标识代码。 报价时 anonymous 设置为true时不可见。
        > legs            	Array of objects	组合交易
        >> instId         	String  	产品ID
        >> px             	String  	成交价格
        >> sz             	String  	成交数量
        >> side           	String  	询价单方向，buy或者sell。
        >> fee            	String  	手续费，正数代表平台返佣 ，负数代表平台扣除
        >> feeCcy         	String  	手续费币种
        >> tradeId        	String  	最新的成交Id.
        '''
        return self.send_request(*_BlockTradeEndpoints.set_execute_quote, **to_local(locals()))

    # 获取可报价产品
    def get_maker_instrument_settings(self, proxies={}, proxy_host: str = None):
        '''
        用于maker查询特定的接受询价和报价的产品, 以及数量和价格范围。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-get-quote-products
        
        
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功
        msg               	String  	错误信息，如果代码不为0，则不为空
        data              	Array of objects	请求返回值，包含请求结果
        instType          	String  	产品类别，枚举值包括FUTURES,OPTION,SWAP和SPOT
        includeAll        	Boolean 	是否接收该instType下所有产品。有效值为true或false。默认false。
        > data            	Array of objects	instType的元素
        >> instFamily     	String  	交易品种交割/永续/期权情况下必填
        >> instId         	String  	产品ID，如BTC-USDT。对SPOT产品类别有效且必须。
        >> maxBlockSz     	String  	该种产品最大可交易数量。FUTURES, OPTION and SWAP 的单位是合约数量。SPOT的单位是交易货币。
        >> makerPxBand    	String  	价格限制以价格精度tick为单位，以标记价格为基准。设置makerPxBand为1个tick代表:如果买一价  > 标记价格 + 1 tick, 操作将被拦截如果 买一价 < 标记价格 - 1 tick, 操作将被拦截
        '''
        return self.send_request(*_BlockTradeEndpoints.get_maker_instrument_settings, **to_local(locals()))

    # 设置可报价产品
    def set_maker_instrument_settings(self, instType: str, data: object, includeAll: bool = '', proxies={},
                                      proxy_host: str = None):
        '''
        用于maker设置特定的接受询价和报价的产品, 以及数量和价格范围。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-set-quote-products
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类别，枚举值包括FUTURES,OPTION,SWAP和SPOT
        includeAll        	Boolean 	否       	是否接收该instType下所有产品。有效值为true或false。默认false。
        data              	Array of objects	是       	instType的元素
        > instFamily      	String  	可选      	交易品种交割/永续/期权情况下必填
        > instId          	String  	可选      	产品ID，如BTC-USDT。对SPOT产品类别有效且必须。
        > maxBlockSz      	String  	否       	该种产品最大可交易数量。FUTURES, OPTION and SWAP 的单位是合约数量。SPOT的单位是交易货币。
        > makerPxBand     	String  	否       	价格限制以价格精度tick为单位，以标记价格为基准。以设置makerPxBand为1个tick为例:如果买价  > 标记价格 + 1 tick, 操作将被拦截如果卖价 < 标记价格 - 1 tick, 操作将被拦截
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功
        msg               	String  	错误信息，如果代码不为0，则不为空
        data              	Array of objects	请求返回值，包含请求结果
        > result          	Boolean 	请求结果，枚举值为true,false
        '''
        return self.send_request(*_BlockTradeEndpoints.set_maker_instrument_settings, **to_local(locals()))

    # 重设MMP状态
    def set_mmp_reset(self, proxies={}, proxy_host: str = None):
        '''
        重设MMP状态为无效。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-reset-mmp-status
        
        
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功
        msg               	String  	错误信息，如果代码不为0，则不为空
        data              	Array of objects	请求返回值，包含请求结果
        ts                	String  	重设时间. Unix 时间戳的毫秒数格式，如1597026383085.
        '''
        return self.send_request(*_BlockTradeEndpoints.set_mmp_reset, **to_local(locals()))

    # 报价
    def set_create_quote(self, rfqId: str, quoteSide: str, legs: object, clQuoteId: str = '', tag: str = '',
                         anonymous: bool = '', expiresIn: str = '', proxies={}, proxy_host: str = None):
        '''
        允许询价单指定的报价方进行报价，需要对整个询价单报价，不允许部分报价。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-create-quote
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        rfqId             	String  	是       	询价单ID
        clQuoteId         	String  	否       	报价单自定义ID
        tag               	String  	否       	报价单标签，与此报价单关联的大宗交易将有相同的标签。字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        anonymous         	Boolean 	否       	是否匿名报价，true表示匿名报价，false表示公开报价，默认值为false，为true时，即使在交易执行之后，身份也不会透露给询价方。
        quoteSide         	String  	是       	报价单方向，buy或者sell。当报价单方向为buy，对maker来说，执行方向与legs里的方向相同，对taker来说相反。反之同理
        expiresIn         	String  	否       	报价单的有效时长（以秒为单位）。 10到120之间的任何整数。 默认值为60
        legs              	Array of objects	是       	组合交易
        > instId          	String  	是       	产品ID
        > tdMode          	String  	否       	交易模式保证金模式：cross全仓isolated逐仓非保证金模式：cash非保证金.如未提供，tdMode 将继承系统设置的默认值：单币种保证金模式 & 现货:cash单币种保证金和多币种保证金模式下买入期权：isolated其他情况:cross
        > ccy             	String  	否       	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单在其他情况下该参数将被忽略。
        > sz              	String  	是       	委托数量
        > px              	String  	是       	委托价格
        > side            	String  	是       	报价单方向
        > posSide         	String  	否       	持仓方向买卖模式下默认为net。在开平仓模式下仅可选择long或short。如未指定，则处于开平仓模式下的用户始终会开新仓位。仅适用交割、永续。
        > tgtCcy          	String  	否       	委托数量的类型定义sz属性的单位。仅适用于 instType=SPOT。有效值为base_ccy和quote_ccy。未指定时，默认为base_ccy。
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功。
        msg               	String  	错误信息，如果代码不为0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > cTime           	String  	报价单创建时间，Unix时间戳的毫秒数格式。
        > uTime           	String  	报价单状态更新时间，Unix时间戳的毫秒数格式。
        > state           	String  	报价单的状态有效值为activecanceledpending_fillfilledexpiredfailed
        > reason          	String  	状态原因. 有效值包括mmp_canceled.
        > validUntil      	String  	报价单的过期时间，Unix时间戳的毫秒数格式。
        > rfqId           	String  	询价单ID
        > clRfqId         	String  	询价单自定义ID，为客户敏感信息，不会公开，对报价方返回""。
        > quoteId         	String  	报价单ID
        > clQuoteId       	String  	报价单自定义ID，为客户敏感信息，不会公开，对询价方返回""。
        > tag             	String  	报价单标签，与此报价单关联的大宗交易将有相同的标签。
        > traderCode      	String  	报价方唯一标识代码。
        > quoteSide       	String  	报价单方向，有效值为buy或者sell。当报价单方向为buy，对maker来说，执行方向与legs里的方向相同，对taker来说相反。反之同理。
        > legs            	Array of objects	组合交易
        >> instId         	String  	产品ID
        >> tdMode         	String  	交易模式保证金模式：cross全仓isolated逐仓非保证金模式：cash非保证金.如未提供，tdMode 将继承系统设置的默认值：单币种保证金模式 & 现货:cash单币种保证金和多币种保证金模式下买入期权：isolated其他情况:cross
        >> ccy            	String  	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单在其他情况下该参数将被忽略。
        >> sz             	String  	委托数量
        >> px             	String  	委托价格
        >> side           	String  	腿的方向，有效值为buy或者sell。
        >> posSide        	String  	持仓方向买卖模式下默认为net。如未指定，则返回""，相当于net。在开平仓模式下仅可选择long或short。 如未指定，则返回""，对应于为交易开新仓位的方向（买入=>long，卖出=>short）。仅适用交割、永续。
        >> tgtCcy         	String  	委托数量的类型定义sz属性的单位。仅适用于 instType=SPOT。有效值为base_ccy和quote_ccy。未指定时，默认为base_ccy。
        '''
        return self.send_request(*_BlockTradeEndpoints.set_create_quote, **to_local(locals()))

    # 取消报价单
    def set_cancel_quote(self, quoteId: str = '', clQuoteId: str = '', rfqId: str = '', proxies={},
                         proxy_host: str = None):
        '''
        取消一个报价单。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-cancel-quote
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        quoteId           	String  	可选      	报价单ID
        clQuoteId         	String  	可选      	报价单自定义ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间，当 clRfqId 和 rfqId 都传时，以 rfqId 为准。
        rfqId             	String  	否       	询价单ID
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > quoteId         	String  	报价单ID
        > clQuoteId       	String  	询价单自定义ID
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败时的msg
        '''
        return self.send_request(*_BlockTradeEndpoints.set_cancel_quote, **to_local(locals()))

    # 批量取消报价单
    def set_cancel_batch_quotes(self, quoteIds: object = '', clQuoteIds: object = '', proxies={},
                                proxy_host: str = None):
        '''
        取消一个或多个报价单，每次最多可以撤销100个订单。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-cancel-multiple-quotes
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        quoteIds          	Array of strings	可选      	报价单ID
        clQuoteIds        	Array of strings	可选      	报价单自定义ID，当 clQuoteIds 和 quoteIds 都传时，以 quoteIds 为准。
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > quoteId         	String  	报价单ID
        > clQuoteId       	String  	报价单自定义ID
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败时的msg
        '''
        return self.send_request(*_BlockTradeEndpoints.set_cancel_batch_quotes, **to_local(locals()))

    # 取消所有报价单
    def set_cancel_all_quotes(self, proxies={}, proxy_host: str = None):
        '''
        取消所有报价单
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-cancel-all-quotes
        
        
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > ts              	String  	成功取消时间，Unix时间戳的毫秒数格式，例如 1597026383085。
        '''
        return self.send_request(*_BlockTradeEndpoints.set_cancel_all_quotes, **to_local(locals()))

    # 获取询价单信息
    def get_rfqs(self, rfqId: str = '', clRfqId: str = '', state: str = '', beginId: str = '', endId: str = '',
                 limit: str = '', proxies={}, proxy_host: str = None):
        '''
        获取用户发出的或收到的询价单信息
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-get-rfqs
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        rfqId             	String  	否       	询价单ID .
        clRfqId           	String  	否       	客户询价单自定义ID，当 clRfqId 和 rfqId 都传时，以 rfqId 为准
        state             	String  	否       	询价单的状态activecanceledpending_fillfilledexpiredfailedtraded_awaytraded_away仅适用于报价方
        beginId           	String  	否       	请求的起始询价单ID，请求此ID之后（更新的数据）的分页内容，不包括 beginId
        endId             	String  	否       	请求的结束询价单ID，请求此ID之前（更旧的数据）的分页内容，不包括 endId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > cTime           	String  	询价单创建时间，Unix时间戳的毫秒数格式。
        > uTime           	String  	询价单状态更新时间，Unix时间戳的毫秒数格式。
        > state           	String  	询价单的状态activecanceledpending_fillfilledexpiredfailedtraded_awaytraded_away仅适用于报价方
        > counterparties  	Array of srings	报价方列表
        > validUntil      	String  	询价单的过期时间，Unix时间戳的毫秒数格式。
        > clRfqId         	String  	询价单自定义ID，为客户敏感信息，不会公开，对报价方返回""。
        > tag             	String  	询价单标签，与此询价单关联的大宗交易将有相同的标签。
        > traderCode      	String  	询价方唯一标识代码，询价时 anonymous 设置为true时不可见
        > rfqId           	String  	询价单ID
        > allowPartialExecution	Boolean 	RFQ是否可以被部分执行，如果腿的比例和原RFQ一致。有效值为true或false。未指定时，默认为false。
        > legs            	Array of objects	组合交易，每个请求最多可放置15条腿
        >> instId         	String  	产品ID，例如："BTC-USDT-SWAP"
        >> tdMode         	String  	交易模式保证金模式：cross全仓isolated逐仓非保证金模式：cash非保证金.如未提供，tdMode 将继承系统设置的默认值：单币种保证金模式 & 现货:cash单币种保证金和多币种保证金模式下买入期权：isolated其他情况:cross
        >> ccy            	String  	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单在其他情况下该参数将被忽略。
        >> sz             	String  	委托数量
        >> side           	String  	询价单方向有效值为buy和sell。
        >> posSide        	String  	持仓方向买卖模式下默认为net。如未指定，则返回""，相当于net。在开平仓模式下仅可选择long或short。 如未指定，则返回""，对应于为交易开新仓位的方向（买入=>long，卖出=>short）。仅适用交割、永续。
        >> tgtCcy         	String  	委托数量的类型定义sz属性的单位。仅适用于 instType=SPOT。有效值为base_ccy和quote_ccy。未指定时，默认为base_ccy。
        '''
        return self.send_request(*_BlockTradeEndpoints.get_rfqs, **to_local(locals()))

    # 获取报价单信息
    def get_quotes(self, rfqId: str = '', clRfqId: str = '', quoteId: str = '', clQuoteId: str = '', state: str = '',
                   beginId: str = '', endId: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        获取用户发出的或收到的报价单信息
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-get-quotes
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        rfqId             	String  	否       	询价单ID
        clRfqId           	String  	否       	询价单自定义ID， 当 clRfqId 和 rfqId 都传时，以 rfqId 为准。
        quoteId           	String  	否       	报价单ID
        clQuoteId         	String  	否       	报价单自定义ID，当 clRfqId 和 rfqId 都传时，以 rfqId 为准。
        state             	String  	否       	报价单的状态有效值为activecanceledpending_fillfilledexpiredfailed
        beginId           	String  	否       	请求的起始报价单ID，请求此ID之后（更新的数据）的分页内容，不包括 beginId
        endId             	String  	否       	请求的结束报价单ID，请求此ID之前（更旧的数据）的分页内容，不包括 endId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的数组
        > cTime           	String  	报价单创建时间，Unix时间戳的毫秒数格式
        > uTime           	String  	报价单状态更新时间，Unix时间戳的毫秒数格式。
        > state           	String  	报价单的状态activecanceledpending_fillfilledexpiredfailed
        > reason          	String  	状态原因. 有效值包括mmp_canceled.
        > validUntil      	String  	报价单的过期时间，Unix时间戳的毫秒数格式。
        > rfqId           	String  	询价单ID
        > clRfqId         	String  	询价单自定义ID，为客户敏感信息，不会公开，对报价方返回""。
        > quoteId         	String  	报价单ID
        > clQuoteId       	String  	报价单自定义ID，为客户敏感信息，不会公开，对询价方返回""。
        > tag             	String  	报价单标签，与此报价单关联的大宗交易将有相同的标签。
        > traderCode      	String  	报价方唯一标识代码，报价时 Anonymous 设置为True时不可见。
        > quoteSide       	String  	报价单方向，buy或者sell。当报价单方向为buy，对maker来说，执行方向与legs里的方向相同，对taker来说相反。反之同理
        > legs            	Array of objects	组合交易
        >> instId         	String  	产品ID
        >> tdMode         	String  	交易模式保证金模式：cross全仓isolated逐仓非保证金模式：cash非保证金.如未提供，tdMode 将继承系统设置的默认值：单币种保证金模式 & 现货:cash单币种保证金和多币种保证金模式下买入期权：isolated其他情况:cross
        >> ccy            	String  	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单在其他情况下该参数将被忽略。
        >> sz             	String  	委托数量
        >> px             	String  	委托价格.
        >> side           	String  	报价单方向
        >> posSide        	String  	持仓方向买卖模式下默认为net。如未指定，则返回""，相当于net。在开平仓模式下仅可选择long或short。 如未指定，则返回""，对应于为交易开新仓位的方向（买入=>long，卖出=>short）。仅适用交割、永续。
        >> tgtCcy         	String  	委托数量的类型定义sz属性的单位。仅适用于 instType=SPOT。有效值为base_ccy和quote_ccy。未指定时，默认为base_ccy。
        '''
        return self.send_request(*_BlockTradeEndpoints.get_quotes, **to_local(locals()))

    # 获取大宗交易信息
    def get_trades(self, rfqId: str = '', clRfqId: str = '', quoteId: str = '', blockTdId: str = '',
                   clQuoteId: str = '', state: str = '', beginId: str = '', endId: str = '', beginTs: str = '',
                   endTs: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        获取该用户大宗交易成交信息
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-get-trades
        
        
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        rfqId             	String  	否       	询价单ID
        clRfqId           	String  	否       	由用户设置的询价单ID. 如果clRfqId和rfqId都通过了，rfqId 将被视为主要
        quoteId           	String  	否       	报价单ID
        blockTdId         	String  	否       	大宗交易ID
        clQuoteId         	String  	否       	由用户设置的报价单ID。如果同时传递了clQuoteId和quoteId，则 quoteId 将被视为主要标识符
        state             	String  	否       	询价单的状态activecanceledpending_fillfilledexpiredfailedtraded_awaytraded_away仅适用于报价方
        beginId           	String  	否       	请求的起始大宗交易ID，请求此ID之后（更新的数据）的分页内容，不包括 beginId
        endId             	String  	否       	请求的结束大宗交易ID，请求此ID之前（更旧的数据）的分页内容，不包括 endId
        beginTs           	String  	否       	用开始时间戳筛选交易执行时间（UTC时区）。Unix时间戳的毫秒数格式，例如 1597026383085。
        endTs             	String  	否       	用结束时间戳筛选交易执行时间（UTC时区）。Unix时间戳的毫秒数格式，例如 1597026383085。
        limit             	String  	否       	返回结果的数量，最大为100，默认100条。如果请求范围内的交易数量大于100，则返回该范围内最近的100笔交易。
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组
        > cTime           	String  	执行创建的时间，Unix时间戳的毫秒数格式。
        > rfqId           	String  	询价单ID
        > clRfqId         	String  	询价单自定义ID，为客户敏感信息，不会公开，对报价方返回""。
        > quoteId         	String  	报价单ID
        > clQuoteId       	String  	报价单自定义ID，为客户敏感信息，不会公开，对询价方返回""。
        > blockTdId       	String  	大宗交易ID
        > tag             	String  	交易标签，大宗交易将有与其对应的询价单或报价单相同的标签。
        > tTraderCode     	String  	询价方唯一标识代码，询价时 anonymous 设置为true时不可见
        > mTraderCode     	String  	报价方唯一标识代码。报价时 anonymous 设置为true时不可见
        > legs            	Array of objects	组合交易
        >> instId         	String  	产品ID
        >> px             	String  	成交价格
        >> sz             	String  	成交数量
        >> side           	String  	询价单方向，buy 或者 sell。
        >> fee            	String  	手续费，正数代表平台返佣 ，负数代表平台扣除
        >> feeCcy         	String  	手续费币种
        >> tradeId        	String  	最新的成交Id
        '''
        return self.send_request(*_BlockTradeEndpoints.get_trades, **to_local(locals()))

    # 获取大宗交易公共成交数据
    def get_public_trades(self, beginId: str = '', endId: str = '', limit: str = '', proxies={},
                          proxy_host: str = None):
        '''
        获取最近执行的大宗交易。
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-get-public-trades
        
        
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        beginId           	String  	否       	请求的起始大宗交易ID，请求此ID之后（更新的数据）的分页内容，不包括 beginId
        endId             	String  	否       	请求的结束大宗交易ID，请求此ID之前（更旧的数据）的分页内容，不包括 endId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0 表示成功。
        msg               	String  	错误信息，如果代码不为 0，则不为空。
        data              	Array of objects	包含结果的对象数组.
        > cTime           	String  	执行创建的时间，Unix时间戳的毫秒数格式。
        > blockTdId       	String  	大宗交易ID
        > legs            	Array of objects	组合交易
        >> instId         	String  	产品ID
        >> px             	String  	成交价格
        >> sz             	String  	成交数量
        >> side           	String  	询价单方向，从 Taker的视角看
        >> tradeId        	String  	最新成交ID
        '''
        return self.send_request(*_BlockTradeEndpoints.get_public_trades, **to_local(locals()))

    # 获取大宗交易所有产品行情信息
    def get_block_tickers(self, instType: str, uly: str = '', instFamily: str = '', proxies={}, proxy_host: str = None):
        '''
        获取最近24小时大宗交易量
        https://www.okx.com/docs-v5/zh/#block-trading-rest-api-get-block-tickers
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数适用于交割/永续/期权，如BTC-USD
        instFamily        	String  	否       	交易品种适用于交割/永续/期权，如BTC-USD
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        instType          	String  	产品类型
        volCcy24h         	String  	24小时成交量，以币为单位如果是衍生品合约，数值为交易货币的数量。如果是币币/币币杠杆，数值为计价货币的数量。
        vol24h            	String  	24小时成交量，以张为单位如果是衍生品合约，数值为合约的张数。如果是币币/币币杠杆，数值为交易货币的数量。
        ts                	String  	数据产生时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_BlockTradeEndpoints.get_block_tickers, **to_local(locals()))

    # 获取大宗交易单个产品行情信息
    def get_block_ticker(self, instId: str, proxies={}, proxy_host: str = None):
        '''
        获取最近24小时大宗交易量
        https://www.okx.com/docs-v5/zh/#central-limit-orderbook-market-data-get-block-ticker
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-SWAP
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        instType          	String  	产品类型
        volCcy24h         	String  	24小时成交量，以币为单位如果是衍生品合约，数值为交易货币的数量。如果是币币/币币杠杆，数值为计价货币的数量。
        vol24h            	String  	24小时成交量，以张为单位如果是衍生品合约，数值为合约的张数。如果是币币/币币杠杆，数值为交易货币的数量。
        ts                	String  	数据产生时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_BlockTradeEndpoints.get_block_ticker, **to_local(locals()))

    # 获取大宗交易公共成交数据
    def get_block_trades(self, instId: str, proxies={}, proxy_host: str = None):
        '''
        查询市场上的成交信息数据，根据 tradeId 倒序排序。
        https://www.okx.com/docs-v5/zh/#central-limit-orderbook-market-data-get-block-trades
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        tradeId           	String  	成交ID
        px                	String  	成交价格
        sz                	String  	成交数量
        side              	String  	成交方向buy：买sell：卖
        ts                	String  	成交时间，Unix时间戳的毫秒数格式， 如1597026383085
        '''
        return self.send_request(*_BlockTradeEndpoints.get_block_trades, **to_local(locals()))

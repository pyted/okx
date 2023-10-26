'''
策略交易
https://www.okx.com/docs-v5/zh/#order-book-trading-algo-trading
'''

from paux.param import to_local
from okx.api._client import Client


class _AlgoTradeEndpoints():
    set_order_algo = ['/api/v5/trade/order-algo', 'POST']  # POST / 策略委托下单
    set_cancel_algos = ['/api/v5/trade/cancel-algos', 'POST']  # POST / 撤销策略委托订单
    set_amend_algos = ['/api/v5/trade/amend-algos', 'POST']  # POST / 修改策略委托订单
    set_cancel_advance_algos = ['/api/v5/trade/cancel-advance-algos', 'POST']  # POST / 撤销高级策略委托订单
    get_order_algo = ['/api/v5/trade/order-algo', 'GET']  # GET / 获取策略委托单信息
    get_orders_algo_pending = ['/api/v5/trade/orders-algo-pending', 'GET']  # GET / 获取未完成策略委托单列表
    get_orders_algo_history = ['/api/v5/trade/orders-algo-history', 'GET']  # GET / 获取历史策略委托单列表


class AlgoTrade(Client):

    # POST / 策略委托下单
    def set_order_algo(self, instId: str, tdMode: str, side: str, ordType: str, ccy: str = '', posSide: str = '',
                       sz: str = '', tag: str = '', tgtCcy: str = '', algoClOrdId: str = '', closeFraction: str = '',
                       proxies={}, proxy_host: str = None):
        '''
        提供单向止盈止损委托、双向止盈止损委托、计划委托、时间加权委托、移动止盈止损委托
        https://www.okx.com/docs-v5/zh/#order-book-trading-algo-trading-post-place-algo-order
        
        限速：20次/2s跟单交易带单合约的限速：1次/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-190927-5000-C
        tdMode            	String  	是       	交易模式保证金模式isolated：逐仓，cross：全仓非保证金模式cash：非保证金
        ccy               	String  	否       	保证金币种仅适用于单币种保证金模式下的全仓杠杆订单
        side              	String  	是       	订单方向buy：买sell：卖
        posSide           	String  	可选      	持仓方向在开平仓模式下必填，且仅可选择long或short
        ordType           	String  	是       	订单类型conditional：单向止盈止损oco：双向止盈止损trigger：计划委托move_order_stop：移动止盈止损twap：时间加权委托
        sz                	String  	可选      	委托数量sz和closeFraction必填且只能填其一
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间
        tgtCcy            	String  	否       	委托数量的类型base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币单向止盈止损市价买单默认买为计价货币，卖为交易货币
        algoClOrdId       	String  	否       	客户自定义策略订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        closeFraction     	String  	可选      	策略委托触发时，平仓的百分比。1 代表100%现在系统只支持全部平仓，唯一接受参数为1对于同一个仓位，仅支持一笔全部平仓的止盈止损挂单仅适用于交割或永续当posSide=net时，reduceOnly必须为true仅适用于止盈止损ordType=conditional或oco仅适用于止盈止损市价订单不支持组合保证金模式sz和closeFraction必填且只能填其一
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	策略委托单ID
        clOrdId           	String  	客户自定义订单ID（已废弃）
        algoClOrdId       	String  	客户自定义策略订单ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        tag               	String  	订单标签
        '''
        return self.send_request(*_AlgoTradeEndpoints.set_order_algo, **to_local(locals()))

    # POST / 撤销策略委托订单
    def set_cancel_algos(self, algoId: str, instId: str, proxies={}, proxy_host: str = None):
        '''
        撤销策略委托订单（不包含冰山委托、时间加权、移动止盈止损等高级策略订单），每次最多可以撤销10个策略委托单
        https://www.okx.com/docs-v5/zh/#order-book-trading-algo-trading-post-cancel-algo-order
        
        限速：20次/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略委托单ID
        instId            	String  	是       	产品ID 如BTC-USDT
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	订单ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        '''
        return self.send_request(*_AlgoTradeEndpoints.set_cancel_algos, **to_local(locals()))

    # POST / 修改策略委托订单
    def set_amend_algos(self, instId: str, algoId: str = '', algoClOrdId: str = '', cxlOnFail: bool = '',
                        reqId: str = '', newSz: str = '', newTpTriggerPx: str = '', newTpOrdPx: str = '',
                        newSlTriggerPx: str = '', newSlOrdPx: str = '', newTpTriggerPxType: str = '',
                        newSlTriggerPxType: str = '', proxies={}, proxy_host: str = None):
        '''
        修改策略委托订单（仅支持止盈止损单，不包含计划委托、冰山委托、时间加权、移动止盈止损等订单）<!- 1-2-3 -->只适用于交割和永续合约。
        https://www.okx.com/docs-v5/zh/#order-book-trading-algo-trading-post-amend-algo-order
        
        限速：20次/2s
        限速规则：UserID + Instrument ID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID
        algoId            	String  	可选      	策略委托单IDalgoId和algoClOrdId必须传一个，若传两个，以algoId为主
        algoClOrdId       	String  	可选      	客户自定义策略订单IDalgoId和algoClOrdId必须传一个，若传两个，以algoId为主
        cxlOnFail         	Boolean 	否       	false：不自动撤单 true：自动撤单 当订单修改失败时，该订单是否需要自动撤销。默认为false
        reqId             	String  	否       	用户自定义修改事件ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间
        newSz             	String  	可选      	修改的新数量
        newTpTriggerPx    	String  	可选      	止盈触发价如果止盈触发价或者委托价为0，那代表删除止盈
        newTpOrdPx        	String  	可选      	止盈委托价委托价格为-1时，执行市价止盈
        newSlTriggerPx    	String  	可选      	止损触发价如果止损触发价或者委托价为0，那代表删除止损
        newSlOrdPx        	String  	可选      	止损委托价委托价格为-1时，执行市价止损
        newTpTriggerPxType	String  	可选      	止盈触发价类型last：最新价格index：指数价格mark：标记价格
        newSlTriggerPxType	String  	可选      	止损触发价类型last：最新价格index：指数价格mark：标记价格
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	订单ID
        algoClOrdId       	String  	客户自定义策略订单ID
        reqId             	String  	用户自定义修改事件ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        '''
        return self.send_request(*_AlgoTradeEndpoints.set_amend_algos, **to_local(locals()))

    # POST / 撤销高级策略委托订单
    def set_cancel_advance_algos(self, algoId: str, instId: str, proxies={}, proxy_host: str = None):
        '''
        撤销冰山委托、时间加权、移动止盈止损委托订单，每次最多可以撤销10个策略委托单
        https://www.okx.com/docs-v5/zh/#order-book-trading-algo-trading-post-cancel-advance-algo-order
        
        限速：20次/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	是       	策略委托单ID
        instId            	String  	是       	产品ID 如BTC-USDT
        返回参数:
        Parameter         	Type    	Description
        algoId            	String  	订单ID
        sCode             	String  	事件执行结果的code，0代表成功
        sMsg              	String  	事件执行失败时的msg
        '''
        return self.send_request(*_AlgoTradeEndpoints.set_cancel_advance_algos, **to_local(locals()))

    # GET / 获取策略委托单信息
    def get_order_algo(self, algoId: str = '', algoClOrdId: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/trade/order-algo
        https://www.okx.com/docs-v5/zh/#order-book-trading-algo-trading-get-algo-order-details
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	可选      	策略委托单IDalgoId和algoClOrdId必须传一个，若传两个，以algoId为主
        algoClOrdId       	String  	可选      	客户自定义策略订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品ID
        ccy               	String  	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        ordId             	String  	最新一笔订单ID
        ordIdList         	String  	订单ID列表，当止盈止损存在市价拆单时，会有多个。
        algoId            	String  	策略委托单ID
        clOrdId           	String  	客户自定义订单ID
        sz                	String  	委托数量
        closeFraction     	String  	策略委托触发时，平仓的百分比。1 代表100%
        ordType           	String  	订单类型
        side              	String  	订单方向
        posSide           	String  	持仓方向
        tdMode            	String  	交易模式
        tgtCcy            	String  	币币市价单委托数量sz的单位base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币市价订单默认买单为quote_ccy，卖单为base_ccy
        state             	String  	订单状态live：待生效pause：暂停生效partially_effective:部分生效effective： 已生效canceled：已撤销order_failed：委托失败partially_failed：部分委托失败
        lever             	String  	杠杆倍数，0.01到125之间的数值，仅适用于币币杠杆/交割/永续
        tpTriggerPx       	String  	止盈触发价
        tpTriggerPxType   	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格
        tpOrdPx           	String  	止盈委托价
        slTriggerPx       	String  	止损触发价
        slTriggerPxType   	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格
        slOrdPx           	String  	止损委托价
        triggerPx         	String  	计划委托触发价格
        triggerPxType     	String  	计划委托触发价格类型last：最新价格index：指数价格mark：标记价格
        ordPx             	String  	订单委托价格
        actualSz          	String  	实际委托量
        actualPx          	String  	实际委托价
        actualSide        	String  	实际触发方向tp：止盈sl： 止损
        triggerTime       	String  	策略委托触发时间，Unix时间戳的毫秒数格式，如1597026383085
        pxVar             	String  	价格比例仅适用于冰山委托和时间加权委托
        pxSpread          	String  	价距仅适用于冰山委托和时间加权委托
        szLimit           	String  	单笔数量仅适用于冰山委托和时间加权委托
        pxLimit           	String  	挂单限制价仅适用于冰山委托和时间加权委托
        tag               	String  	订单标签
        timeInterval      	String  	下单间隔仅适用于时间加权委托
        callbackRatio     	String  	回调幅度的比例仅适用于移动止盈止损
        callbackSpread    	String  	回调幅度的价距仅适用于移动止盈止损
        activePx          	String  	移动止盈止损激活价格仅适用于移动止盈止损
        moveTriggerPx     	String  	移动止盈止损触发价格仅适用于移动止盈止损
        reduceOnly        	String  	是否只减仓，true或false
        quickMgnType      	String  	一键借币类型，仅适用于杠杆逐仓的一键借币模式manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币
        last              	String  	下单时的最新成交价
        failCode          	String  	代表策略触发失败的原因，已撤销和已生效时为""，委托失败时有值，如 51008；仅适用于单向止盈止损委托、双向止盈止损委托、移动止盈止损委托、计划委托。
        algoClOrdId       	String  	客户自定义策略订单ID
        attachAlgoOrds    	Array of object	附带止盈止损信息适用于单币种保证金模式/跨币种保证金/模式组合保证金模式
        > attachAlgoClOrdId	String  	下单附带止盈止损时，客户自定义的策略订单ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。订单完全成交，下止盈止损委托单时，该值会传给algoClOrdId。
        > tpTriggerPx     	String  	止盈触发价，如果填写此参数，必须填写止盈委托价
        > tpTriggerPxType 	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        > tpOrdPx         	String  	止盈委托价，如果填写此参数，必须填写止盈触发价委托价格为-1时，执行市价止盈
        > slTriggerPx     	String  	止损触发价，如果填写此参数，必须填写止损委托价
        > slTriggerPxType 	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        > slOrdPx         	String  	止损委托价，如果填写此参数，必须填写止损触发价委托价格为-1时，执行市价止损
        cTime             	String  	订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_AlgoTradeEndpoints.get_order_algo, **to_local(locals()))

    # GET / 获取未完成策略委托单列表
    def get_orders_algo_pending(self, ordType: str, algoId: str = '', instType: str = '', instId: str = '',
                                after: str = '', before: str = '', limit: str = '', algoClOrdId: str = '', proxies={},
                                proxy_host: str = None):
        '''
        获取当前账户下未触发的策略委托单列表
        https://www.okx.com/docs-v5/zh/#order-book-trading-algo-trading-get-algo-order-list
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        algoId            	String  	否       	策略委托单ID
        instType          	String  	否       	产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约MARGIN：杠杆
        instId            	String  	否       	产品ID，BTC-USD-190927
        ordType           	String  	是       	订单类型conditional：单向止盈止损oco：双向止盈止损trigger：计划委托move_order_stop：移动止盈止损iceberg：冰山委托twap：时间加权委托
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        algoClOrdId       	String  	否       	客户自定义策略订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品ID
        ccy               	String  	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        ordId             	String  	最新一笔订单ID
        ordIdList         	String  	订单ID列表，当止盈止损存在市价拆单时，会有多个。
        algoId            	String  	策略委托单ID
        clOrdId           	String  	客户自定义订单ID
        sz                	String  	委托数量
        closeFraction     	String  	策略委托触发时，平仓的百分比。1 代表100%
        ordType           	String  	订单类型
        side              	String  	订单方向
        posSide           	String  	持仓方向
        tdMode            	String  	交易模式
        tgtCcy            	String  	币币市价单委托数量sz的单位base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币市价订单默认买单为quote_ccy，卖单为base_ccy
        state             	String  	订单状态 ，live：待生效pause：暂停生效
        lever             	String  	杠杆倍数，0.01到125之间的数值，仅适用于币币杠杆/交割/永续
        tpTriggerPx       	String  	止盈触发价
        tpTriggerPxType   	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格
        tpOrdPx           	String  	止盈委托价
        slTriggerPx       	String  	止损触发价
        slTriggerPxType   	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格
        slOrdPx           	String  	止损委托价
        triggerPx         	String  	计划委托触发价格
        triggerPxType     	String  	计划委托触发价类型last：最新价格index：指数价格mark：标记价格
        ordPx             	String  	计划委托委托价格
        actualSz          	String  	实际委托量
        actualPx          	String  	实际委托价
        actualSide        	String  	实际触发方向，tp：止盈sl： 止损
        triggerTime       	String  	策略委托触发时间，Unix时间戳的毫秒数格式，如1597026383085
        pxVar             	String  	价格比例仅适用于冰山委托和时间加权委托
        pxSpread          	String  	价距仅适用于冰山委托和时间加权委托
        szLimit           	String  	单笔数量仅适用于冰山委托和时间加权委托
        tag               	String  	订单标签
        pxLimit           	String  	挂单限制价仅适用于冰山委托和时间加权委托
        timeInterval      	String  	下单间隔仅适用于时间加权委托
        callbackRatio     	String  	回调幅度的比例仅适用于移动止盈止损
        callbackSpread    	String  	回调幅度的价距仅适用于移动止盈止损
        activePx          	String  	移动止盈止损激活价格仅适用于移动止盈止损
        moveTriggerPx     	String  	移动止盈止损触发价格仅适用于移动止盈止损
        reduceOnly        	String  	是否只减仓，true或false
        quickMgnType      	String  	一键借币类型，仅适用于杠杆逐仓的一键借币模式manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币
        last              	String  	下单时的最新成交价
        failCode          	String  	代表策略触发失败的原因，委托失败时有值，如 51008，对于该接口一直为""。
        algoClOrdId       	String  	客户自定义策略订单ID
        attachAlgoOrds    	Array of object	附带止盈止损信息适用于单币种保证金模式/跨币种保证金/模式组合保证金模式
        > attachAlgoClOrdId	String  	下单附带止盈止损时，客户自定义的策略订单ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。订单完全成交，下止盈止损委托单时，该值会传给algoClOrdId。
        > tpTriggerPx     	String  	止盈触发价，如果填写此参数，必须填写止盈委托价
        > tpTriggerPxType 	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        > tpOrdPx         	String  	止盈委托价，如果填写此参数，必须填写止盈触发价委托价格为-1时，执行市价止盈
        > slTriggerPx     	String  	止损触发价，如果填写此参数，必须填写止损委托价
        > slTriggerPxType 	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        > slOrdPx         	String  	止损委托价，如果填写此参数，必须填写止损触发价委托价格为-1时，执行市价止损
        cTime             	String  	订单创建时间，   Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_AlgoTradeEndpoints.get_orders_algo_pending, **to_local(locals()))

    # GET / 获取历史策略委托单列表
    def get_orders_algo_history(self, ordType: str, state: str = '', algoId: str = '', instType: str = '',
                                instId: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                                proxy_host: str = None):
        '''
        获取最近3个月当前账户下所有策略委托单列表
        https://www.okx.com/docs-v5/zh/#order-book-trading-algo-trading-get-algo-order-history
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ordType           	String  	是       	订单类型conditional：单向止盈止损oco：双向止盈止损trigger：计划委托move_order_stop：移动止盈止损iceberg：冰山委托twap：时间加权委托
        state             	String  	可选      	订单状态effective：已生效canceled：已经撤销order_failed：委托失败state和algoId必填且只能填其一
        algoId            	String  	可选      	策略委托单ID
        instType          	String  	否       	产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约MARGIN：杠杆
        instId            	String  	否       	产品ID，BTC-USD-190927
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品ID
        ccy               	String  	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        ordId             	String  	最新一笔订单ID
        ordIdList         	String  	订单ID列表，当止盈止损存在市价拆单时，会有多个。
        algoId            	String  	策略委托单ID
        clOrdId           	String  	客户自定义订单ID
        sz                	String  	委托数量
        closeFraction     	String  	策略委托触发时，平仓的百分比。1 代表100%
        ordType           	String  	订单类型
        side              	String  	订单方向
        posSide           	String  	持仓方向
        tdMode            	String  	交易模式
        tgtCcy            	String  	币币市价单委托数量sz的单位base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币市价订单默认买单为quote_ccy，卖单为base_ccy
        state             	String  	订单状态effective： 已生效canceled：已撤销order_failed：委托失败partially_failed：部分委托失败
        lever             	String  	杠杆倍数，0.01到125之间的数值，仅适用于币币杠杆/交割/永续
        tpTriggerPx       	String  	止盈触发价
        tpTriggerPxType   	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格
        tpOrdPx           	String  	止盈委托价
        slTriggerPx       	String  	止损触发价
        slTriggerPxType   	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格
        slOrdPx           	String  	止损委托价
        triggerPx         	String  	计划委托触发价格
        triggerPxType     	String  	计划委托触发价格
        ordPx             	String  	计划委托委托价格类型last：最新价格index：指数价格mark：标记价格
        actualSz          	String  	实际委托量
        actualPx          	String  	实际委托价
        actualSide        	String  	实际触发方向tp：止盈sl： 止损
        triggerTime       	String  	策略委托触发时间，Unix时间戳的毫秒数格式，如1597026383085
        pxVar             	String  	价格比例仅适用于冰山委托和时间加权委托
        pxSpread          	String  	价距仅适用于冰山委托和时间加权委托
        szLimit           	String  	单笔数量仅适用于冰山委托和时间加权委托
        pxLimit           	String  	挂单限制价仅适用于冰山委托和时间加权委托
        tag               	String  	订单标签
        timeInterval      	String  	下单间隔仅适用于时间加权委托
        callbackRatio     	String  	回调幅度的比例仅适用于移动止盈止损
        callbackSpread    	String  	回调幅度的价距仅适用于移动止盈止损
        activePx          	String  	移动止盈止损激活价格仅适用于移动止盈止损
        moveTriggerPx     	String  	移动止盈止损触发价格仅适用于移动止盈止损
        reduceOnly        	String  	是否只减仓，true或false
        quickMgnType      	String  	一键借币类型，仅适用于杠杆逐仓的一键借币模式manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币
        last              	String  	下单时的最新成交价
        failCode          	String  	代表策略触发失败的原因，已撤销和已生效时为""，委托失败时有值，如 51008；仅适用于单向止盈止损委托、双向止盈止损委托、移动止盈止损委托、计划委托。
        algoClOrdId       	String  	客户自定义策略订单ID
        attachAlgoOrds    	Array of object	附带止盈止损信息适用于单币种保证金模式/跨币种保证金/模式组合保证金模式
        > attachAlgoClOrdId	String  	下单附带止盈止损时，客户自定义的策略订单ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。订单完全成交，下止盈止损委托单时，该值会传给algoClOrdId。
        > tpTriggerPx     	String  	止盈触发价，如果填写此参数，必须填写止盈委托价
        > tpTriggerPxType 	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        > tpOrdPx         	String  	止盈委托价，如果填写此参数，必须填写止盈触发价委托价格为-1时，执行市价止盈
        > slTriggerPx     	String  	止损触发价，如果填写此参数，必须填写止损委托价
        > slTriggerPxType 	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        > slOrdPx         	String  	止损委托价，如果填写此参数，必须填写止损触发价委托价格为-1时，执行市价止损
        cTime             	String  	订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_AlgoTradeEndpoints.get_orders_algo_history, **to_local(locals()))

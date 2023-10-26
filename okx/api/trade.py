'''
交易
https://www.okx.com/docs-v5/zh/#order-book-trading-trade
'''

from paux.param import to_local
from okx.api._client import Client


class _TradeEndpoints():
    set_order = ['/api/v5/trade/order', 'POST']  # POST / 下单
    set_batch_orders = ['/api/v5/trade/batch-orders', 'POST']  # POST / 批量下单
    set_cancel_order = ['/api/v5/trade/cancel-order', 'POST']  # POST / 撤单
    set_cancel_batch_orders = ['/api/v5/trade/cancel-batch-orders', 'POST']  # POST / 批量撤单
    set_amend_order = ['/api/v5/trade/amend-order', 'POST']  # POST / 修改订单
    set_amend_batch_orders = ['/api/v5/trade/amend-batch-orders', 'POST']  # POST / 批量修改订单
    set_close_position = ['/api/v5/trade/close-position', 'POST']  # POST / 市价仓位全平
    get_order = ['/api/v5/trade/order', 'GET']  # GET / 获取订单信息
    get_orders_pending = ['/api/v5/trade/orders-pending', 'GET']  # GET / 获取未成交订单列表
    get_orders_history = ['/api/v5/trade/orders-history', 'GET']  # GET / 获取历史订单记录（近七天）
    get_orders_history_archive = ['/api/v5/trade/orders-history-archive', 'GET']  # GET / 获取历史订单记录（近三个月）
    get_fills = ['/api/v5/trade/fills', 'GET']  # GET / 获取成交明细（近三天）
    get_fills_history = ['/api/v5/trade/fills-history', 'GET']  # GET / 获取成交明细（近三个月）
    set_fills_archive = ['/api/v5/trade/fills-archive', 'POST']  # POST / 申请成交明细（近两年）
    get_fills_archive = ['/api/v5/trade/fills-archive', 'GET']  # GET / 获取成交明细（近两年）
    get_easy_convert_currency_list = ['/api/v5/trade/easy-convert-currency-list', 'GET']  # GET / 获取一键兑换主流币币种列表
    set_easy_convert = ['/api/v5/trade/easy-convert', 'POST']  # POST / 一键兑换主流币交易
    get_easy_convert_history = ['/api/v5/trade/easy-convert-history', 'GET']  # GET / 获取一键兑换主流币历史记录
    get_one_click_repay_currency_list = ['/api/v5/trade/one-click-repay-currency-list', 'GET']  # GET / 获取一键还债币种列表
    set_one_click_repay = ['/api/v5/trade/one-click-repay', 'POST']  # POST / 一键还债交易
    get_one_click_repay_history = ['/api/v5/trade/one-click-repay-history', 'GET']  # GET / 获取一键还债历史记录
    set_mass_cancel = ['/api/v5/trade/mass-cancel', 'POST']  # POST / 撤销 MMP 订单
    set_cancel_all_after = ['/api/v5/trade/cancel-all-after', 'POST']  # POST / 倒计时全部撤单


class Trade(Client):

    # POST / 下单
    def set_order(self, instId: str, tdMode: str, side: str, ordType: str, sz: str, ccy: str = '', clOrdId: str = '',
                  tag: str = '', posSide: str = '', px: str = '', pxUsd: str = '', pxVol: str = '',
                  reduceOnly: bool = '', tgtCcy: str = '', banAmend: bool = '', tpTriggerPx: str = '',
                  tpOrdPx: str = '', attachAlgoClOrdId: str = '', slTriggerPx: str = '', slOrdPx: str = '',
                  tpTriggerPxType: str = '', slTriggerPxType: str = '', quickMgnType: str = '', stpId: str = '',
                  stpMode: str = '', proxies={}, proxy_host: str = None):
        '''
        只有当您的账户有足够的资金才能下单。<!- 1-2-3 -->该接口支持带单合约的下单，但不支持为带单合约平仓。请参考跟单了解更多
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-place-order
        
        限速：60次/2s跟单交易带单合约的限速：4次/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-190927-5000-C
        tdMode            	String  	是       	交易模式保证金模式：isolated：逐仓 ；cross：全仓非保证金模式：cash：非保证金
        ccy               	String  	否       	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        clOrdId           	String  	否       	客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        side              	String  	是       	订单方向buy：买，sell：卖
        posSide           	String  	可选      	持仓方向在开平仓模式下必填，且仅可选择long或short。 仅适用交割、永续。
        ordType           	String  	是       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)
        sz                	String  	是       	委托数量
        px                	String  	可选      	委托价格，仅适用于limit、post_only、fok、ioc、mmp、mmp_and_post_only类型的订单期权下单时，px/pxUsd/pxVol 只能填一个
        pxUsd             	String  	可选      	以USD价格进行期权下单仅适用于期权期权下单时 px/pxUsd/pxVol 必填一个，且只能填一个
        pxVol             	String  	可选      	以隐含波动率进行期权下单，例如 1 代表 100%仅适用于期权期权下单时 px/pxUsd/pxVol 必填一个，且只能填一个
        reduceOnly        	Boolean 	否       	是否只减仓，true或false，默认false仅适用于币币杠杆，以及买卖模式下的交割/永续仅适用于单币种保证金模式和跨币种保证金模式
        tgtCcy            	String  	否       	市价单委托数量sz的单位，仅适用于币币市价订单base_ccy: 交易货币 ；quote_ccy：计价货币买单默认quote_ccy， 卖单默认base_ccy
        banAmend          	Boolean 	否       	是否禁止币币市价改单，true 或 false，默认false为true时，余额不足时，系统不会改单，下单会失败，仅适用于币币市价单
        tpTriggerPx       	String  	否       	止盈触发价，如果填写此参数，必须填写 止盈委托价
        tpOrdPx           	String  	否       	止盈委托价，如果填写此参数，必须填写 止盈触发价委托价格为-1时，执行市价止盈
        attachAlgoClOrdId 	String  	否       	下单附带止盈止损时，客户自定义的策略订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。订单完全成交，下止盈止损委托单时，该值会传给algoClOrdId
        slTriggerPx       	String  	否       	止损触发价，如果填写此参数，必须填写 止损委托价
        slOrdPx           	String  	否       	止损委托价，如果填写此参数，必须填写 止损触发价委托价格为-1时，执行市价止损
        tpTriggerPxType   	String  	否       	止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        slTriggerPxType   	String  	否       	止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        quickMgnType      	String  	否       	一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动
        stpId             	String  	否       	自成交保护ID。来自同一个母账户配着同一个ID的订单不能自成交用户自定义1<=x<=999999999的整数
        stpMode           	String  	否       	自成交保护模式，需要stpId有值才会生效默认为 cancel makercancel_maker,cancel_taker,cancel_bothCancel both不支持FOK
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功
        msg               	String  	错误信息，代码为0时，该字段为空
        data              	String  	包含结果的对象数组
        > ordId           	String  	订单ID
        > clOrdId         	String  	客户自定义订单ID
        > tag             	String  	订单标签
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败或成功时的msg
        inTime            	String  	REST网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123返回的时间是请求验证后的时间。
        outTime           	String  	REST网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123
        '''
        return self.send_request(*_TradeEndpoints.set_order, **to_local(locals()))

    # POST / 批量下单
    def set_batch_orders(self, orders: list, proxies={}, proxy_host: str = None, ):
        '''
        每次最多可以批量提交20个新订单。请求参数应该按数组格式传递，会依次委托订单。<!- 1-2-3 -->该接口支持带单合约的下单，但不支持为带单合约平仓。请参考跟单了解更多
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-place-multiple-orders
        
        限速：300个/2s跟单交易带单合约的限速：4个/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-190927-5000-C
        tdMode            	String  	是       	交易模式保证金模式：isolated：逐仓 ；cross：全仓非保证金模式：cash：非保证金
        ccy               	String  	否       	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        clOrdId           	String  	否       	客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-16位之间。
        side              	String  	是       	订单方向buy：买，sell：卖
        posSide           	String  	可选      	持仓方向在开平仓模式下必填，且仅可选择long或short。 仅适用交割、永续。
        ordType           	String  	是       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)
        sz                	String  	是       	委托数量
        px                	String  	可选      	委托价格，仅适用于limit、post_only、fok、ioc、mmp、mmp_and_post_only类型的订单期权下单时，px/pxUsd/pxVol 只能填一个
        pxUsd             	String  	可选      	以USD价格进行期权下单仅适用于期权期权下单时 px/pxUsd/pxVol 必填一个，且只能填一个
        pxVol             	String  	可选      	以隐含波动率进行期权下单，例如 1 代表 100%仅适用于期权期权下单时 px/pxUsd/pxVol 必填一个，且只能填一个
        reduceOnly        	Boolean 	否       	是否只减仓，true或false，默认false仅适用于币币杠杆，以及买卖模式下的交割/永续仅适用于单币种保证金模式和跨币种保证金模式
        tgtCcy            	String  	否       	市价单委托数量sz的单位，仅适用于币币市价订单base_ccy: 交易货币 ；quote_ccy：计价货币买单默认quote_ccy， 卖单默认base_ccy
        banAmend          	Boolean 	否       	是否禁止币币市价改单，true 或 false，默认false为true时，余额不足时，系统不会改单，下单会失败，仅适用于币币市价单
        attachAlgoClOrdId 	String  	否       	下单附带止盈止损时，客户自定义的策略订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。订单完全成交，下止盈止损委托单时，该值会传给algoClOrdId
        tpTriggerPx       	String  	否       	止盈触发价，如果填写此参数，必须填写 止盈委托价
        tpOrdPx           	String  	否       	止盈委托价，如果填写此参数，必须填写 止盈触发价委托价格为-1时，执行市价止盈
        slTriggerPx       	String  	否       	止损触发价，如果填写此参数，必须填写 止损委托价
        slOrdPx           	String  	否       	止损委托价，如果填写此参数，必须填写 止损触发价委托价格为-1时，执行市价止损
        stpId             	String  	否       	自成交保护ID。来自同一个母账户配着同一个ID的订单不能自成交用户自定义1<=x<=999999999的整数
        stpMode           	String  	否       	自成交保护模式，需要stpId有值才会生效默认为 cancel makercancel_maker,cancel_taker,cancel_bothCancel both不支持FOK
        tpTriggerPxType   	String  	否       	止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        slTriggerPxType   	String  	否       	止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        quickMgnType      	String  	否       	一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功
        msg               	String  	错误信息，代码为0时，该字段为空
        data              	String  	包含结果的对象数组
        > ordId           	String  	订单ID
        > clOrdId         	String  	客户自定义订单ID
        > tag             	String  	订单标签
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败或成功时的msg
        inTime            	String  	REST网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123返回的时间是请求验证后的时间。
        outTime           	String  	REST网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123
        '''
        return self.send_request(*_TradeEndpoints.set_batch_orders, orders, proxies=proxies, proxy_host=proxy_host)

    # POST / 撤单
    def set_cancel_order(self, instId: str, ordId: str = '', clOrdId: str = '', proxies={}, proxy_host: str = None):
        '''
        撤销之前下的未完成订单。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-cancel-order
        
        限速：60次/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-190927
        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功
        msg               	String  	错误信息，代码为0时，该字段为空
        data              	String  	包含结果的对象数组
        > ordId           	String  	订单ID
        > clOrdId         	String  	客户自定义订单ID
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败时的msg
        inTime            	String  	REST网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123返回的时间是请求验证后的时间。
        outTime           	String  	REST网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123
        '''
        return self.send_request(*_TradeEndpoints.set_cancel_order, **to_local(locals()))

    # POST / 批量撤单
    def set_cancel_batch_orders(self, orders: list, proxies={}, proxy_host: str = None):
        '''
        撤销未完成的订单，每次最多可以撤销20个订单。请求参数应该按数组格式传递。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-cancel-multiple-orders
        
        限速：300个/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-190927
        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功
        msg               	String  	错误信息，代码为0时，该字段为空
        data              	String  	包含结果的对象数组
        > ordId           	String  	订单ID
        > clOrdId         	String  	客户自定义订单ID
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败时的msg
        inTime            	String  	REST网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123返回的时间是请求验证后的时间。
        outTime           	String  	REST网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123
        '''
        return self.send_request(*_TradeEndpoints.set_cancel_batch_orders, orders, proxies=proxies,
                                 proxy_host=proxy_host)

    # POST / 修改订单
    def set_amend_order(self, instId: str, cxlOnFail: bool = '', ordId: str = '', clOrdId: str = '', reqId: str = '',
                        newSz: str = '', newPx: str = '', newPxUsd: str = '', newPxVol: str = '',
                        newTpTriggerPx: str = '', newTpOrdPx: str = '', newSlTriggerPx: str = '', newSlOrdPx: str = '',
                        newTpTriggerPxType: str = '', newSlTriggerPxType: str = '', proxies={}, proxy_host: str = None):
        '''
        修改当前未成交的挂单
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-amend-order
        
        限速：60次/2s跟单交易带单合约的限速：4个/2s
        限速规则：UserID + Instrument ID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID
        cxlOnFail         	Boolean 	否       	false：不自动撤单true：自动撤单 当订单修改失败时，该订单是否需要自动撤销。默认为false
        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义order ID
        reqId             	String  	否       	用户自定义修改事件ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        newSz             	String  	可选      	修改的新数量，对于部分成交订单，该数量应包含已成交数量。
        newPx             	String  	可选      	修改后的新价格修改的新价格期权改单时，newPx/newPxUsd/newPxVol 只能填一个，且必须与下单参数保持一致，如下单用px，改单时需使用newPx
        newPxUsd          	String  	可选      	以USD价格进行期权改单仅适用于期权，期权改单时，newPx/newPxUsd/newPxVol 只能填一个
        newPxVol          	String  	可选      	以隐含波动率进行期权改单，例如 1 代表 100%仅适用于期权，期权改单时，newPx/newPxUsd/newPxVol 只能填一个
        newTpTriggerPx    	String  	可选      	止盈触发价如果止盈触发价或者委托价为0，那代表删除止盈。只适用于交割和永续合约。
        newTpOrdPx        	String  	可选      	止盈委托价委托价格为-1时，执行市价止盈。只适用于交割和永续合约。
        newSlTriggerPx    	String  	可选      	止损触发价如果止损触发价或者委托价为0，那代表删除止损。只适用于交割和永续合约。
        newSlOrdPx        	String  	可选      	止损委托价委托价格为-1时，执行市价止损。 只适用于交割和永续合约。
        newTpTriggerPxType	String  	可选      	止盈触发价类型last：最新价格index：指数价格mark：标记价格只适用于交割/永续如果要新增止盈，该参数必填
        newSlTriggerPxType	String  	可选      	止损触发价类型last：最新价格index：指数价格mark：标记价格只适用于交割/永续如果要新增止损，该参数必填
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功
        msg               	String  	错误信息，代码为0时，该字段为空
        data              	String  	包含结果的对象数组
        > ordId           	String  	订单ID
        > clOrdId         	String  	用户自定义ID
        > reqId           	String  	用户自定义修改事件ID
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败时的msg
        inTime            	String  	REST网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123返回的时间是请求验证后的时间。
        outTime           	String  	REST网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123
        '''
        return self.send_request(*_TradeEndpoints.set_amend_order, **to_local(locals()))

    # POST / 批量修改订单
    def set_amend_batch_orders(self, orders, proxies={}, proxy_host: str = None):
        '''
        修改未完成的订单，一次最多可批量修改20个订单。请求参数应该按数组格式传递。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-amend-multiple-orders
        
        限速：300个/2s跟单交易带单合约的限速：4个/2s
        限速规则：UserID + Instrument ID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID
        cxlOnFail         	Boolean 	否       	false：不自动撤单true：自动撤单 当订单修改失败时，该订单是否需要自动撤销，默认为false
        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义order ID
        reqId             	String  	否       	用户自定义修改事件ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        newSz             	String  	可选      	修改的新数量，对于部分成交订单，该数量应包含已成交数量。
        newPx             	String  	可选      	修改后的新价格修改的新价格期权改单时，newPx/newPxUsd/newPxVol 只能填一个，且必须与下单参数保持一致，如下单用px，改单时需使用newPx
        newPxUsd          	String  	可选      	以USD价格进行期权改单仅适用于期权，期权改单时，newPx/newPxUsd/newPxVol 只能填一个
        newPxVol          	String  	可选      	以隐含波动率进行期权改单，例如 1 代表 100%仅适用于期权，期权改单时，newPx/newPxUsd/newPxVol 只能填一个
        newTpTriggerPx    	String  	可选      	止盈触发价如果止盈触发价或者委托价为0，那代表删除止盈。只适用于交割和永续合约。
        newTpOrdPx        	String  	可选      	止盈委托价委托价格为-1时，执行市价止盈。只适用于交割和永续合约。
        newSlTriggerPx    	String  	可选      	止损触发价如果止损触发价或者委托价为0，那代表删除止损。只适用于交割和永续合约。
        newSlOrdPx        	String  	可选      	止损委托价委托价格为-1时，执行市价止损。只适用于交割和永续合约。
        newTpTriggerPxType	String  	可选      	止盈触发价类型last：最新价格index：指数价格mark：标记价格只适用于交割/永续如果要新增止盈，该参数必填
        newSlTriggerPxType	String  	可选      	止损触发价类型last：最新价格index：指数价格mark：标记价格只适用于交割/永续如果要新增止损，该参数必填
        返回参数:
        Parameter         	Type    	Description
        code              	String  	结果代码，0表示成功
        msg               	String  	错误信息，代码为0时，该字段为空
        data              	String  	包含结果的对象数组
        > ordId           	String  	订单ID
        > clOrdId         	String  	用户自定义ID
        > reqId           	String  	用户自定义修改事件ID
        > sCode           	String  	事件执行结果的code，0代表成功
        > sMsg            	String  	事件执行失败时的msg
        inTime            	String  	REST网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123返回的时间是请求验证后的时间。
        outTime           	String  	REST网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123
        '''
        return self.send_request(*_TradeEndpoints.set_amend_batch_orders, orders, proxies=proxies,
                                 proxy_host=proxy_host)

    # POST / 市价仓位全平
    def set_close_position(self, instId: str, mgnMode: str, posSide: str = '', ccy: str = '', autoCxl: bool = '',
                           clOrdId: str = '', tag: str = '', proxies={}, proxy_host: str = None):
        '''
        市价平掉指定交易产品的持仓
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-close-positions
        
        限速：20次/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID
        posSide           	String  	可选      	持仓方向买卖模式下：可不填写此参数，默认值net，如果填写，仅可以填写net开平仓模式下： 必须填写此参数，且仅可以填写long：平多 ，short：平空
        mgnMode           	String  	是       	保证金模式cross：全仓 ；isolated：逐仓
        ccy               	String  	可选      	保证金币种，单币种保证金模式的全仓币币杠杆平仓必填
        autoCxl           	Boolean 	否       	当市价全平时，平仓单是否需要自动撤销,默认为false.false：不自动撤单true：自动撤单
        clOrdId           	String  	否       	客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        posSide           	String  	持仓方向
        clOrdId           	String  	客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        '''
        return self.send_request(*_TradeEndpoints.set_close_position, **to_local(locals()))

    # GET / 获取订单信息
    def get_order(self, instId: str, ordId: str = '', clOrdId: str = '', proxies={}, proxy_host: str = None):
        '''
        查订单信息
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-order-details
        
        限速：60次/2s
        
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID ，如BTC-USD-190927
        ordId             	String  	可选      	订单ID ，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID如果clOrdId关联了多个订单，只会返回最近的那笔订单
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        instId            	String  	产品ID
        tgtCcy            	String  	币币市价单委托数量sz的单位base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币市价订单默认买单为quote_ccy，卖单为base_ccy
        ccy               	String  	保证金币种，仅适用于单币种保证金模式下的全仓币币杠杆订单
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        tag               	String  	订单标签
        px                	String  	委托价格，对于期权，以币(如BTC, ETH)为单位
        pxUsd             	String  	期权价格，以USD为单位仅适用于期权，其他业务线返回空字符串""
        pxVol             	String  	期权订单的隐含波动率仅适用于期权，其他业务线返回空字符串""
        pxType            	String  	期权的价格类型px：代表按价格下单，单位为币 (请求参数 px 的数值单位是BTC或ETH)pxVol：代表按pxVol下单pxUsd：代表按照pxUsd下单，单位为USD (请求参数px 的数值单位是USD)
        sz                	String  	委托数量
        pnl               	String  	收益，适用于有成交的平仓订单，其他情况均为0
        ordType           	String  	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)
        side              	String  	订单方向
        posSide           	String  	持仓方向
        tdMode            	String  	交易模式
        accFillSz         	String  	累计成交数量对于币币和杠杆，单位为交易货币，如 BTC-USDT, 单位为 BTC；对于市价单，无论tgtCcy是base_ccy，还是quote_ccy，单位均为交易货币；对于交割、永续以及期权，单位为张。
        fillPx            	String  	最新成交价格，如果成交数量为0，该字段为""
        tradeId           	String  	最新成交ID
        fillSz            	String  	最新成交数量对于币币和杠杆，单位为交易货币，如 BTC-USDT, 单位为 BTC；对于市价单，无论tgtCcy是base_ccy，还是quote_ccy，单位均为交易货币；对于交割、永续以及期权，单位为张。
        fillTime          	String  	最新成交时间
        avgPx             	String  	成交均价，如果成交数量为0，该字段也为""
        state             	String  	订单状态canceled：撤单成功live：等待成交partially_filled：部分成交filled：完全成交mmp_canceled：做市商保护机制导致的自动撤单
        lever             	String  	杠杆倍数，0.01到125之间的数值，仅适用于币币杠杆/交割/永续
        attachAlgoClOrdId 	String  	下单附带止盈止损时，客户自定义的策略订单ID
        tpTriggerPx       	String  	止盈触发价
        tpTriggerPxType   	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格
        tpOrdPx           	String  	止盈委托价
        slTriggerPx       	String  	止损触发价
        slTriggerPxType   	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格
        slOrdPx           	String  	止损委托价
        stpId             	String  	自成交保护ID如果自成交保护不适用则返回""
        stpMode           	String  	自成交保护模式如果自成交保护不适用则返回""
        feeCcy            	String  	交易手续费币种
        fee               	String  	手续费与返佣对于币币和杠杆，为订单交易累计的手续费，平台向用户收取的交易手续费，为负数。如： -0.01对于交割、永续和期权，为订单交易累计的手续费和返佣
        rebateCcy         	String  	返佣金币种
        source            	String  	订单来源6：计划委托策略触发后的生成的普通单7：止盈止损策略触发后的生成的普通单13：策略委托单触发后的生成的普通单24：移动止盈止损策略触发后的生成的普通单
        rebate            	String  	返佣金额，仅适用于币币和杠杆，平台向达到指定lv交易等级的用户支付的挂单奖励（返佣），如果没有返佣金，该字段为“”。手续费返佣为正数，如：0.01
        category          	String  	订单种类normal：普通委托twap：TWAP自动换币adl：ADL自动减仓full_liquidation：强制平仓partial_liquidation：强制减仓delivery：交割ddh：对冲减仓类型订单
        reduceOnly        	String  	是否只减仓，true或false
        cancelSource      	String  	订单取消来源的原因枚举值代码
        cancelSourceReason	String  	订单取消来源的对应具体原因
        quickMgnType      	String  	一键借币类型，仅适用于杠杆逐仓的一键借币模式manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币
        algoClOrdId       	String  	客户自定义策略订单ID。策略订单触发，且策略单有algoClOrdId时有值，否则为"",
        algoId            	String  	策略委托单ID，策略订单触发时有值，否则为""
        uTime             	String  	订单状态更新时间，Unix时间戳的毫秒数格式，如：1597026383085
        cTime             	String  	订单创建时间，Unix时间戳的毫秒数格式， 如 ：1597026383085
        '''
        return self.send_request(*_TradeEndpoints.get_order, **to_local(locals()))

    # GET / 获取未成交订单列表
    def get_orders_pending(self, instType: str = '', uly: str = '', instFamily: str = '', instId: str = '',
                           ordType: str = '', state: str = '', after: str = '', before: str = '', limit: str = '',
                           proxies={}, proxy_host: str = None):
        '''
        获取当前账户下所有未成交订单信息
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-order-list
        
        限速：60次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	否       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品ID，如BTC-USD-200927
        ordType           	String  	否       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)
        state             	String  	否       	订单状态live：等待成交partially_filled：部分成交
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品ID
        tgtCcy            	String  	币币市价单委托数量sz的单位base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币市价订单默认买单为quote_ccy，卖单为base_ccy
        ccy               	String  	保证金币种，仅适用于单币种保证金模式下的全仓币币杠杆订单
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        tag               	String  	订单标签
        px                	String  	委托价格，对于期权，以币(如BTC, ETH)为单位
        pxUsd             	String  	期权价格，以USD为单位仅适用于期权，其他业务线返回空字符串""
        pxVol             	String  	期权订单的隐含波动率仅适用于期权，其他业务线返回空字符串""
        pxType            	String  	期权的价格类型px：代表按价格下单，单位为币 (请求参数 px 的数值单位是BTC或ETH)pxVol：代表按pxVol下单pxUsd：代表按照pxUsd下单，单位为USD (请求参数px 的数值单位是USD)
        sz                	String  	委托数量
        pnl               	String  	收益，适用于有成交的平仓订单，其他情况均为0
        ordType           	String  	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)
        side              	String  	订单方向
        posSide           	String  	持仓方向
        tdMode            	String  	交易模式
        accFillSz         	String  	累计成交数量
        fillPx            	String  	最新成交价格。如果还没成交，系统返回""。
        tradeId           	String  	最新成交ID
        fillSz            	String  	最新成交数量
        fillTime          	String  	最新成交时间
        avgPx             	String  	成交均价。如果还没成交，系统返回0。
        state             	String  	订单状态live：等待成交partially_filled：部分成交
        lever             	String  	杠杆倍数，0.01到125之间的数值，仅适用于币币杠杆/交割/永续
        attachAlgoClOrdId 	String  	下单附带止盈止损时，客户自定义的策略订单ID
        tpTriggerPx       	String  	止盈触发价
        tpTriggerPxType   	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格
        slTriggerPx       	String  	止损触发价
        slTriggerPxType   	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格
        slOrdPx           	String  	止损委托价
        tpOrdPx           	String  	止盈委托价
        stpId             	String  	自成交保护ID如果自成交保护不适用则返回""
        stpMode           	String  	自成交保护模式如果自成交保护不适用则返回""
        feeCcy            	String  	交易手续费币种
        fee               	String  	手续费与返佣对于币币和杠杆，为订单交易累计的手续费，平台向用户收取的交易手续费，为负数。如： -0.01对于交割、永续和期权，为订单交易累计的手续费和返佣
        rebateCcy         	String  	返佣金币种
        source            	String  	订单来源6：计划委托策略触发后的生成的普通单7：止盈止损策略触发后的生成的普通单13：策略委托单触发后的生成的普通单24：移动止盈止损策略触发后的生成的普通单
        rebate            	String  	返佣金额，仅适用于币币和杠杆，平台向达到指定lv交易等级的用户支付的挂单奖励（返佣），如果没有返佣金，该字段为“”。手续费返佣为正数，如：0.01
        category          	String  	订单种类normal： 普通委托
        reduceOnly        	String  	是否只减仓，true或false
        quickMgnType      	String  	一键借币类型，仅适用于杠杆逐仓的一键借币模式manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币
        algoClOrdId       	String  	客户自定义策略订单ID。策略订单触发，且策略单有algoClOrdId是有值，否则为"",
        algoId            	String  	策略委托单ID，策略订单触发时有值，否则为""
        uTime             	String  	订单状态更新时间，Unix时间戳的毫秒数格式，如1597026383085
        cTime             	String  	订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_TradeEndpoints.get_orders_pending, **to_local(locals()))

    # GET / 获取历史订单记录（近七天）
    def get_orders_history(self, instType: str, uly: str = '', instFamily: str = '', instId: str = '',
                           ordType: str = '', state: str = '', category: str = '', after: str = '', before: str = '',
                           begin: str = '', end: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        获取最近7天挂单，且完全成交的订单数据，包括7天以前挂单，但近7天才成交的订单数据。按照订单创建时间倒序排序。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-order-history-last-7-days
        
        限速：40次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品ID，如BTC-USD-190927
        ordType           	String  	否       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)
        state             	String  	否       	订单状态canceled：撤单成功filled：完全成交mmp_canceled：做市商保护机制导致的自动撤单
        category          	String  	否       	订单种类twap：TWAP自动换币adl：ADL自动减仓full_liquidation：强制平仓partial_liquidation：强制减仓delivery：交割ddh：对冲减仓类型订单
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品ID
        tgtCcy            	String  	币币市价单委托数量sz的单位base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币市价订单默认买单为quote_ccy，卖单为base_ccy
        ccy               	String  	保证金币种，仅适用于单币种保证金模式下的全仓币币杠杆订单
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        tag               	String  	订单标签
        px                	String  	委托价格，对于期权，以币(如BTC, ETH)为单位
        pxUsd             	String  	期权价格，以USD为单位仅适用于期权，其他业务线返回空字符串""
        pxVol             	String  	期权订单的隐含波动率仅适用于期权，其他业务线返回空字符串""
        pxType            	String  	期权的价格类型px：代表按价格下单，单位为币 (请求参数 px 的数值单位是BTC或ETH)pxVol：代表按pxVol下单pxUsd：代表按照pxUsd下单，单位为USD (请求参数px 的数值单位是USD)
        sz                	String  	委托数量
        ordType           	String  	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)
        side              	String  	订单方向
        posSide           	String  	持仓方向
        tdMode            	String  	交易模式
        accFillSz         	String  	累计成交数量
        fillPx            	String  	最新成交价格，如果成交数量为0，该字段为""
        tradeId           	String  	最新成交ID
        fillSz            	String  	最新成交数量
        fillTime          	String  	最新成交时间
        avgPx             	String  	成交均价，如果成交数量为0，该字段也为""
        state             	String  	订单状态canceled：撤单成功filled：完全成交mmp_canceled：做市商保护机制导致的自动撤单
        lever             	String  	杠杆倍数，0.01到125之间的数值，仅适用于币币杠杆/交割/永续
        attachAlgoClOrdId 	String  	下单附带止盈止损时，客户自定义的策略订单ID
        tpTriggerPx       	String  	止盈触发价
        tpTriggerPxType   	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格
        tpOrdPx           	String  	止盈委托价
        slTriggerPx       	String  	止损触发价
        slTriggerPxType   	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格
        slOrdPx           	String  	止损委托价
        stpId             	String  	自成交保护ID如果自成交保护不适用则返回""
        stpMode           	String  	自成交保护模式如果自成交保护不适用则返回""
        feeCcy            	String  	交易手续费币种
        fee               	String  	手续费与返佣对于币币和杠杆，为订单交易累计的手续费，平台向用户收取的交易手续费，为负数。如： -0.01对于交割、永续和期权，为订单交易累计的手续费和返佣
        rebateCcy         	String  	返佣金币种
        source            	String  	订单来源6：计划委托策略触发后的生成的普通单7：止盈止损策略触发后的生成的普通单13：策略委托单触发后的生成的普通单24：移动止盈止损策略触发后的生成的普通单
        rebate            	String  	返佣金额，仅适用于币币和杠杆，平台向达到指定lv交易等级的用户支付的挂单奖励（返佣），如果没有返佣金，该字段为“”。手续费返佣为正数，如：0.01
        pnl               	String  	收益，适用于有成交的平仓订单，其他情况均为0
        category          	String  	订单种类normal：普通委托twap：TWAP自动换币adl：ADL自动减仓full_liquidation：强制平仓partial_liquidation：强制减仓delivery：交割ddh：对冲减仓类型订单
        reduceOnly        	String  	是否只减仓，true或false
        cancelSource      	String  	订单取消来源的原因枚举值代码
        cancelSourceReason	String  	订单取消来源的对应具体原因
        algoClOrdId       	String  	客户自定义策略订单ID。策略订单触发，且策略单有algoClOrdId时有值，否则为"",
        algoId            	String  	策略委托单ID，策略订单触发时有值，否则为""
        uTime             	String  	订单状态更新时间，Unix时间戳的毫秒数格式，如1597026383085
        cTime             	String  	订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_TradeEndpoints.get_orders_history, **to_local(locals()))

    # GET / 获取历史订单记录（近三个月）
    def get_orders_history_archive(self, instType: str, uly: str = '', instFamily: str = '', instId: str = '',
                                   ordType: str = '', state: str = '', category: str = '', after: str = '',
                                   before: str = '', begin: str = '', end: str = '', limit: str = '', proxies={},
                                   proxy_host: str = None):
        '''
        获取最近3个月挂单，且完全成交的订单数据，包括3个月以前挂单，但近3个月才成交的订单数据。按照订单创建时间倒序排序。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-order-history-last-3-months
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品ID，如BTC-USD-200927
        ordType           	String  	否       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)
        state             	String  	否       	订单状态canceled：撤单成功filled：完全成交mmp_canceled：做市商保护机制导致的自动撤单
        category          	String  	否       	订单种类twap：TWAP自动换币adl：ADL自动减仓full_liquidation：强制平仓partial_liquidation：强制减仓delivery：交割ddh：对冲减仓类型订单
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品ID
        tgtCcy            	String  	币币市价单委托数量sz的单位base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币市价订单默认买单为quote_ccy，卖单为base_ccy
        ccy               	String  	保证金币种，仅适用于单币种保证金模式下的全仓币币杠杆订单
        ordId             	String  	订单ID
        clOrdId           	String  	客户自定义订单ID
        tag               	String  	订单标签
        px                	String  	委托价格，对于期权，以币(如BTC, ETH)为单位
        pxUsd             	String  	期权价格，以USD为单位仅适用于期权，其他业务线返回空字符串""
        pxVol             	String  	期权订单的隐含波动率仅适用于期权，其他业务线返回空字符串""
        pxType            	String  	期权的价格类型px：代表按价格下单，单位为币 (请求参数 px 的数值单位是BTC或ETH)pxVol：代表按pxVol下单pxUsd：代表按照pxUsd下单，单位为USD (请求参数px 的数值单位是USD)
        sz                	String  	委托数量
        ordType           	String  	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)
        side              	String  	订单方向
        posSide           	String  	持仓方向
        tdMode            	String  	交易模式
        accFillSz         	String  	累计成交数量
        fillPx            	String  	最新成交价格，如果成交数量为0，该字段为""
        tradeId           	String  	最新成交ID
        fillSz            	String  	最新成交数量
        fillTime          	String  	最新成交时间
        avgPx             	String  	成交均价，如果成交数量为0，该字段也为""
        state             	String  	订单状态canceled：撤单成功filled：完全成交mmp_canceled：做市商保护机制导致的自动撤单
        lever             	String  	杠杆倍数，0.01到125之间的数值，仅适用于币币杠杆/交割/永续
        attachAlgoClOrdId 	String  	下单附带止盈止损时，客户自定义的策略订单ID
        tpTriggerPx       	String  	止盈触发价
        tpTriggerPxType   	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格
        tpOrdPx           	String  	止盈委托价
        slTriggerPx       	String  	止损触发价
        slTriggerPxType   	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格
        slOrdPx           	String  	止损委托价
        stpId             	String  	自成交保护ID如果自成交保护不适用则返回""
        stpMode           	String  	自成交保护模式如果自成交保护不适用则返回""
        feeCcy            	String  	交易手续费币种
        fee               	String  	手续费与返佣对于币币和杠杆，为订单交易累计的手续费，平台向用户收取的交易手续费，为负数。如： -0.01对于交割、永续和期权，为订单交易累计的手续费和返佣
        rebateCcy         	String  	返佣金币种
        rebate            	String  	返佣金额，仅适用于币币和杠杆，平台向达到指定lv交易等级的用户支付的挂单奖励（返佣），如果没有返佣金，该字段为“”。手续费返佣为正数，如：0.01
        pnl               	String  	收益，适用于有成交的平仓订单，其他情况均为0
        source            	String  	订单来源6：计划委托策略触发后的生成的普通单7：止盈止损策略触发后的生成的普通单13：策略委托单触发后的生成的普通单24：移动止盈止损策略触发后的生成的普通单
        category          	String  	订单种类normal：普通委托twap：TWAP自动换币adl：ADL自动减仓full_liquidation：强制平仓partial_liquidation：强制减仓delivery：交割ddh：对冲减仓类型订单
        reduceOnly        	String  	是否只减仓，true或false
        cancelSource      	String  	订单取消来源的原因枚举值代码
        cancelSourceReason	String  	订单取消来源的对应具体原因
        algoClOrdId       	String  	客户自定义策略订单ID。策略订单触发，且策略单有algoClOrdId是有值，否则为"",
        algoId            	String  	策略委托单ID，策略订单触发时有值，否则为""
        uTime             	String  	订单状态更新时间，Unix时间戳的毫秒数格式，如1597026383085
        cTime             	String  	订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_TradeEndpoints.get_orders_history_archive, **to_local(locals()))

    # GET / 获取成交明细（近三天）
    def get_fills(self, instType: str = '', uly: str = '', instFamily: str = '', instId: str = '', ordId: str = '',
                  after: str = '', before: str = '', begin: str = '', end: str = '', limit: str = '', proxies={},
                  proxy_host: str = None):
        '''
        获取近3天的订单成交明细信息
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-transaction-details-last-3-days
        
        限速：60次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	否       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品 ID，如BTC-USD-190927
        ordId             	String  	否       	订单 ID
        after             	String  	否       	请求此 ID 之前（更旧的数据）的分页内容，传的值为对应接口的billId
        before            	String  	否       	请求此 ID 之后（更新的数据）的分页内容，传的值为对应接口的billId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品 ID
        tradeId           	String  	最新成交 ID
        ordId             	String  	订单 ID
        clOrdId           	String  	用户自定义订单ID
        billId            	String  	账单 ID
        tag               	String  	订单标签
        fillPx            	String  	最新成交价格
        fillSz            	String  	最新成交数量
        fillIdxPx         	String  	交易执行时的指数价格对于交叉现货币对，返回 baseCcy-USDT 的指数价格。 例如LTC-ETH，该字段返回LTC-USDT的指数价格。
        fillPnl           	String  	最新成交收益，适用于有成交的平仓订单。其他情况均为0。
        fillPxVol         	String  	成交时的隐含波动率，仅适用于期权，其他业务线返回空字符串""
        fillPxUsd         	String  	成交时的期权价格，以USD为单位，仅适用于期权，其他业务线返回空字符串""
        fillMarkVol       	String  	成交时的标记波动率，仅适用于期权，其他业务线返回空字符串""
        fillFwdPx         	String  	成交时的远期价格，仅适用于期权，其他业务线返回空字符串""
        fillMarkPx        	String  	成交时的标记价格，仅适用于交割/永续/期权
        side              	String  	订单方向buy：买sell：卖
        posSide           	String  	持仓方向long：多short：空 买卖模式返回net
        execType          	String  	流动性方向T：takerM：maker不适用于系统订单比如强平和ADL
        feeCcy            	String  	交易手续费币种或者返佣金币种
        fee               	String  	手续费金额或者返佣金额，手续费扣除为‘负数’，如-0.01；手续费返佣为‘正数’，如 0.01
        ts                	String  	成交明细产生时间，Unix时间戳的毫秒数格式，如1597026383085
        fillTime          	String  	成交时间，与订单频道的fillTime相同
        '''
        return self.send_request(*_TradeEndpoints.get_fills, **to_local(locals()))

    # GET / 获取成交明细（近三个月）
    def get_fills_history(self, instType: str, uly: str = '', instFamily: str = '', instId: str = '', ordId: str = '',
                          after: str = '', before: str = '', begin: str = '', end: str = '', limit: str = '',
                          proxies={}, proxy_host: str = None):
        '''
        获取近3个月订单成交明细信息
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-transaction-details-last-3-months
        
        限速：10 次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品 ID，如BTC-USD-190927
        ordId             	String  	否       	订单 ID
        after             	String  	否       	请求此 ID 之前（更旧的数据）的分页内容，传的值为对应接口的billId
        before            	String  	否       	请求此 ID 之后（更新的数据）的分页内容，传的值为对应接口的billId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品 ID
        tradeId           	String  	最新成交 ID
        ordId             	String  	订单 ID
        clOrdId           	String  	用户自定义订单ID
        billId            	String  	账单 ID
        tag               	String  	订单标签
        fillPx            	String  	最新成交价格
        fillSz            	String  	最新成交数量
        fillIdxPx         	String  	交易执行时的指数价格对于交叉现货币对，返回 baseCcy-USDT 的指数价格。 例如LTC-ETH，该字段返回LTC-USDT的指数价格。
        fillPnl           	String  	最新成交收益，适用于有成交的平仓订单。其他情况均为0。
        fillPxVol         	String  	成交时的隐含波动率，仅适用于期权，其他业务线返回空字符串""
        fillPxUsd         	String  	成交时的期权价格，以USD为单位，仅适用于期权，其他业务线返回空字符串""
        fillMarkVol       	String  	成交时的标记波动率，仅适用于期权，其他业务线返回空字符串""
        fillFwdPx         	String  	成交时的远期价格，仅适用于期权，其他业务线返回空字符串""
        fillMarkPx        	String  	成交时的标记价格，仅适用于交割/永续/期权
        side              	String  	订单方向buy：买sell：卖
        posSide           	String  	持仓方向long：多short：空 买卖模式返回net
        execType          	String  	流动性方向T：takerM：maker不适用于系统订单比如强平和ADL
        feeCcy            	String  	交易手续费币种或者返佣金币种
        fee               	String  	手续费金额或者返佣金额 ，手续费扣除 为 ‘负数’，如 -0.01 ； 手续费返佣 为 ‘正数’，如 0.01
        ts                	String  	成交明细产生时间，Unix时间戳的毫秒数格式，如1597026383085
        fillTime          	String  	成交时间，与订单频道的fillTime相同
        '''
        return self.send_request(*_TradeEndpoints.get_fills_history, **to_local(locals()))

    # POST / 申请成交明细（近两年）
    def set_fills_archive(self, year: str, quarter: str, proxies={}, proxy_host: str = None):
        '''
        申请近2年的历史成交成交明细信息，不包括最近三个月。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-transaction-details-in-the-past-2-years
        
        限速：5 次/天
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        year              	String  	是       	4位数字的年份，如2023
        quarter           	String  	是       	季度，有效值Q1Q2Q3Q4
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	下载链接生成时间，Unix时间戳的毫秒数格式 ，如1597026383085
        '''
        return self.send_request(*_TradeEndpoints.set_fills_archive, **to_local(locals()))

    # GET / 获取成交明细（近两年）
    def get_fills_archive(self, year: str, quarter: str, proxies={}, proxy_host: str = None):
        '''
        获取近2年的历史成交明细信息
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-transaction-details-in-the-past-2-years
        
        限速：10 次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        year              	String  	是       	4位数字的年份，如2023
        quarter           	String  	是       	季度，有效值Q1Q2Q3Q4
        返回参数:
        Parameter         	Type    	Description
        fileHref          	String  	文件链接
        ts                	String  	下载链接生成时间，Unix时间戳的毫秒数格式 ，如1597026383085
        state             	String  	下载链接状态finished：已生成ongoing：进行中
        '''
        return self.send_request(*_TradeEndpoints.get_fills_archive, **to_local(locals()))

    # GET / 获取一键兑换主流币币种列表
    def get_easy_convert_currency_list(self, proxies={}, proxy_host: str = None):
        '''
        获取小币一键兑换主流币币种列表。仅可兑换余额在 $10 以下小币币种。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-easy-convert-currency-list
        
        限速：1次/2s
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        fromData          	Array   	当前拥有并可兑换的小币币种列表信息
        > fromCcy         	String  	可兑换币种
        > fromAmt         	String  	可兑换币种数量
        toCcy             	Array   	可转换成的主流币币种列表
        '''
        return self.send_request(*_TradeEndpoints.get_easy_convert_currency_list, **to_local(locals()))

    # POST / 一键兑换主流币交易
    def set_easy_convert(self, fromCcy: list, toCcy: str, proxies={}, proxy_host: str = None):
        '''
        进行小币一键兑换主流币交易。仅可兑换余额在 $10 以下小币币种。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-place-easy-convert
        
        限速：1次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        fromCcy           	Array   	是       	小币支付币种单次最多同时选择5个币种，如有多个币种则用逗号隔开
        toCcy             	String  	是       	兑换的主流币只选择一个币种，且不能和小币支付币种重复
        返回参数:
        Parameter         	Type    	Description
        status            	String  	当前兑换进度/状态running: 进行中filled: 已完成failed: 失败
        fromCcy           	String  	小币支付币种
        toCcy             	String  	兑换的主流币
        fillFromSz        	String  	小币偿还币种支付数量
        fillToSz          	String  	兑换的主流币成交数量
        uTime             	String  	交易时间戳，Unix时间戳为毫秒数格式，如 1597026383085
        '''
        return self.send_request(*_TradeEndpoints.set_easy_convert, **to_local(locals()))

    # GET / 获取一键兑换主流币历史记录
    def get_easy_convert_history(self, after: str = '', before: str = '', limit: str = '', proxies={},
                                 proxy_host: str = None):
        '''
        查询一键兑换主流币的历史记录与进度状态。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-easy-convert-history
        
        限速：1次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	返回的结果集数量，默认为100，最大为100
        返回参数:
        Parameter         	Type    	Description
        fromCcy           	String  	小币支付币种
        fromSz            	String  	对应的小币支付数量
        toCcy             	String  	兑换到的主流币
        toSz              	String  	兑换到的主流币数量
        status            	String  	当前兑换进度/状态running: 进行中filled: 已完成failed: 失败
        uTime             	String  	交易时间戳，Unix时间戳为毫秒数格式，如 1597026383085
        '''
        return self.send_request(*_TradeEndpoints.get_easy_convert_history, **to_local(locals()))

    # GET / 获取一键还债币种列表
    def get_one_click_repay_currency_list(self, debtType: str = '', proxies={}, proxy_host: str = None):
        '''
        查询一键还债币种列表。负债币种包括全仓负债和逐仓负债。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-one-click-repay-currency-list
        
        限速：1次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        debtType          	String  	否       	负债类型cross: 全仓负债isolated: 逐仓负债
        返回参数:
        Parameter         	Type    	Description
        debtData          	Array   	负债币种信息
        > debtCcy         	String  	负债币种
        > debtAmt         	String  	可负债币种数量包括本金和利息
        debtType          	String  	负债类型cross: 全仓负债isolated: 逐仓负债
        repayData         	Array   	偿还币种信息
        > repayCcy        	String  	可偿还负债的币种
        > repayAmt        	String  	可偿还负债的币种可用资产数量
        '''
        return self.send_request(*_TradeEndpoints.get_one_click_repay_currency_list, **to_local(locals()))

    # POST / 一键还债交易
    def set_one_click_repay(self, debtCcy: list, repayCcy: str, proxies={}, proxy_host: str = None):
        '''
        交易一键偿还小额全仓债务。不支持逐仓负债的偿还。根据资金和交易账户的剩余可用余额为最大偿还数量。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-trade-one-click-repay
        
        限速：1次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        debtCcy           	Array   	是       	负债币种单次最多同时选择5个币种，如有多个币种则用逗号隔开
        repayCcy          	String  	是       	偿还币种只选择一个币种，且不能和负债币种重复
        返回参数:
        Parameter         	Type    	Description
        status            	String  	当前还债进度/状态running: 进行中filled: 已完成failed: 失败
        debtCcy           	String  	负债币种
        repayCcy          	String  	偿还币种
        fillDebtSz        	String  	负债币种成交数量
        fillRepaySz       	String  	偿还币种成交数量
        uTime             	String  	交易时间戳，Unix时间戳为毫秒数格式，如 1597026383085
        '''
        return self.send_request(*_TradeEndpoints.set_one_click_repay, **to_local(locals()))

    # GET / 获取一键还债历史记录
    def get_one_click_repay_history(self, after: str = '', before: str = '', limit: str = '', proxies={},
                                    proxy_host: str = None):
        '''
        查询一键还债的历史记录与进度状态。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-get-one-click-repay-history
        
        限速：1次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	返回的结果集数量，默认为100，最大为100
        返回参数:
        Parameter         	Type    	Description
        debtCcy           	String  	负债币种
        debtSz            	String  	对应的负债币种成交数量
        repayCcy          	String  	偿还币种
        repaySz           	String  	偿还币种实际支付数量
        status            	String  	当前还债进度/状态running: 进行中filled: 已完成failed: 失败
        uTime             	String  	交易时间戳，Unix时间戳为毫秒数格式，如 1597026383085
        '''
        return self.send_request(*_TradeEndpoints.get_one_click_repay_history, **to_local(locals()))

    # POST / 撤销 MMP 订单
    def set_mass_cancel(self, instType: str, instFamily: str, proxies={}, proxy_host: str = None):
        '''
        撤销同一交易品种下用户所有的 MMP 挂单<!- 1-2-3 -->仅适用于组合保证金账户模式下的期权订单，且有 MMP 权限。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-mass-cancel-order
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	交易产品类型OPTION:期权
        instFamily        	String  	是       	交易品种
        返回参数:
        Parameter         	Type    	Description
        result            	Boolean 	撤单结果true：全部撤单成功false：全部撤单失败
        '''
        return self.send_request(*_TradeEndpoints.set_mass_cancel, **to_local(locals()))

    # POST / 倒计时全部撤单
    def set_cancel_all_after(self, timeOut: str, proxies={}, proxy_host: str = None):
        '''
        在倒计时结束后，取消所有 MMP 的挂单。<!- 1-2-3 -->仅适用于组合保证金账户模式下的期权订单，且有 MMP 权限。
        https://www.okx.com/docs-v5/zh/#order-book-trading-trade-post-cancel-all-after
        
        限速：1次/1s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        timeOut           	String  	是       	取消 MMP 挂单的倒计时，单位为秒。取值范围为 0, [10, 120]0 代表不使用该功能。
        返回参数:
        Parameter         	Type    	Description
        triggerTime       	String  	触发撤单的时间.triggerTime=0 代表未使用该功能。
        ts                	String  	请求时间
        '''
        return self.send_request(*_TradeEndpoints.set_cancel_all_after, **to_local(locals()))

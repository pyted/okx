from paux.param import to_local
from okx_api._client import Client


class _TradeEndpoints:
    set_order = ['/api/v5/trade/order', 'POST']  # 下单
    set_batch_orders = ['/api/v5/trade/batch-orders', 'POST']  # 批量下单
    set_cancel_order = ['/api/v5/trade/cancel-order', 'POST']  # 撤单
    set_cancel_batch_orders = ['/api/v5/trade/cancel-batch-orders', 'POST']  # 批量撤单
    set_amend_order = ['/api/v5/trade/amend-order', 'POST']  # 修改订单
    set_amend_batch_orders = ['/api/v5/trade/amend-batch-orders', 'POST']  # 批量修改订单
    set_close_position = ['/api/v5/trade/close-position', 'POST']  # 市价仓位全平
    get_order = ['/api/v5/trade/order', 'GET']  # 获取订单信息
    get_orders_pending = ['/api/v5/trade/orders-pending', 'GET']  # 获取未成交订单列表
    get_orders_history = ['/api/v5/trade/orders-history', 'GET']  # 获取历史订单记录（近七天）
    get_orders_history_archive = ['/api/v5/trade/orders-history-archive', 'GET']  # 获取历史订单记录（近三个月）
    get_fills = ['/api/v5/trade/fills', 'GET']  # 获取成交明细（近三天）
    get_fills_history = ['/api/v5/trade/fills-history', 'GET']  # 获取成交明细（近三个月）
    set_order_algo = ['/api/v5/trade/order-algo', 'POST']  # 策略委托下单
    set_cancel_algos = ['/api/v5/trade/cancel-algos', 'POST']  # 撤销策略委托订单
    set_cancel_advance_algos = ['/api/v5/trade/cancel-advance-algos', 'POST']  # 撤销高级策略委托订单
    get_orders_algo_pending = ['/api/v5/trade/orders-algo-pending', 'GET']  # 获取未完成策略委托单列表
    get_orders_algo_history = ['/api/v5/trade/orders-algo-history', 'GET']  # 获取历史策略委托单列表
    get_easy_convert_currency_list = ['/api/v5/trade/easy-convert-currency-list', 'GET']  # 获取一键兑换主流币币种列表
    set_easy_convert = ['/api/v5/trade/easy-convert', 'POST']  # 一键兑换主流币交易
    get_easy_convert_history = ['/api/v5/trade/easy-convert-history', 'GET']  # 获取一键兑换主流币历史记录
    get_one_click_repay_currency_list = ['/api/v5/trade/one-click-repay-currency-list', 'GET']  # 获取一键还债币种列表
    set_one_click_repay = ['/api/v5/trade/one-click-repay', 'POST']  # 一键还债交易
    get_one_click_repay_history = ['/api/v5/trade/one-click-repay-history', 'GET']  # 获取一键还债历史记录


class Trade(Client):
    # 下单
    def set_order(self, instId: str, tdMode: str, side: str, ordType: str, sz: str, ccy: str = '', clOrdId: str = '',
                  tag: str = '', posSide: str = '', px: str = '', reduceOnly: bool = '', tgtCcy: str = '',
                  banAmend: bool = '', tpTriggerPx: str = '', tpOrdPx: str = '', slTriggerPx: str = '',
                  slOrdPx: str = '', tpTriggerPxType: str = '', slTriggerPxType: str = '', quickMgnType: str = ''):
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
        return self.send_request(*_TradeEndpoints.set_order, **to_local(locals()))

    # 批量下单
    def set_batch_orders(self, instId: str, tdMode: str, side: str, ordType: str, sz: str, ccy: str = '',
                         clOrdId: str = '', tag: str = '', posSide: str = '', px: str = '', reduceOnly: bool = '',
                         tgtCcy: str = '', banAmend: bool = '', tpTriggerPx: str = '', tpOrdPx: str = '',
                         slTriggerPx: str = '', slOrdPx: str = '', tpTriggerPxType: str = '', slTriggerPxType: str = '',
                         quickMgnType: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-place-multiple-orders

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-190927-5000-C
        tdMode            	String  	是       	交易模式保证金模式：isolated：逐仓 ；cross：全仓非保证金模式：cash：非保证金
        side              	String  	是       	订单方向buy：买，sell：卖
        ordType           	String  	是       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）
        sz                	String  	是       	委托数量
        ccy               	String  	否       	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        clOrdId           	String  	否       	客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-16位之间。
        posSide           	String  	可选      	持仓方向在双向持仓模式下必填，且仅可选择long或short。 仅适用交割、永续。
        px                	String  	否       	委托价格，仅适用于limit、post_only、fok、ioc类型的订单
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
        return self.send_request(*_TradeEndpoints.set_batch_orders, **to_local(locals()))

    # 撤单
    def set_cancel_order(self, instId: str, ordId: str = '', clOrdId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-cancel-order

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-190927
        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID
        '''
        return self.send_request(*_TradeEndpoints.set_cancel_order, **to_local(locals()))

    # 批量撤单
    def set_cancel_batch_orders(self, instId: str, ordId: str = '', clOrdId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-cancel-multiple-orders

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-190927
        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID
        '''
        return self.send_request(*_TradeEndpoints.set_cancel_batch_orders, **to_local(locals()))

    # 修改订单
    def set_amend_order(self, instId: str, cxlOnFail: bool = '', ordId: str = '', clOrdId: str = '', reqId: str = '',
                        newSz: str = '', newPx: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-amend-order

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID
        cxlOnFail         	Boolean 	否       	false：不自动撤单true：自动撤单 当订单修改失败时，该订单是否需要自动撤销。默认为false
        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义order ID
        reqId             	String  	否       	用户自定义修改事件ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        newSz             	String  	可选      	修改的新数量，newSz和newPx不可同时为空。对于部分成交订单，该数量应包含已成交数量。
        newPx             	String  	可选      	修改的新价格
        '''
        return self.send_request(*_TradeEndpoints.set_amend_order, **to_local(locals()))

    # 批量修改订单
    def set_amend_batch_orders(self, instId: str, cxlOnFail: bool = '', ordId: str = '', clOrdId: str = '',
                               reqId: str = '', newSz: str = '', newPx: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-amend-multiple-orders

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID
        cxlOnFail         	Boolean 	否       	false：不自动撤单true：自动撤单 当订单修改失败时，该订单是否需要自动撤销，默认为false
        ordId             	String  	可选      	订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义order ID
        reqId             	String  	否       	用户自定义修改事件ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        newSz             	String  	可选      	修改的新数量，newSz和newPx不可同时为空。对于部分成交订单，该数量应包含已成交数量。
        newPx             	String  	可选      	修改的新价格
        '''
        return self.send_request(*_TradeEndpoints.set_amend_batch_orders, **to_local(locals()))

    # 市价仓位全平
    def set_close_position(self, instId: str, mgnMode: str, posSide: str = '', ccy: str = '', autoCxl: bool = '',
                           clOrdId: str = '', tag: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-close-positions

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID
        mgnMode           	String  	是       	保证金模式cross：全仓 ；isolated：逐仓
        posSide           	String  	可选      	持仓方向单向持仓模式下：可不填写此参数，默认值net，如果填写，仅可以填写net双向持仓模式下： 必须填写此参数，且仅可以填写long：平多 ，short：平空
        ccy               	String  	可选      	保证金币种，单币种保证金模式的全仓币币杠杆平仓必填
        autoCxl           	Boolean 	否       	当市价全平时，平仓单是否需要自动撤销,默认为false.false：不自动撤单true：自动撤单
        clOrdId           	String  	否       	客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        '''
        return self.send_request(*_TradeEndpoints.set_close_position, **to_local(locals()))

    # 获取订单信息
    def get_order(self, instId: str, ordId: str = '', clOrdId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-order-details

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID ，如BTC-USD-190927
        ordId             	String  	可选      	订单ID ，ordId和clOrdId必须传一个，若传两个，以ordId为主
        clOrdId           	String  	可选      	用户自定义ID
        '''
        return self.send_request(*_TradeEndpoints.get_order, **to_local(locals()))

    # 获取未成交订单列表
    def get_orders_pending(self, instType: str = '', uly: str = '', instFamily: str = '', instId: str = '',
                           ordType: str = '', state: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-order-list

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	否       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品ID，如BTC-USD-200927
        ordType           	String  	否       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）
        state             	String  	否       	订单状态live：等待成交partially_filled：部分成交
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_TradeEndpoints.get_orders_pending, **to_local(locals()))

    # 获取历史订单记录（近七天）
    def get_orders_history(self, instType: str, uly: str = '', instFamily: str = '', instId: str = '',
                           ordType: str = '', state: str = '', category: str = '', after: str = '', before: str = '',
                           begin: str = '', end: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-order-history-last-7-days

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品ID，如BTC-USD-190927
        ordType           	String  	否       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）
        state             	String  	否       	订单状态canceled：撤单成功filled：完全成交
        category          	String  	否       	订单种类twap：TWAP自动换币adl：ADL自动减仓full_liquidation：强制平仓partial_liquidation：强制减仓delivery：交割ddh：对冲减仓类型订单
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_TradeEndpoints.get_orders_history, **to_local(locals()))

    # 获取历史订单记录（近三个月）
    def get_orders_history_archive(self, instType: str, uly: str = '', instFamily: str = '', instId: str = '',
                                   ordType: str = '', state: str = '', category: str = '', after: str = '',
                                   before: str = '', begin: str = '', end: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-order-history-last-3-months

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品ID，如BTC-USD-200927
        ordType           	String  	否       	订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）
        state             	String  	否       	订单状态canceled：撤单成功filled：完全成交
        category          	String  	否       	订单种类twap：TWAP自动换币adl：ADL自动减仓full_liquidation：强制平仓partial_liquidation：强制减仓delivery：交割ddh：对冲减仓类型订单
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_TradeEndpoints.get_orders_history_archive, **to_local(locals()))

    # 获取成交明细（近三天）
    def get_fills(self, instType: str = '', uly: str = '', instFamily: str = '', instId: str = '', ordId: str = '',
                  after: str = '', before: str = '', begin: str = '', end: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-transaction-details-last-3-days

        请求参数：
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
        '''
        return self.send_request(*_TradeEndpoints.get_fills, **to_local(locals()))

    # 获取成交明细（近三个月）
    def get_fills_history(self, instType: str, uly: str = '', instFamily: str = '', instId: str = '', ordId: str = '',
                          after: str = '', before: str = '', begin: str = '', end: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-transaction-details-last-3-months

        请求参数：
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
        '''
        return self.send_request(*_TradeEndpoints.get_fills_history, **to_local(locals()))

    # 策略委托下单
    def set_order_algo(self, instId: str, tdMode: str, side: str, ordType: str, ccy: str = '', posSide: str = '',
                       sz: str = '', tag: str = '', tgtCcy: str = '', reduceOnly: bool = '', clOrdId: str = '',
                       closeFraction: str = '', quickMgnType: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-place-algo-order

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-190927-5000-C
        tdMode            	String  	是       	交易模式保证金模式isolated：逐仓，cross：全仓非保证金模式cash：非保证金
        side              	String  	是       	订单方向buy：买sell：卖
        ordType           	String  	是       	订单类型conditional：单向止盈止损oco：双向止盈止损trigger：计划委托move_order_stop：移动止盈止损iceberg：冰山委托twap：时间加权委托
        ccy               	String  	否       	保证金币种仅适用于单币种保证金模式下的全仓杠杆订单
        posSide           	String  	可选      	持仓方向在双向持仓模式下必填，且仅可选择long或short
        sz                	String  	可选      	委托数量sz和closeFraction必填且只能填其一
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间
        tgtCcy            	String  	否       	委托数量的类型base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币单向止盈止损市价买单默认买为计价货币，卖为交易货币
        reduceOnly        	Boolean 	否       	是否只减仓，true或false，默认false仅适用于币币杠杆，以及买卖模式下的交割/永续仅适用于单币种保证金模式和跨币种保证金模式
        clOrdId           	String  	否       	客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间
        closeFraction     	String  	可选      	策略委托触发时，平仓的百分比。1 代表100%现在系统只支持全部平仓，唯一接受参数为1仅适用于交割或永续仅适用于买卖模式posSide=net仅适用于减仓订单reduceOnly=true仅适用于止盈止损ordType=conditional或oco仅适用于止盈止损市价订单sz和closeFraction必填且只能填其一
        quickMgnType      	String  	否       	一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动
        '''
        return self.send_request(*_TradeEndpoints.set_order_algo, **to_local(locals()))

    # 撤销策略委托订单
    def set_cancel_algos(self, algoId: str, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-cancel-algo-order

        请求参数：
        Parameter         	Type    	Required	Description
        algoId            	String  	是       	策略委托单ID
        instId            	String  	是       	产品ID 如BTC-USDT
        '''
        return self.send_request(*_TradeEndpoints.set_cancel_algos, **to_local(locals()))

    # 撤销高级策略委托订单
    def set_cancel_advance_algos(self, algoId: str, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-cancel-advance-algo-order

        请求参数：
        Parameter         	Type    	Required	Description
        algoId            	String  	是       	策略委托单ID
        instId            	String  	是       	产品ID 如BTC-USDT
        '''
        return self.send_request(*_TradeEndpoints.set_cancel_advance_algos, **to_local(locals()))

    # 获取未完成策略委托单列表
    def get_orders_algo_pending(self, ordType: str, algoId: str = '', instType: str = '', instId: str = '',
                                after: str = '', before: str = '', limit: str = '', clOrdId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-algo-order-list

        请求参数：
        Parameter         	Type    	Required	Description
        ordType           	String  	是       	订单类型conditional：单向止盈止损oco：双向止盈止损trigger：计划委托move_order_stop：移动止盈止损iceberg：冰山委托twap：时间加权委托
        algoId            	String  	否       	策略委托单ID
        instType          	String  	否       	产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约MARGIN：杠杆
        instId            	String  	否       	产品ID，BTC-USD-190927
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        clOrdId           	String  	否       	客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        '''
        return self.send_request(*_TradeEndpoints.get_orders_algo_pending, **to_local(locals()))

    # 获取历史策略委托单列表
    def get_orders_algo_history(self, ordType: str, state: str = '', algoId: str = '', instType: str = '',
                                instId: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-algo-order-history

        请求参数：
        Parameter         	Type    	Required	Description
        ordType           	String  	是       	订单类型conditional：单向止盈止损oco：双向止盈止损trigger：计划委托move_order_stop：移动止盈止损iceberg：冰山委托twap：时间加权委托
        state             	String  	可选      	订单状态effective：已生效canceled：已经撤销order_failed：委托失败【state和algoId必填且只能填其一】
        algoId            	String  	可选      	策略委托单ID 【state和algoId必填且只能填其一】
        instType          	String  	否       	产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约MARGIN：杠杆
        instId            	String  	否       	产品ID，BTC-USD-190927
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_TradeEndpoints.get_orders_algo_history, **to_local(locals()))

    # 获取一键兑换主流币币种列表
    def get_easy_convert_currency_list(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-easy-convert-currency-list
        '''
        return self.send_request(*_TradeEndpoints.get_easy_convert_currency_list, **to_local(locals()))

    # 一键兑换主流币交易
    def set_easy_convert(self, fromCcy: object, toCcy: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-place-easy-convert-rest-api-trade-easy-convert

        请求参数：
        Parameter         	Type    	Required	Description
        fromCcy           	Array   	是       	小币支付币种单次最多同时选择5个币种，如有多个币种则用逗号隔开
        toCcy             	String  	是       	兑换的主流币只选择一个币种，且不能和小币支付币种重复
        '''
        return self.send_request(*_TradeEndpoints.set_easy_convert, **to_local(locals()))

    # 获取一键兑换主流币历史记录
    def get_easy_convert_history(self, after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-easy-convert-history-rest-api-trade-easy-convert-history

        请求参数：
        Parameter         	Type    	Required	Description
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	返回的结果集数量，默认为100，最大为100
        '''
        return self.send_request(*_TradeEndpoints.get_easy_convert_history, **to_local(locals()))

    # 获取一键还债币种列表
    def get_one_click_repay_currency_list(self, debtType: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-one-click-repay-currency-list-rest-api-trade-one-click-repay-currency-list

        请求参数：
        Parameter         	Type    	Required	Description
        debtType          	String  	否       	负债类型cross: 全仓负债isolated: 逐仓负债
        '''
        return self.send_request(*_TradeEndpoints.get_one_click_repay_currency_list, **to_local(locals()))

    # 一键还债交易
    def set_one_click_repay(self, debtCcy: object, repayCcy: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-trade-one-click-repay-rest-api-trade-one-click-repay

        请求参数：
        Parameter         	Type    	Required	Description
        debtCcy           	Array   	是       	负债币种单次最多同时选择5个币种，如有多个币种则用逗号隔开
        repayCcy          	String  	是       	偿还币种只选择一个币种，且不能和负债币种重复
        '''
        return self.send_request(*_TradeEndpoints.set_one_click_repay, **to_local(locals()))

    # 获取一键还债历史记录
    def get_one_click_repay_history(self, after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-trade-get-one-click-repay-history-rest-api-trade-one-click-repay-history

        请求参数：
        Parameter         	Type    	Required	Description
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	返回的结果集数量，默认为100，最大为100
        '''
        return self.send_request(*_TradeEndpoints.get_one_click_repay_history, **to_local(locals()))

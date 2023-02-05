from paux.param import to_local
from okx_api._client import Client


class _GridEndpoints:
    set_order_algo = ['/api/v5/tradingBot/grid/order-algo', 'POST']  # 网格策略委托下单
    set_amend_order_algo = ['/api/v5/tradingBot/grid/amend-order-algo', 'POST']  # 修改网格策略订单
    set_stop_order_algo = ['/api/v5/tradingBot/grid/stop-order-algo', 'POST']  # 网格策略停止
    get_orders_algo_pending = ['/api/v5/tradingBot/grid/orders-algo-pending', 'GET']  # 获取未完成网格策略委托单列表
    get_orders_algo_history = ['/api/v5/tradingBot/grid/orders-algo-history', 'GET']  # 获取历史网格策略委托单列表
    get_orders_algo_details = ['/api/v5/tradingBot/grid/orders-algo-details', 'GET']  # 获取网格策略委托订单详情
    get_sub_orders = ['/api/v5/tradingBot/grid/sub-orders', 'GET']  # 获取网格策略委托子订单信息
    get_positions = ['/api/v5/tradingBot/grid/positions', 'GET']  # 获取网格策略委托持仓
    set_withdraw_income = ['/api/v5/tradingBot/grid/withdraw-income', 'POST']  # 现货/天地网格提取利润
    set_compute_margin_balance = ['/api/v5/tradingBot/grid/compute-margin-balance', 'POST']  # 调整保证金计算
    set_margin_balance = ['/api/v5/tradingBot/grid/margin-balance', 'POST']  # 调整保证金
    get_ai_param = ['/api/v5/tradingBot/grid/ai-param', 'GET']  # 网格策略智能回测（公共）


class Grid(Client):
    # 网格策略委托下单
    def set_order_algo(self, instId: str, algoOrdType: str, maxPx: str, minPx: str, gridNum: str, runType: str = '',
                       tpTriggerPx: str = '', slTriggerPx: str = '', tag: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-place-grid-algo-order

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        maxPx             	String  	是       	区间最高价格
        minPx             	String  	是       	区间最低价格
        gridNum           	String  	是       	网格数量
        runType           	String  	否       	网格类型1：等差，2：等比默认为等差天地网格只支持2
        tpTriggerPx       	String  	否       	止盈触发价适用于现货网格/合约网格
        slTriggerPx       	String  	否       	止损触发价适用于现货网格/合约网格
        tag               	String  	否       	订单标签
        '''
        return self.send_request(*_GridEndpoints.set_order_algo, **to_local(locals()))

    # 修改网格策略订单
    def set_amend_order_algo(self, algoId: str, instId: str, slTriggerPx: str = '', tpTriggerPx: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-amend-grid-algo-order

        请求参数：
        Parameter         	Type    	Required	Description
        algoId            	String  	是       	策略订单ID
        instId            	String  	是       	产品ID，如BTC-USDT-SWAP
        slTriggerPx       	String  	可选      	新的止损触发价当值为""则代表取消止损触发价slTriggerPx、tpTriggerPx至少要传一个值
        tpTriggerPx       	String  	可选      	新的止盈触发价当值为""则代表取消止盈触发价
        '''
        return self.send_request(*_GridEndpoints.set_amend_order_algo, **to_local(locals()))

    # 网格策略停止
    def set_stop_order_algo(self, algoId: str, instId: str, algoOrdType: str, stopType: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-stop-grid-algo-order

        请求参数：
        Parameter         	Type    	Required	Description
        algoId            	String  	是       	策略订单ID
        instId            	String  	是       	产品ID，如BTC-USDT
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        stopType          	String  	是       	网格策略停止类型现货网格/天地网格1：卖出交易币，2：不卖出交易币合约网格1：市价全平
        '''
        return self.send_request(*_GridEndpoints.set_stop_order_algo, **to_local(locals()))

    # 获取未完成网格策略委托单列表
    def get_orders_algo_pending(self, algoOrdType: str, algoId: str = '', instId: str = '', instType: str = '',
                                after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-get-grid-algo-order-list

        请求参数：
        Parameter         	Type    	Required	Description
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        algoId            	String  	否       	策略订单ID
        instId            	String  	否       	产品ID，如BTC-USDT
        instType          	String  	否       	产品类型SPOT：币币MARGIN：杠杆FUTURES：交割合约SWAP：永续合约
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_GridEndpoints.get_orders_algo_pending, **to_local(locals()))

    # 获取历史网格策略委托单列表
    def get_orders_algo_history(self, algoOrdType: str, algoId: str = '', instId: str = '', instType: str = '',
                                after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-get-grid-algo-order-history

        请求参数：
        Parameter         	Type    	Required	Description
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        algoId            	String  	否       	策略订单ID
        instId            	String  	否       	产品ID，如BTC-USDT
        instType          	String  	否       	产品类型SPOT：币币MARGIN：杠杆FUTURES：交割合约SWAP：永续合约
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_GridEndpoints.get_orders_algo_history, **to_local(locals()))

    # 获取网格策略委托订单详情
    def get_orders_algo_details(self, algoOrdType: str, algoId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-get-grid-algo-order-details

        请求参数：
        Parameter         	Type    	Required	Description
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        algoId            	String  	是       	策略订单ID
        '''
        return self.send_request(*_GridEndpoints.get_orders_algo_details, **to_local(locals()))

    # 获取网格策略委托子订单信息
    def get_sub_orders(self, algoId: str, algoOrdType: str, type: str, groupId: str = '', after: str = '',
                       before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-get-grid-algo-sub-orders

        请求参数：
        Parameter         	Type    	Required	Description
        algoId            	String  	是       	策略订单ID
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        type              	String  	是       	子订单状态live：未成交，filled：已成交
        groupId           	String  	否       	组ID
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_GridEndpoints.get_sub_orders, **to_local(locals()))

    # 获取网格策略委托持仓
    def get_positions(self, algoOrdType: str, algoId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-get-grid-algo-order-positions

        请求参数：
        Parameter         	Type    	Required	Description
        algoOrdType       	String  	是       	订单类型contract_grid：合约网格委托
        algoId            	String  	是       	策略订单ID
        '''
        return self.send_request(*_GridEndpoints.get_positions, **to_local(locals()))

    # 现货/天地网格提取利润
    def set_withdraw_income(self, algoId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-spot-moon-grid-withdraw-income

        请求参数：
        Parameter         	Type    	Required	Description
        algoId            	String  	是       	策略订单ID
        '''
        return self.send_request(*_GridEndpoints.set_withdraw_income, **to_local(locals()))

    # 调整保证金计算
    def set_compute_margin_balance(self, algoId: str, type: str, amt: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-compute-margin-balance

        请求参数：
        Parameter         	Type    	Required	Description
        algoId            	String  	是       	策略订单ID
        type              	String  	是       	调整保证金类型add：增加，reduce：减少
        amt               	String  	否       	调整保证金数量
        '''
        return self.send_request(*_GridEndpoints.set_compute_margin_balance, **to_local(locals()))

    # 调整保证金
    def set_margin_balance(self, algoId: str, type: str, amt: str = '', percent: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-adjust-margin-balance

        请求参数：
        Parameter         	Type    	Required	Description
        algoId            	String  	是       	策略订单ID
        type              	String  	是       	调整保证金类型add：增加，reduce：减少
        amt               	String  	可选      	调整保证金数量amt和percent必须传一个
        percent           	String  	可选      	调整保证金百分比
        '''
        return self.send_request(*_GridEndpoints.set_margin_balance, **to_local(locals()))

    # 网格策略智能回测（公共）
    def get_ai_param(self, algoOrdType: str, instId: str, direction: str = '', duration: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-grid-trading-get-grid-ai-parameter-public

        请求参数：
        Parameter         	Type    	Required	Description
        algoOrdType       	String  	是       	策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托
        instId            	String  	是       	产品ID，如BTC-USDT
        direction         	String  	可选      	合约网格类型long：做多，short：做空，neutral：中性合约网格必填
        duration          	String  	否       	回测周期7D：7天，30D：30天，180D：180天默认现货网格为7D，天地网格为180D
        '''
        return self.send_request(*_GridEndpoints.get_ai_param, **to_local(locals()))

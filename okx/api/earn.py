'''
赚币
https://www.okx.com/docs-v5/zh/#financial-product-earn
'''
from paux.param import to_local
from okx.api._client import Client


class _EarnEndpoints():
    get_offers = ['/api/v5/finance/staking-defi/offers', 'GET']  # GET / 查看项目
    set_purchase = ['/api/v5/finance/staking-defi/purchase', 'POST']  # POST / 申购项目
    set_redeem = ['/api/v5/finance/staking-defi/redeem', 'POST']  # POST / 赎回项目
    set_cancel = ['/api/v5/finance/staking-defi/cancel', 'POST']  # POST / 撤销项目申购/赎回
    get_orders_active = ['/api/v5/finance/staking-defi/orders-active', 'GET']  # GET / 查看活跃订单
    get_orders_history = ['/api/v5/finance/staking-defi/orders-history', 'GET']  # GET / 查看历史订单


class Earn(Client):

    # GET / 查看项目
    def get_offers(self, productId: str = '', protocolType: str = '', ccy: str = '', proxies={},
                   proxy_host: str = None):
        '''
        GET /api/v5/finance/staking-defi/offers
        https://www.okx.com/docs-v5/zh/#financial-product-earn-get-offers
        
        限速：3次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        productId         	String  	否       	项目ID
        protocolType      	String  	否       	项目类型staking：锁仓挖矿defi：DEFI
        ccy               	String  	否       	投资币种，如BTC
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种名称，如BTC
        productId         	String  	项目ID
        protocol          	String  	项目名称
        protocolType      	String  	项目类型staking：锁仓挖矿defi：DEFI
        term              	String  	项目期限活期为0，其他则显示定期天数
        apy               	String  	预估年化如果年化为7% ，则该字段为0.07
        earlyRedeem       	Boolean 	项目是否支持提前赎回
        investData        	Array   	目前用户可用来投资的目标币种信息
        > ccy             	String  	投资币种，如BTC
        > bal             	String  	可投数量
        > minAmt          	String  	最小申购量
        > maxAmt          	String  	最大申购量
        earningData       	Array   	收益信息
        > ccy             	String  	收益币种，如BTC
        > earningType     	String  	收益类型0: 预估收益1: 累计发放收益
        state             	String  	项目状态purchasable：可申购sold_out：售罄stop：暂停申购
        '''
        return self.send_request(*_EarnEndpoints.get_offers, **to_local(locals()))

    # POST / 申购项目
    def set_purchase(self, productId: str, investData: list, term: str = '', tag: str = '', proxies={},
                     proxy_host: str = None):
        '''
        POST /api/v5/finance/staking-defi/purchase
        https://www.okx.com/docs-v5/zh/#financial-product-earn-post-purchase
        
        限速：2次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        productId         	String  	是       	项目ID
        investData        	Array   	是       	投资信息
        > ccy             	String  	是       	投资币种，如BTC
        > amt             	String  	是       	投资数量
        term              	String  	可选      	投资期限定期项目必须指定投资期限
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间
        返回参数:
        Parameter         	Type    	Description
        ordId             	String  	订单ID
        tag               	String  	订单标签
        '''
        return self.send_request(*_EarnEndpoints.set_purchase, **to_local(locals()))

    # POST / 赎回项目
    def set_redeem(self, ordId: str, protocolType: str, allowEarlyRedeem: bool = '', proxies={},
                   proxy_host: str = None):
        '''
        POST /api/v5/finance/staking-defi/redeem
        https://www.okx.com/docs-v5/zh/#financial-product-earn-post-redeem
        
        限速：2次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ordId             	String  	是       	订单ID
        protocolType      	String  	是       	项目类型staking：锁仓挖矿defi：DEFI
        allowEarlyRedeem  	Boolean 	否       	是否提前赎回默认为false
        返回参数:
        Parameter         	Type    	Description
        ordId             	String  	订单ID
        tag               	String  	订单标签
        '''
        return self.send_request(*_EarnEndpoints.set_redeem, **to_local(locals()))

    # POST / 撤销项目申购/赎回
    def set_cancel(self, ordId: str, protocolType: str, proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/finance/staking-defi/cancel
        https://www.okx.com/docs-v5/zh/#financial-product-earn-post-cancel-purchases-redemptions
        
        限速：2次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ordId             	String  	是       	订单ID
        protocolType      	String  	是       	项目类型staking：锁仓挖矿defi：DEFI
        返回参数:
        Parameter         	Type    	Description
        ordId             	String  	订单ID
        tag               	String  	订单标签
        '''
        return self.send_request(*_EarnEndpoints.set_cancel, **to_local(locals()))

    # GET / 查看活跃订单
    def get_orders_active(self, productId: str = '', protocolType: str = '', ccy: str = '', state: str = '', proxies={},
                          proxy_host: str = None):
        '''
        GET /api/v5/finance/staking-defi/orders-active
        https://www.okx.com/docs-v5/zh/#financial-product-earn-get-active-orders
        
        限速：3次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        productId         	String  	否       	项目ID
        protocolType      	String  	否       	项目类型staking：锁仓挖矿defi：DEFI
        ccy               	String  	否       	投资币种，如BTC
        state             	String  	否       	订单状态8: 待上车（预约中）13: 订单取消中9: 上链中1: 收益中2: 赎回中
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种名称，如BTC
        ordId             	String  	订单ID
        productId         	String  	项目ID
        state             	String  	订单状态8: 待上车（预约中）13: 订单取消中9: 上链中1: 收益中2: 赎回中
        protocol          	String  	项目名称
        protocolType      	String  	项目类型staking：锁仓挖矿defi：DEFI
        term              	String  	项目期限活期为0，其他则显示定期天数
        apy               	String  	预估年化如果年化为7% ，则该字段为0.07保留到小数点后4位（截位）
        investData        	Array   	用户投资信息
        > ccy             	String  	投资币种，如BTC
        > amt             	String  	已投资数量
        earningData       	Array   	收益信息
        > ccy             	String  	收益币种，如BTC
        > earningType     	String  	收益类型0: 预估收益1: 实际到账收益
        > earnings        	String  	收益数量
        purchasedTime     	String  	用户订单创建时间，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        purchasedTime     	String  	用户订单创建时间，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        estSettlementTime 	String  	预估赎回到账时间
        cancelRedemptionDeadline	String  	撤销赎回申请截止时间
        tag               	String  	订单标签
        '''
        return self.send_request(*_EarnEndpoints.get_orders_active, **to_local(locals()))

    # GET / 查看历史订单
    def get_orders_history(self, productId: str = '', protocolType: str = '', ccy: str = '', after: str = '',
                           before: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/finance/staking-defi/orders-history
        https://www.okx.com/docs-v5/zh/#financial-product-earn-get-order-history
        
        限速：3次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        productId         	String  	否       	项目ID
        protocolType      	String  	否       	项目类型staking：锁仓挖矿defi：DEFI
        ccy               	String  	否       	投资币种，如BTC
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，默认100条,最大值为100条
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种名称，如BTC
        ordId             	String  	订单ID
        productId         	String  	项目ID
        state             	String  	订单状态3: 订单已完成（包含撤销和已赎回两种状态）
        protocol          	String  	项目名称
        protocolType      	String  	项目类型staking：锁仓挖矿defi：DEFI
        term              	String  	项目期限活期为0，其他则显示定期天数
        apy               	String  	预估年化如果年化为7% ，则该字段为0.07保留到小数点后4位（截位）
        investData        	Array   	用户投资信息
        > ccy             	String  	投资币种，如BTC
        > amt             	String  	已投资数量
        earningData       	Array   	收益信息
        > ccy             	String  	收益币种，如BTC
        > earningType     	String  	收益类型0:预估收益1:实际到账收益
        > realizedEarnings	String  	已赎回订单累计收益该字段只在订单处于赎回状态时有效
        purchasedTime     	String  	用户订单创建时间，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        redeemedTime      	String  	用户订单赎回时间，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        tag               	String  	订单标签
        '''
        return self.send_request(*_EarnEndpoints.get_orders_history, **to_local(locals()))

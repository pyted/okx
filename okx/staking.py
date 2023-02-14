from paux.param import to_local
from okx._client import Client


class _StakingEndpoints:
    get_offers = ['/api/v5/finance/staking-defi/offers', 'GET']  # 查看项目
    set_purchase = ['/api/v5/finance/staking-defi/purchase', 'POST']  # 申购项目
    set_redeem = ['/api/v5/finance/staking-defi/redeem', 'POST']  # 赎回项目
    set_cancel = ['/api/v5/finance/staking-defi/cancel', 'POST']  # 撤销项目申购/赎回
    get_orders_active = ['/api/v5/finance/staking-defi/orders-active', 'GET']  # 查看活跃订单
    get_orders_history = ['/api/v5/finance/staking-defi/orders-history', 'GET']  # 查看历史订单


class Staking(Client):
    # 查看项目
    def get_offers(self, productId: str = '', protocolType: str = '', ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-earn-get-offers

        请求参数：
        Parameter         	Type    	Required	Description
        productId         	String  	否       	项目ID
        protocolType      	String  	否       	项目类型staking：锁仓挖矿defi：DEFI
        ccy               	String  	否       	投资币种，如BTC
        '''
        return self.send_request(*_StakingEndpoints.get_offers, **to_local(locals()))

    # 申购项目
    def set_purchase(self, productId: str, investData: object, ccy:str, amt:str, term: str = '', tag: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-earn-purchase

        请求参数：
        Parameter         	Type    	Required	Description
        productId         	String  	是       	项目ID
        investData        	Array   	是       	投资信息
        > ccy             	String  	是       	投资币种，如BTC
        > amt             	String  	是       	投资数量
        term              	String  	可选      	投资期限定期项目必须指定投资期限
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间
        '''
        return self.send_request(*_StakingEndpoints.set_purchase, **to_local(locals()))

    # 赎回项目
    def set_redeem(self, ordId: str, protocolType: str, allowEarlyRedeem: bool = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-earn-redeem

        请求参数：
        Parameter         	Type    	Required	Description
        ordId             	String  	是       	订单ID
        protocolType      	String  	是       	项目类型staking：锁仓挖矿defi：DEFI
        allowEarlyRedeem  	Boolean 	否       	是否提前赎回默认为false
        '''
        return self.send_request(*_StakingEndpoints.set_redeem, **to_local(locals()))

    # 撤销项目申购/赎回
    def set_cancel(self, ordId: str, protocolType: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-earn-cancel-purchases-redemptions

        请求参数：
        Parameter         	Type    	Required	Description
        ordId             	String  	是       	订单ID
        protocolType      	String  	是       	项目类型staking：锁仓挖矿defi：DEFI
        '''
        return self.send_request(*_StakingEndpoints.set_cancel, **to_local(locals()))

    # 查看活跃订单
    def get_orders_active(self, productId: str = '', protocolType: str = '', ccy: str = '', state: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-earn-get-active-orders

        请求参数：
        Parameter         	Type    	Required	Description
        productId         	String  	否       	项目ID
        protocolType      	String  	否       	项目类型staking：锁仓挖矿defi：DEFI
        ccy               	String  	否       	投资币种，如BTC
        state             	String  	否       	订单状态8: 待上车（预约中）13: 订单取消中9: 上链中1: 收益中2: 赎回中
        '''
        return self.send_request(*_StakingEndpoints.get_orders_active, **to_local(locals()))

    # 查看历史订单
    def get_orders_history(self, productId: str = '', protocolType: str = '', ccy: str = '', after: str = '',
                           before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-earn-get-order-history

        请求参数：
        Parameter         	Type    	Required	Description
        productId         	String  	否       	项目ID
        protocolType      	String  	否       	项目类型staking：锁仓挖矿defi：DEFI
        ccy               	String  	否       	投资币种，如BTC
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，默认100条,最大值为100条
        '''
        return self.send_request(*_StakingEndpoints.get_orders_history, **to_local(locals()))

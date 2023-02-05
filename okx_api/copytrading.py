from paux.param import to_local
from okx_api._client import Client


class _CopytradingEndpoints:
    get_current_subpositions = ['/api/v5/copytrading/current-subpositions', 'GET']  # 交易员获取当前带单
    get_subpositions_history = ['/api/v5/copytrading/subpositions-history', 'GET']  # 交易员获取历史带单
    set_algo_order = ['/api/v5/copytrading/algo-order', 'POST']  # 交易员止盈止损
    set_close_subposition = ['/api/v5/copytrading/close-subposition', 'POST']  # 交易员平仓
    get_instruments = ['/api/v5/copytrading/instruments', 'GET']  # 交易员获取带单合约
    set_set_instruments = ['/api/v5/copytrading/set-instruments', 'POST']  # 交易员修改带单合约
    get_profit_sharing_details = ['/api/v5/copytrading/profit-sharing-details', 'GET']  # 交易员历史分润明细
    get_total_profit_sharing = ['/api/v5/copytrading/total-profit-sharing', 'GET']  # 交易员历史分润汇总
    get_unrealized_profit_sharing_details = ['/api/v5/copytrading/unrealized-profit-sharing-details', 'GET']  # 交易员待分润明细


class Copytrading(Client):
    # 交易员获取当前带单
    def get_current_subpositions(self, instId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-copy-trading-get-existing-leading-positions

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	否       	产品ID ，如BTC-USDT-SWAP
        '''
        return self.send_request(*_CopytradingEndpoints.get_current_subpositions, **to_local(locals()))

    # 交易员获取历史带单
    def get_subpositions_history(self, instId: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-copy-trading-get-leading-position-history

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	否       	产品ID ，如BTC-USDT-SWAP
        after             	String  	否       	请求此id之前（更旧的数据）的分页内容，传的值为对应接口的subPosId
        before            	String  	否       	请求此id之后（更新的数据）的分页内容，传的值为对应接口的subPosId
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_CopytradingEndpoints.get_subpositions_history, **to_local(locals()))

    # 交易员止盈止损
    def set_algo_order(self, subPosId: str, tpTriggerPx: str = '', slTriggerPx: str = '', tpTriggerPxType: str = '',
                       slTriggerPxType: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-copy-trading-place-leading-stop-order

        请求参数：
        Parameter         	Type    	Required	Description
        subPosId          	String  	是       	带单仓位ID
        tpTriggerPx       	String  	可选      	止盈触发价，触发后以市价进行委托，tpTriggerPx 和 slTriggerPx 至少需要填写一个
        slTriggerPx       	String  	可选      	止损触发价，触发后以市价进行委托
        tpTriggerPxType   	String  	否       	止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        slTriggerPxType   	String  	否       	止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        '''
        return self.send_request(*_CopytradingEndpoints.set_algo_order, **to_local(locals()))

    # 交易员平仓
    def set_close_subposition(self, subPosId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-copy-trading-close-leading-position

        请求参数：
        Parameter         	Type    	Required	Description
        subPosId          	String  	是       	带单仓位ID
        '''
        return self.send_request(*_CopytradingEndpoints.set_close_subposition, **to_local(locals()))

    # 交易员获取带单合约
    def get_instruments(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-copy-trading-get-leading-instruments
        '''
        return self.send_request(*_CopytradingEndpoints.get_instruments, **to_local(locals()))

    # 交易员修改带单合约
    def set_set_instruments(self, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-copy-trading-set-leading-instruments

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如 BTC-USDT-SWAP，多个产品用半角逗号隔开，最多支持10个产品ID
        '''
        return self.send_request(*_CopytradingEndpoints.set_set_instruments, **to_local(locals()))

    # 交易员历史分润明细
    def get_profit_sharing_details(self, after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-copy-trading-get-profit-sharing-details

        请求参数：
        Parameter         	Type    	Required	Description
        after             	String  	否       	请求此id之前（更旧的数据）的分页内容，传的值为对应接口的profitSharingId
        before            	String  	否       	请求此id之后（更新的数据）的分页内容，传的值为对应接口的profitSharingId
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_CopytradingEndpoints.get_profit_sharing_details, **to_local(locals()))

    # 交易员历史分润汇总
    def get_total_profit_sharing(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-copy-trading-get-total-profit-sharing
        '''
        return self.send_request(*_CopytradingEndpoints.get_total_profit_sharing, **to_local(locals()))

    # 交易员待分润明细
    def get_unrealized_profit_sharing_details(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-copy-trading-get-unrealized-profit-sharing-details
        '''
        return self.send_request(*_CopytradingEndpoints.get_unrealized_profit_sharing_details, **to_local(locals()))

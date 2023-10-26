'''
跟单
https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading
'''
from paux.param import to_local
from okx.api._client import Client


class _CopyTradeEndpoints():
    get_current_subpositions = ['/api/v5/copytrading/current-subpositions', 'GET']  # GET / 交易员获取当前带单
    get_subpositions_history = ['/api/v5/copytrading/subpositions-history', 'GET']  # GET / 交易员获取历史带单
    set_algo_order = ['/api/v5/copytrading/algo-order', 'POST']  # POST / 交易员止盈止损
    set_close_subposition = ['/api/v5/copytrading/close-subposition', 'POST']  # POST / 交易员平仓
    get_instruments = ['/api/v5/copytrading/instruments', 'GET']  # GET / 交易员获取带单合约
    set_instruments = ['/api/v5/copytrading/set-instruments', 'POST']  # POST / 交易员修改带单合约
    get_profit_sharing_details = ['/api/v5/copytrading/profit-sharing-details', 'GET']  # GET / 交易员历史分润明细
    get_total_profit_sharing = ['/api/v5/copytrading/total-profit-sharing', 'GET']  # GET / 交易员历史分润汇总
    get_unrealized_profit_sharing_details = ['/api/v5/copytrading/unrealized-profit-sharing-details', 'GET']  # GET / 交易员待分润明细


class CopyTrade(Client):

    # GET / 交易员获取当前带单
    def get_current_subpositions(self, instId: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                                 proxy_host: str = None):
        '''
        交易员获取当前未平仓的带单仓位。
        https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading-get-existing-leading-positions
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	否       	产品ID ，如BTC-USDT-SWAP
        after             	String  	否       	请求此id之前（更旧的数据）的分页内容，传的值为对应接口的subPosId
        before            	String  	否       	请求此id之后（更新的数据）的分页内容，传的值为对应接口的subPosId
        limit             	String  	否       	分页返回的结果集数量，最大为500，不填默认返回500条
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        subPosId          	String  	带单仓位ID
        posSide           	String  	持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式（subPos为正代表开多，subPos为负代表开空）
        mgnMode           	String  	保证金模式，isolated：逐仓 ；cross：全仓
        lever             	String  	杠杆倍数
        openOrdId         	String  	交易员开仓订单号
        openAvgPx         	String  	开仓均价
        openTime          	String  	开仓时间
        subPos            	String  	持仓张数
        tpTriggerPx       	String  	止盈触发价，触发后以市价进行委托
        slTriggerPx       	String  	止损触发价，触发后以市价进行委托
        algoId            	String  	止盈止损委托单ID
        '''
        return self.send_request(*_CopyTradeEndpoints.get_current_subpositions, **to_local(locals()))

    # GET / 交易员获取历史带单
    def get_subpositions_history(self, instId: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                                 proxy_host: str = None):
        '''
        交易员获取最近三个月的已经平仓的带单仓位，按照subPosId倒序排序。
        https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading-get-leading-position-history
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	否       	产品ID ，如BTC-USDT-SWAP
        after             	String  	否       	请求此id之前（更旧的数据）的分页内容，传的值为对应接口的subPosId
        before            	String  	否       	请求此id之后（更新的数据）的分页内容，传的值为对应接口的subPosId
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        subPosId          	String  	带单仓位ID
        posSide           	String  	持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式（subPos为正代表开多，subPos为负代表开空）
        mgnMode           	String  	保证金模式，isolated：逐仓 ；cross：全仓
        lever             	String  	杠杆倍数
        openOrdId         	String  	交易员开仓订单号
        openAvgPx         	String  	开仓均价
        openTime          	String  	开仓时间
        subPos            	String  	持仓张数
        closeTime         	String  	平仓时间(最近一次平仓的时间，即完全平仓的时间)
        closeAvgPx        	String  	平仓均价
        pnl               	String  	收益额
        pnlRatio          	String  	收益率
        '''
        return self.send_request(*_CopyTradeEndpoints.get_subpositions_history, **to_local(locals()))

    # POST / 交易员止盈止损
    def set_algo_order(self, subPosId: str, tpTriggerPx: str = '', slTriggerPx: str = '', tpTriggerPxType: str = '',
                       slTriggerPxType: str = '', tag: str = '', proxies={}, proxy_host: str = None):
        '''
        交易员为当前未平仓的带单仓位设置止盈止损。
        https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading-post-place-leading-stop-order
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        subPosId          	String  	是       	带单仓位ID
        tpTriggerPx       	String  	可选      	止盈触发价，触发后以市价进行委托，tpTriggerPx 和 slTriggerPx 至少需要填写一个
        slTriggerPx       	String  	可选      	止损触发价，触发后以市价进行委托
        tpTriggerPxType   	String  	否       	止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        slTriggerPxType   	String  	否       	止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        返回参数:
        Parameter         	Type    	Description
        subPosId          	String  	带单仓位ID
        tag               	String  	订单标签
        '''
        return self.send_request(*_CopyTradeEndpoints.set_algo_order, **to_local(locals()))

    # POST / 交易员平仓
    def set_close_subposition(self, subPosId: str, tag: str = '', proxies={}, proxy_host: str = None):
        '''
        交易员一次仅可平仓一个带单仓位。<!- 1-2-3 -->带单ID（subPosId）为必填参数，需要通过交易员获取当前带单接口获取。
        https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading-post-close-leading-position
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        subPosId          	String  	是       	带单仓位ID
        tag               	String  	否       	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        返回参数:
        Parameter         	Type    	Description
        subPosId          	String  	带单仓位ID
        tag               	String  	订单标签
        '''
        return self.send_request(*_CopyTradeEndpoints.set_close_subposition, **to_local(locals()))

    # GET / 交易员获取带单合约
    def get_instruments(self, proxies={}, proxy_host: str = None):
        '''
        交易员获取平台支持带单的合约。
        https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading-get-leading-instruments
        
        限速：5次/2s
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        enabled           	Boolean 	是否设置了跟单true或false
        '''
        return self.send_request(*_CopyTradeEndpoints.get_instruments, **to_local(locals()))

    # POST / 交易员修改带单合约
    def set_instruments(self, instId: str, proxies={}, proxy_host: str = None):
        '''
        交易员修改带单合约的设置。初始带单合约在申请带单交易员时进行设置。<!- 1-2-3 -->非带单合约修改为带单合约时，该次请求中所有的非带单合约合约不能有持仓或者挂单。
        https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading-post-amend-leading-instruments
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如 BTC-USDT-SWAP，多个产品用半角逗号隔开，最多支持31个产品ID
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品id， 如 BTC-USDT-SWAP
        enabled           	Boolean 	true或falsetrue代表设置成功false代表设置失败
        '''
        return self.send_request(*_CopyTradeEndpoints.set_instruments, **to_local(locals()))

    # GET / 交易员历史分润明细
    def get_profit_sharing_details(self, after: str = '', before: str = '', limit: str = '', proxies={},
                                   proxy_host: str = None):
        '''
        交易员获取获取最近三个月的分润明细。
        https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading-get-profit-sharing-details
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        after             	String  	否       	请求此id之前（更旧的数据）的分页内容，传的值为对应接口的profitSharingId
        before            	String  	否       	请求此id之后（更新的数据）的分页内容，传的值为对应接口的profitSharingId
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	产品ID
        profitSharingAmt  	String  	分润额，没有分润时，默认返回0
        nickName          	String  	跟单人的昵称
        profitSharingId   	String  	分润ID
        ts                	String  	分润时间
        '''
        return self.send_request(*_CopyTradeEndpoints.get_profit_sharing_details, **to_local(locals()))

    # GET / 交易员历史分润汇总
    def get_total_profit_sharing(self, proxies={}, proxy_host: str = None):
        '''
        交易员获取自入驻平台以来，累计获得的总分润金额。
        https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading-get-total-profit-sharing
        
        限速：5次/2s
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	分润币种
        totalProfitSharingAmt	String  	历史分润汇总
        '''
        return self.send_request(*_CopyTradeEndpoints.get_total_profit_sharing, **to_local(locals()))

    # GET / 交易员待分润明细
    def get_unrealized_profit_sharing_details(self, proxies={}, proxy_host: str = None):
        '''
        交易员获取预计在下一个周期分到的分润金额明细。<!- 1-2-3 -->当有跟单仓位平仓时，待分润明细会进行更新。
        https://www.okx.com/docs-v5/zh/#order-book-trading-copy-trading-get-unrealized-profit-sharing-details
        
        限速：5次/2s
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	分润币种，e.g.USDT
        unrealizedProfitSharingAmt	String  	待分润额
        nickName          	String  	跟单人昵称
        ts                	String  	数据更新时间
        '''
        return self.send_request(*_CopyTradeEndpoints.get_unrealized_profit_sharing_details, **to_local(locals()))

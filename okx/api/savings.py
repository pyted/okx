'''
余币宝
https://www.okx.com/docs-v5/zh/#financial-product-savings
'''
from paux.param import to_local
from okx.api._client import Client


class _SavingsEndpoints():
    get_balance = ['/api/v5/finance/savings/balance', 'GET']  # GET / 获取余币宝余额
    set_purchase_redempt = ['/api/v5/finance/savings/purchase-redempt', 'POST']  # POST / 余币宝申购/赎回
    set_lending_rate = ['/api/v5/finance/savings/set-lending-rate', 'POST']  # POST / 设置余币宝借贷利率
    get_lending_history = ['/api/v5/finance/savings/lending-history', 'GET']  # GET / 获取余币宝出借明细
    get_lending_rate_summary = ['/api/v5/finance/savings/lending-rate-summary', 'GET']  # GET / 获取市场借贷信息（公共）
    get_lending_rate_history = ['/api/v5/finance/savings/lending-rate-history', 'GET']  # GET / 获取市场借贷历史（公共）


class Savings(Client):

    # GET / 获取余币宝余额
    def get_balance(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/finance/savings/balance
        https://www.okx.com/docs-v5/zh/#financial-product-savings-get-saving-balance
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种，如BTC
        amt               	String  	币种数量
        earnings          	String  	币种持仓收益
        rate              	String  	最新出借利率
        loanAmt           	String  	已出借数量
        pendingAmt        	String  	未出借数量
        redemptAmt        	String  	赎回中的数量（已废弃）
        '''
        return self.send_request(*_SavingsEndpoints.get_balance, **to_local(locals()))

    # POST / 余币宝申购/赎回
    def set_purchase_redempt(self, ccy: str, amt: str, side: str, rate: str, proxies={}, proxy_host: str = None):
        '''
        仅资金账户中的资产支持余币宝申购。
        https://www.okx.com/docs-v5/zh/#financial-product-savings-post-savings-purchase-redemption
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种名称，如BTC
        amt               	String  	是       	申购/赎回 数量
        side              	String  	是       	操作类型purchase：申购redempt：赎回
        rate              	String  	是       	申购年利率仅适用于申购，新申购的利率会覆盖上次申购的利率参数取值范围在1%到365%之间
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种名称
        amt               	String  	申购/赎回 数量
        side              	String  	操作类型
        rate              	String  	申购年利率
        '''
        return self.send_request(*_SavingsEndpoints.set_purchase_redempt, **to_local(locals()))

    # POST / 设置余币宝借贷利率
    def set_lending_rate(self, ccy: str, rate: str, proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/finance/savings/set-lending-rate
        https://www.okx.com/docs-v5/zh/#financial-product-savings-post-set-lending-rate
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种名称，如BTC
        rate              	String  	是       	贷出年利率参数取值范围在1%到365%之间
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种名称，如BTC
        rate              	String  	贷出年利率
        '''
        return self.send_request(*_SavingsEndpoints.set_lending_rate, **to_local(locals()))

    # GET / 获取余币宝出借明细
    def get_lending_history(self, ccy: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                            proxy_host: str = None):
        '''
        GET /api/v5/finance/savings/lending-history
        https://www.okx.com/docs-v5/zh/#financial-product-savings-get-lending-history
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为 100，不填默认返回 100 条
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种，如BTC
        amt               	String  	出借数量
        earnings          	String  	已赚取利息
        rate              	String  	出借年利率
        ts                	String  	出借时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_SavingsEndpoints.get_lending_history, **to_local(locals()))

    # GET / 获取市场借贷信息（公共）
    def get_lending_rate_summary(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        公共接口无须鉴权
        https://www.okx.com/docs-v5/zh/#financial-product-savings-get-public-borrow-info-public
        
        限速：6次/s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种，如BTC
        avgAmt            	String  	过去24小时平均借贷量
        avgAmtUsd         	String  	过去24小时平均借贷美元价值
        avgRate           	String  	过去24小时平均借出利率
        preRate           	String  	上一次借贷年利率
        estRate           	String  	下一次预估借贷年利率
        '''
        return self.send_request(*_SavingsEndpoints.get_lending_rate_summary, **to_local(locals()))

    # GET / 获取市场借贷历史（公共）
    def get_lending_rate_history(self, ccy: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                                 proxy_host: str = None):
        '''
        公共接口无须鉴权<!- 1-2-3 -->返回2021年12月14日后的记录
        https://www.okx.com/docs-v5/zh/#financial-product-savings-get-public-borrow-history-public
        
        限速：6次/s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条如果不指定ccy,会返回同一个ts下的全部数据，不受limit限制
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种，如BTC
        amt               	String  	市场总出借数量
        rate              	String  	出借年利率
        ts                	String  	时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_SavingsEndpoints.get_lending_rate_history, **to_local(locals()))

'''
交易大数据
https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api
'''
from paux.param import to_local
from okx.api._client import Client


class _TradingStatisticsEndpoints():
    get_support_coin = ['/api/v5/rubik/stat/trading-data/support-coin', 'GET']  # 获取交易大数据支持币种
    get_taker_volume = ['/api/v5/rubik/stat/taker-volume', 'GET']  # 获取主动买入/卖出情况
    get_loan_ratio = ['/api/v5/rubik/stat/margin/loan-ratio', 'GET']  # 获取杠杆多空比
    get_long_short_account_ratio = ['/api/v5/rubik/stat/contracts/long-short-account-ratio', 'GET']  # 获取合约多空持仓人数比
    get_contracts_open_interest_volume = ['/api/v5/rubik/stat/contracts/open-interest-volume', 'GET']  # 获取合约持仓量及交易量
    get_option_open_interest_volume = ['/api/v5/rubik/stat/option/open-interest-volume', 'GET']  # 获取期权持仓量及交易量
    get_open_interest_volume_ratio = ['/api/v5/rubik/stat/option/open-interest-volume-ratio', 'GET']  # 看涨/看跌期权合约 持仓总量比/交易总量比
    get_open_interest_volume_expiry = ['/api/v5/rubik/stat/option/open-interest-volume-expiry', 'GET']  # 看涨看跌持仓总量及交易总量（按到期日分）
    get_open_interest_volume_strike = ['/api/v5/rubik/stat/option/open-interest-volume-strike', 'GET']  # 看涨看跌持仓总量及交易总量（按执行价格分）
    get_taker_block_volume = ['/api/v5/rubik/stat/option/taker-block-volume', 'GET']  # 看跌/看涨期权合约 主动买入/卖出量


class TradingStatistics(Client):

    # 获取交易大数据支持币种
    def get_support_coin(self, proxies={}, proxy_host: str = None):
        '''
        获取支持交易大数据的币种
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-support-coin
        
        限速：5次/2s
        限速规则：IP
    
        
        返回参数:
        Parameter         	Type    	Description
        contract          	Array of strings	合约交易大数据接口功能支持的币种
        option            	Array of strings	期权交易大数据接口功能支持的币种
        spot              	Array of strings	现货交易大数据接口功能支持的币种
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_support_coin, **to_local(locals()))

    # 获取主动买入/卖出情况
    def get_taker_volume(self, ccy: str, instType: str, begin: str = '', end: str = '', period: str = '', proxies={},
                         proxy_host: str = None):
        '''
        获取taker主动买入和卖出的交易量
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-taker-volume
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        instType          	String  	是       	产品类型，币币："SPOT" , 衍生品："CONTRACTS"
        begin             	String  	否       	开始时间，例如：1597026383085
        end               	String  	否       	结束时间，例如：1597026383011
        period            	String  	否       	时间粒度，默认值5m。支持[5m/1H/1D]5m粒度最多只能查询两天之内的数据1H粒度最多只能查询30天之内的数据1D粒度最多只能查询180天之内的数据
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	数据产生时间
        sellVol           	String  	卖出量
        buyVol            	String  	买入量
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_taker_volume, **to_local(locals()))

    # 获取杠杆多空比
    def get_loan_ratio(self, ccy: str, begin: str = '', end: str = '', period: str = '', proxies={},
                       proxy_host: str = None):
        '''
        获取借入计价货币与借入交易货币的累计数额比值。
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-margin-lending-ratio
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        begin             	String  	否       	开始时间，例如：1597026383085
        end               	String  	否       	结束时间，例如：1597026383011
        period            	String  	否       	时间粒度，默认值5m。支持[5m/1H/1D]5m粒度最多只能查询两天之内的数据1H粒度最多只能查询30天之内的数据1D粒度最多只能查询180天之内的数据
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	数据产生时间
        ratio             	String  	多空比值
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_loan_ratio, **to_local(locals()))

    # 获取合约多空持仓人数比
    def get_long_short_account_ratio(self, ccy: str, begin: str = '', end: str = '', period: str = '', proxies={},
                                     proxy_host: str = None):
        '''
        获取交割永续净开多持仓用户数与净开空持仓用户数的比值。
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-long-short-ratio
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        begin             	String  	否       	开始时间，例如：1597026383085
        end               	String  	否       	结束时间，例如：1597026383011
        period            	String  	否       	时间粒度，默认值5m。支持[5m/1H/1D]5m粒度最多只能查询两天之内的数据1H粒度最多只能查询30天之内的数据1D粒度最多只能查询180天之内的数据
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	数据产生时间
        ratio             	String  	多空人数比
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_long_short_account_ratio, **to_local(locals()))

    # 获取合约持仓量及交易量
    def get_contracts_open_interest_volume(self, ccy: str, begin: str = '', end: str = '', period: str = '', proxies={},
                                           proxy_host: str = None):
        '''
        获取交割永续的持仓量和交易量。
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-contracts-open-interest-and-volume
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        begin             	String  	否       	开始时间，例如：1597026383085
        end               	String  	否       	结束时间，例如：1597026383011
        period            	String  	否       	时间粒度，默认值5m。支持[5m/1H/1D]5m粒度最多只能查询两天之内的数据1H粒度最多只能查询30天之内的数据1D粒度最多只能查询180天之内的数据
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	数据产生时间
        oi                	String  	持仓总量（USD）
        vol               	String  	交易总量（USD）
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_contracts_open_interest_volume, **to_local(locals()))

    # 获取期权持仓量及交易量
    def get_option_open_interest_volume(self, ccy: str, period: str = '', proxies={}, proxy_host: str = None):
        '''
        获取期权的持仓量和交易量。
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-options-open-interest-and-volume
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        period            	String  	否       	时间粒度，默认值8H。支持[8H/1D]每个粒度最多只能查询72条数据
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	数据产生时间
        oi                	String  	持仓总量（BTC）
        vol               	String  	交易总量（BTC）
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_option_open_interest_volume, **to_local(locals()))

    # 看涨/看跌期权合约 持仓总量比/交易总量比
    def get_open_interest_volume_ratio(self, ccy: str, period: str = '', proxies={}, proxy_host: str = None):
        '''
        获取看涨期权和看跌期权的持仓量比值，以及交易量比值。
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-put-call-ratio
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        period            	String  	否       	时间粒度，默认值8H。支持[8H/1D]每个粒度最多只能查询72条数据
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	数据产生时间
        oiRatio           	String  	看涨/看跌 持仓总量比
        volRatio          	String  	看涨/看跌 交易总量比
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_open_interest_volume_ratio, **to_local(locals()))

    # 看涨看跌持仓总量及交易总量（按到期日分）
    def get_open_interest_volume_expiry(self, ccy: str, period: str = '', proxies={}, proxy_host: str = None):
        '''
        获取每个到期日上看涨期权和看跌期权的持仓量和交易量。
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-open-interest-and-volume-expiry
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        period            	String  	否       	时间粒度，默认值8H。支持[8H/1D]每个粒度仅展示最新的一份数据
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	数据产生时间
        expTime           	String  	到期日（格式: YYYYMMDD，例如："20210623"）
        callOI            	String  	看涨持仓总量（以币为单位）
        putOI             	String  	看跌持仓总量（以币为单位）
        callVol           	String  	看涨交易总量（以币为单位）
        putVol            	String  	看跌交易总量（以币为单位）
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_open_interest_volume_expiry, **to_local(locals()))

    # 看涨看跌持仓总量及交易总量（按执行价格分）
    def get_open_interest_volume_strike(self, ccy: str, expTime: str, period: str = '', proxies={},
                                        proxy_host: str = None):
        '''
        获取看涨期权和看跌期权的taker主动买入和卖出的交易量。
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-open-interest-and-volume-strike
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        expTime           	String  	是       	到期日（格式: YYYYMMdd，例如："20210623"）
        period            	String  	否       	时间粒度，默认值8H。支持[8H/1D]每个粒度仅展示最新的一份数据
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	数据产生时间
        strike            	String  	执行价格
        callOI            	String  	看涨持仓总量（以币为单位）
        putOI             	String  	看跌持仓总量（以币为单位）
        callVol           	String  	看涨交易总量（以币为单位）
        putVol            	String  	看跌交易总量（以币为单位）
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_open_interest_volume_strike, **to_local(locals()))

    # 看跌/看涨期权合约 主动买入/卖出量
    def get_taker_block_volume(self, ccy: str, period: str = '', proxies={}, proxy_host: str = None):
        '''
        该指标展示某一时刻，单位时间内看跌/看涨期权的主动（taker）买入/卖出交易量
        https://www.okx.com/docs-v5/zh/#trading-statistics-rest-api-get-taker-flow
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        period            	String  	否       	时间粒度，默认值8H。支持[8H/1D]每个粒度仅展示最新的一份数据
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	数据产生时间
        callBuyVol        	String  	看涨买入量  以结算货币为单位
        callSellVol       	String  	看涨卖出量  以结算货币为单位
        putBuyVol         	String  	看跌买入量  以结算货币为单位
        putSellVol        	String  	看跌卖出量  以结算货币为单位
        callBlockVol      	String  	看涨大单
        putBlockVol       	String  	看跌大单
        '''
        return self.send_request(*_TradingStatisticsEndpoints.get_taker_block_volume, **to_local(locals()))

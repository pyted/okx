'''
公共数据
https://www.okx.com/docs-v5/zh/#public-data
'''

from paux.param import to_local
from okx.api._client import Client


class _PublicEndpoints():
    get_instruments = ['/api/v5/public/instruments', 'GET']  # 获取交易产品基础信息
    get_delivery_exercise_history = ['/api/v5/public/delivery-exercise-history', 'GET']  # 获取交割和行权记录
    get_open_interest = ['/api/v5/public/open-interest', 'GET']  # 获取持仓总量
    get_funding_rate = ['/api/v5/public/funding-rate', 'GET']  # 获取永续合约当前资金费率
    get_funding_rate_history = ['/api/v5/public/funding-rate-history', 'GET']  # 获取永续合约历史资金费率
    get_price_limit = ['/api/v5/public/price-limit', 'GET']  # 获取限价
    get_opt_summary = ['/api/v5/public/opt-summary', 'GET']  # 获取期权定价
    get_estimated_price = ['/api/v5/public/estimated-price', 'GET']  # 获取预估交割/行权价格
    get_discount_rate_interest_free_quota = ['/api/v5/public/discount-rate-interest-free-quota', 'GET']  # 获取免息额度和币种折算率等级
    get_time = ['/api/v5/public/time', 'GET']  # 获取系统时间
    get_mark_price = ['/api/v5/public/mark-price', 'GET']  # 获取标记价格
    get_position_tiers = ['/api/v5/public/position-tiers', 'GET']  # 获取衍生品仓位档位
    get_interest_rate_loan_quota = ['/api/v5/public/interest-rate-loan-quota', 'GET']  # 获取市场借币杠杆利率和借币限额
    get_vip_interest_rate_loan_quota = ['/api/v5/public/vip-interest-rate-loan-quota', 'GET']  # 获取尊享借币杠杆利率和借币限额
    get_underlying = ['/api/v5/public/underlying', 'GET']  # 获取衍生品标的指数
    get_insurance_fund = ['/api/v5/public/insurance-fund', 'GET']  # 获取风险准备金余额
    get_convert_contract_coin = ['/api/v5/public/convert-contract-coin', 'GET']  # 张币转换
    get_instrument_tick_bands = ['/api/v5/public/instrument-tick-bands', 'GET']  # 获取期权价格梯度
    get_index_tickers = ['/api/v5/market/index-tickers', 'GET']  # 获取指数行情
    get_index_candles = ['/api/v5/market/index-candles', 'GET']  # 获取指数K线数据
    get_history_index_candles = ['/api/v5/market/history-index-candles', 'GET']  # 获取指数历史K线数据
    get_mark_price_candles = ['/api/v5/market/mark-price-candles', 'GET']  # 获取标记价格K线数据
    get_history_mark_price_candles = ['/api/v5/market/history-mark-price-candles', 'GET']  # 获取标记价格历史K线数据
    get_open_oracle = ['/api/v5/market/open-oracle', 'GET']  # Oracle  上链交易数据
    get_exchange_rate = ['/api/v5/market/exchange-rate', 'GET']  # 获取法币汇率
    get_index_components = ['/api/v5/market/index-components', 'GET']  # 获取指数成分数据


class Public(Client):

    # 获取交易产品基础信息
    def get_instruments(self, instType: str, uly: str = '', instFamily: str = '', instId: str = '', proxies={},
                        proxy_host: str = None):
        '''
        获取所有可交易产品的信息列表。
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-instruments
        
        限速：20次/2s
        限速规则：IP +instType
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	可选      	标的指数，仅适用于交割/永续/期权，期权必填
        instFamily        	String  	否       	交易品种，仅适用于交割/永续/期权
        instId            	String  	否       	产品ID
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品id， 如BTC-USD-SWAP
        uly               	String  	标的指数，如BTC-USD，仅适用于交割/永续/期权
        instFamily        	String  	交易品种，如BTC-USD，仅适用于交割/永续/期权
        category          	String  	币种类别（已废弃）
        baseCcy           	String  	交易货币币种，如BTC-USDT中的BTC，仅适用于币币/币币杠杆
        quoteCcy          	String  	计价货币币种，如BTC-USDT中的USDT，仅适用于币币/币币杠杆
        settleCcy         	String  	盈亏结算和保证金币种，如BTC仅适用于交割/永续/期权
        ctVal             	String  	合约面值，仅适用于交割/永续/期权
        ctMult            	String  	合约乘数，仅适用于交割/永续/期权
        ctValCcy          	String  	合约面值计价币种，仅适用于交割/永续/期权
        optType           	String  	期权类型，C或P仅适用于期权
        stk               	String  	行权价格，仅适用于期权
        listTime          	String  	上线时间Unix时间戳的毫秒数格式，如1597026383085
        expTime           	String  	产品下线时间适用于币币/杠杆/交割/永续/期权，对于交割/期权，为交割/行权日期；亦可以为产品下线时间，有变动就会推送。
        lever             	String  	该instId支持的最大杠杆倍数，不适用于币币、期权
        tickSz            	String  	下单价格精度，如0.0001对于期权来说，是梯度中的最小下单价格精度，如果想要获取期权价格梯度，请使用"获取期权价格梯度"接口
        lotSz             	String  	下单数量精度，如 BTC-USDT-SWAP：1
        minSz             	String  	最小下单数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
        ctType            	String  	linear：正向合约inverse：反向合约仅适用于交割/永续
        alias             	String  	合约日期别名this_week：本周next_week：次周quarter：季度next_quarter：次季度仅适用于交割
        state             	String  	产品状态live：交易中suspend：暂停中preopen：预上线，如：交割和期权的新合约在 live 之前，会有 preopen 状态test：测试中（测试产品，不可交易）
        maxLmtSz          	String  	合约或现货限价单的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
        maxMktSz          	String  	合约或现货市价单的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“USDT”
        maxTwapSz         	String  	合约或现货时间加权单的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
        maxIcebergSz      	String  	合约或现货冰山委托的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
        maxTriggerSz      	String  	合约或现货计划委托委托的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
        maxStopSz         	String  	合约或现货止盈止损市价委托的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“USDT”
        '''
        return self.send_request(*_PublicEndpoints.get_instruments, **to_local(locals()))

    # 获取交割和行权记录
    def get_delivery_exercise_history(self, instType: str, uly: str = '', instFamily: str = '', after: str = '',
                                      before: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        获取3个月内的交割合约的交割记录和期权的行权记录
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-delivery-exercise-history
        
        限速：40次/2s
        限速规则：IP + (instrumentType + uly)
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型FUTURES：交割合约OPTION：期权
        uly               	String  	可选      	标的指数uly与instFamily必须传一个,若传两个，以instFamily为主
        instFamily        	String  	可选      	交易品种uly与instFamily必须传一个,若传两个，以instFamily为主
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	交割/行权日期，Unix时间戳的毫秒数格式，如1597026383085
        details           	String  	详细数据
        > instId          	String  	交割/行权的合约ID
        > px              	String  	交割/行权的价格
        > type            	String  	类型delivery：交割exercised：实值已行权expired_otm：虚值已过期
        '''
        return self.send_request(*_PublicEndpoints.get_delivery_exercise_history, **to_local(locals()))

    # 获取持仓总量
    def get_open_interest(self, instType: str, uly: str = '', instFamily: str = '', instId: str = '', proxies={},
                          proxy_host: str = None):
        '''
        查询单个交易产品的市场的持仓总量
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-open-interest
        
        限速：20次/2s
        限速规则：IP + instrumentID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	可选      	标的指数适用于交割/永续/期权期权情况下，uly和instFamily必须传一个
        instFamily        	String  	可选      	交易品种适用于交割/永续/期权期权情况下，uly和instFamily必须传一个
        instId            	String  	否       	产品ID，如BTC-USD-180216仅适用于交割/永续/期权
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品ID
        oi                	String  	持仓量（按张折算）
        oiCcy             	String  	持仓量（按币折算）
        ts                	String  	数据返回时间，Unix时间戳的毫秒数格式 ，如1597026383085
        '''
        return self.send_request(*_PublicEndpoints.get_open_interest, **to_local(locals()))

    # 获取永续合约当前资金费率
    def get_funding_rate(self, instId: str, proxies={}, proxy_host: str = None):
        '''
        获取当前资金费率
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-funding-rate
        
        限速：20次/2s
        限速规则：IP +instrumentID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID ，如BTC-USD-SWAP仅适用于永续
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型SWAP：永续合约
        instId            	String  	产品ID，如BTC-USD-SWAP
        fundingRate       	String  	资金费率
        nextFundingRate   	String  	下一期预测资金费率
        fundingTime       	String  	资金费时间 ，Unix时间戳的毫秒数格式，如1597026383085
        nextFundingTime   	String  	下一期资金费时间 ，Unix时间戳的毫秒数格式，如1622851200000
        '''
        return self.send_request(*_PublicEndpoints.get_funding_rate, **to_local(locals()))

    # 获取永续合约历史资金费率
    def get_funding_rate_history(self, instId: str, before: str = '', after: str = '', limit: str = '', proxies={},
                                 proxy_host: str = None):
        '''
        获取最近3个月的历史资金费率
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-funding-rate-history
        
        限速：10次/2s
        限速规则：IP +instrumentID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID ，如BTC-USD-SWAP仅适用于永续
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的fundingTime
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的fundingTime
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型SWAP：永续合约
        instId            	String  	产品ID，如BTC-USD-SWAP
        fundingRate       	String  	预计资金费率
        realizedRate      	String  	实际资金费率
        fundingTime       	String  	资金费时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_PublicEndpoints.get_funding_rate_history, **to_local(locals()))

    # 获取限价
    def get_price_limit(self, instId: str, proxies={}, proxy_host: str = None):
        '''
        查询单个交易产品的最高买价和最低卖价
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-limit-price
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT-SWAP仅适用于交割/永续/期权
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权
        instId            	String  	产品ID ，如BTC-USDT-SWAP
        buyLmt            	String  	最高买价
        sellLmt           	String  	最低卖价
        ts                	String  	限价数据更新时间 ，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_PublicEndpoints.get_price_limit, **to_local(locals()))

    # 获取期权定价
    def get_opt_summary(self, uly: str = '', instFamily: str = '', expTime: str = '', proxies={},
                        proxy_host: str = None):
        '''
        查询期权详细信息
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-option-market-data
        
        限速：20次/2s
        限速规则：IP +uly
    
        请求参数:
        Parameter         	Type    	Required	Description

        uly               	String  	可选      	标的指数，仅适用于期权uly与instFamily必须传一个,若传两个，以instFamily为主
        instFamily        	String  	可选      	交易品种，仅适用于期权uly与instFamily必须传一个,若传两个，以instFamily为主
        expTime           	String  	否       	合约到期日，格式为"YYMMDD"，如 "200527"
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型OPTION：期权
        instId            	String  	产品ID，如BTC-USD-200103-5500-C
        uly               	String  	标的指数
        delta             	String  	期权价格对uly价格的敏感度
        gamma             	String  	delta对uly价格的敏感度
        vega              	String  	权价格对隐含波动率的敏感度
        theta             	String  	期权价格对剩余期限的敏感度
        deltaBS           	String  	BS模式下期权价格对uly价格的敏感度
        gammaBS           	String  	BS模式下delta对uly价格的敏感度
        vegaBS            	String  	BS模式下期权价格对隐含波动率的敏感度
        thetaBS           	String  	BS模式下期权价格对剩余期限的敏感度
        lever             	String  	杠杆倍数
        markVol           	String  	标记波动率
        bidVol            	String  	bid波动率
        askVol            	String  	ask波动率
        realVol           	String  	已实现波动率（目前该字段暂未启用）
        volLv             	String  	价平期权的隐含波动率
        fwdPx             	String  	远期价格
        ts                	String  	数据更新时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_PublicEndpoints.get_opt_summary, **to_local(locals()))

    # 获取预估交割/行权价格
    def get_estimated_price(self, instId: str, proxies={}, proxy_host: str = None):
        '''
        获取交割合约和期权预估交割/行权价。交割/行权预估价只有交割/行权前一小时才有返回值
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-estimated-delivery-exercise-price
        
        限速：10次/2s
        限速规则：IP +instrumentID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID， 如BTC-USD-200214仅适用于交割/期权
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型FUTURES：交割合约OPTION：期权
        instId            	String  	产品ID， 如BTC-USD-180216
        settlePx          	String  	预估交割、行权价格
        ts                	String  	数据返回时间 ，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_PublicEndpoints.get_estimated_price, **to_local(locals()))

    # 获取免息额度和币种折算率等级
    def get_discount_rate_interest_free_quota(self, ccy: str = '', discountLv: str = '', proxies={},
                                              proxy_host: str = None):
        '''
        获取免息额度和币种折算率等级
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-discount-rate-and-interest-free-quota
        
        限速：2 次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种
        discountLv        	String  	否       	折算率等级1:第一档2:第二档3:第三档4:第四档5:第五档
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种
        amt               	String  	免息金额
        discountLv        	String  	折算率等级折算率等级说明
        discountInfo      	Array   	币种折算率详情
        > discountRate    	String  	折算率
        > maxAmt          	String  	梯度区间上限（美元）， “”表示正无穷
        > minAmt          	String  	梯度区间下限（美元）， 最小值是0
        '''
        return self.send_request(*_PublicEndpoints.get_discount_rate_interest_free_quota, **to_local(locals()))

    # 获取系统时间
    def get_time(self, proxies={}, proxy_host: str = None):
        '''
        获取系统时间
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-system-time
        
        限速：10次/2s
        限速规则：IP
    
        
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	系统时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_PublicEndpoints.get_time, **to_local(locals()))

    # 获取标记价格
    def get_mark_price(self, instType: str, uly: str = '', instFamily: str = '', instId: str = '', proxies={},
                       proxy_host: str = None):
        '''
        为了防止个别用户恶意操控市场导致合约价格波动剧烈，我们根据现货指数和合理基差设定标记价格。
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-mark-price
        
        限速：10次/2s
        限速规则：IP +instrumentID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数适用于交割/永续/期权
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品ID，如BTC-USD-SWAP
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        instId            	String  	产品ID，如BTC-USD-200214
        markPx            	String  	标记价格
        ts                	String  	接口数据返回时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_PublicEndpoints.get_mark_price, **to_local(locals()))

    # 获取衍生品仓位档位
    def get_position_tiers(self, instType: str, tdMode: str, uly: str = '', instFamily: str = '', instId: str = '',
                           ccy: str = '', tier: str = '', proxies={}, proxy_host: str = None):
        '''
        全部仓位档位对应信息，当前最高可开杠杆倍数由您的借币持仓和保证金率决定。
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-position-tiers
        
        限速：10次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        tdMode            	String  	是       	保证金模式isolated：逐仓 ；cross：全仓
        uly               	String  	可选      	标的指数，支持多uly，半角逗号分隔，最大不超过3个当产品类型是永续、交割、期权之一时，uly与instFamily必须传一个，若传两个，以instFamily为主当产品类型是MARGIN时忽略
        instFamily        	String  	可选      	交易品种，支持多instFamily，半角逗号分隔，最大不超过5个当产品类型是永续、交割、期权之一时，uly与instFamily必须传一个，若传两个，以instFamily为主
        instId            	String  	可选      	产品ID，支持多instId，半角逗号分隔，最大不超过5个仅适用币币杠杆，instId和ccy必须传一个，若传两个，以instId为主
        ccy               	String  	可选      	保证金币种仅适用杠杆全仓，该值生效时，返回的是跨币种保证金模式和组合保证金模式下的借币量
        tier              	String  	否       	查指定档位
        返回参数:
        Parameter         	Type    	Description
        uly               	String  	标的指数适用于交割/永续/期权
        instFamily        	String  	交易品种适用于交割/永续/期权
        instId            	String  	币对
        tier              	String  	仓位档位
        minSz             	String  	该档位最少借币量或者持仓数量  杠杆/期权/永续/交割 最小持仓量 默认0当ccy参数生效时，返回ccy的最小借币量
        maxSz             	String  	该档位最多借币量或者持仓数量  杠杆/期权/永续/交割当ccy参数生效时，返回ccy的最大借币量
        mmr               	String  	维持保证金率
        imr               	String  	最低初始保证金率
        maxLever          	String  	最高可用杠杆倍数
        optMgnFactor      	String  	期权保证金系数  （仅适用于期权）
        quoteMaxLoan      	String  	计价货币  最大借币量（仅适用于杠杆，且instId参数生效时），例如 BTC-USDT   里的 USDT最大借币量
        baseMaxLoan       	String  	交易货币  最大借币量（仅适用于杠杆，且instId参数生效时），例如 BTC-USDT   里的 BTC最大借币量
        '''
        return self.send_request(*_PublicEndpoints.get_position_tiers, **to_local(locals()))

    # 获取市场借币杠杆利率和借币限额
    def get_interest_rate_loan_quota(self, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/public/interest-rate-loan-quota
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-interest-rate-and-loan-quota
        
        限速：2次/2s
        限速规则：IP
    
        
        返回参数:
        Parameter         	Type    	Description
        basic             	Array   	基础利率和借币限额
        > ccy             	String  	币种
        > rate            	String  	基础杠杆日利率
        > quota           	String  	基础借币限额
        vip               	Array   	专业用户
        > level           	String  	账户交易手续费等级，如VIP1
        > loanQuotaCoef   	String  	借币限额系数
        > irDiscount      	String  	利率的折扣率(已废弃)
        regular           	Array   	普通用户
        > level           	String  	账户交易手续费等级，如Lv1
        > loanQuotaCoef   	String  	借币限额系数
        > irDiscount      	String  	利率的折扣率(已废弃)
        '''
        return self.send_request(*_PublicEndpoints.get_interest_rate_loan_quota, **to_local(locals()))

    # 获取尊享借币杠杆利率和借币限额
    def get_vip_interest_rate_loan_quota(self, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/public/vip-interest-rate-loan-quota
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-interest-rate-and-loan-quota-for-vip-loans
        
        限速：2次/2s
        限速规则：IP
    
        
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种
        rate              	String  	借币日利率
        quota             	String  	基础借币限额(已废弃)
        levelList         	Array   	不同VIP等级下的借币限额信息
        > level           	String  	用户VIP等级，如VIP5
        > loanQuota       	String  	借币限额
        '''
        return self.send_request(*_PublicEndpoints.get_vip_interest_rate_loan_quota, **to_local(locals()))

    # 获取衍生品标的指数
    def get_underlying(self, instType: str, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/public/underlying
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-underlying
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权
        返回参数:
        Parameter         	Type    	Description
        uly               	Array   	标的指数   如：BTC-USDT
        '''
        return self.send_request(*_PublicEndpoints.get_underlying, **to_local(locals()))

    # 获取风险准备金余额
    def get_insurance_fund(self, instType: str, type: str = '', uly: str = '', instFamily: str = '', ccy: str = '',
                           before: str = '', after: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        通过该接口获取系统风险准备金余额信息
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-insurance-fund
        
        限速：10次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        type              	String  	否       	风险准备金类型liquidation_balance_deposit：强平注入 ；bankruptcy_loss：穿仓亏损 ；platform_revenue：平台收入注入默认返回全部类型
        uly               	String  	可选      	标的指数交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主
        instFamily        	String  	可选      	交易品种交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主
        ccy               	String  	可选      	币种， 仅适用币币杠杆，且必填写
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        total             	String  	平台风险准备金总计，单位为USD
        instFamily        	String  	交易品种适用于交割/永续/期权
        details           	Array of objects	风险准备金详情
        > balance         	String  	风险准备金总量
        > amt             	String  	风险准备金更新数量
        > ccy             	String  	风险准备金总量对应的币种
        > type            	String  	风险准备金类型
        > ts              	String  	风险准备金更新时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_PublicEndpoints.get_insurance_fund, **to_local(locals()))

    # 张币转换
    def get_convert_contract_coin(self, instId: str, sz: str, type: str = '', px: str = '', unit: str = '',
                                  opType: str = '', proxies={}, proxy_host: str = None):
        '''
        由币转换为张，或者张转换为币。
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-unit-convert
        
        限速：10次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        type              	String  	否       	转换类型1: 币转张2: 张转币默认为 1
        instId            	String  	是       	产品ID，仅适用于交割/永续/期权
        sz                	String  	是       	数量，币转张时，为币的数量，张转币时，为张的数量。张的数量，只能是正整数
        px                	String  	可选      	委托价格币本位合约的张币转换时必填；U本位合约，usdt 与张的转换时，必填；coin 与张的转换时，可不填；期权的张币转换时，可不填。
        unit              	String  	否       	币的单位，coin: 币，usds: usdt 或者 usdc仅适用于交割和永续合约的U本位合约
        opType            	String  	否       	将要下单的类型open: 开仓时将sz舍位close: 平仓时将sz四舍五入默认值为close适用于交割永续
        返回参数:
        Parameter         	Type    	Description
        type              	String  	转换类型1: 币转张2: 张转币
        instId            	String  	产品ID
        px                	String  	委托价格
        sz                	String  	数量，张转币时，为币的数量，币转张时，为张的数量
        unit              	String  	币的单位，coin: 币，usds: usdt 或者 usdc
        '''
        return self.send_request(*_PublicEndpoints.get_convert_contract_coin, **to_local(locals()))

    # 获取期权价格梯度
    def get_instrument_tick_bands(self, instType: str = '', instFamily: str = '', proxies={}, proxy_host: str = None):
        '''
        获取期权价格梯度信息
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-option-tickbands
        
        限速：5次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	Yes     	产品类型OPTION：期权
        instFamily        	String  	No      	交易品种，仅适用于期权
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instFamily        	String  	交易品种
        tickBand          	String  	下单价格精度梯度
        > minPx           	String  	最低下单价格
        > maxPx           	String  	最高下单价格
        > tickSz          	String  	下单价格精度，如 0.0001
        '''
        return self.send_request(*_PublicEndpoints.get_instrument_tick_bands, **to_local(locals()))

    # 获取指数行情
    def get_index_tickers(self, quoteCcy: str = '', instId: str = '', proxies={}, proxy_host: str = None):
        '''
        获取指数行情数据
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-index-tickers
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        quoteCcy          	String  	可选      	指数计价单位， 目前只有USD/USDT/BTC/USDC为计价单位的指数，quoteCcy和instId必须填写一个
        instId            	String  	可选      	指数，如BTC-USD
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	指数
        idxPx             	String  	最新指数价格
        high24h           	String  	24小时指数最高价格
        low24h            	String  	24小时指数最低价格
        open24h           	String  	24小时指数开盘价格
        sodUtc0           	String  	UTC 0  时开盘价
        sodUtc8           	String  	UTC+8 时开盘价
        ts                	String  	指数价格更新时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_PublicEndpoints.get_index_tickers, **to_local(locals()))

    # 获取指数K线数据
    def get_index_candles(self, instId: str, after: str = '', before: str = '', bar: str = '', limit: str = '',
                          proxies={}, proxy_host: str = None):
        '''
        指数K线数据每个粒度最多可获取最近1,440条。
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-index-candlesticks
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	现货指数，如BTC-USD
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts, 单独使用时，会返回最新的数据。
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M/3M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/1Wutc/1Mutc/3Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	开始时间，Unix时间戳的毫秒数格式，如1597026383085
        o                 	String  	开盘价格
        h                 	String  	最高价格
        l                 	String  	最低价格
        c                 	String  	收盘价格
        confirm           	String  	K线状态0代表 K 线未完结，1代表 K 线已完结。
        '''
        return self.send_request(*_PublicEndpoints.get_index_candles, **to_local(locals()))

    # 获取指数历史K线数据
    def get_history_index_candles(self, instId: str, after: str = '', before: str = '', bar: str = '', limit: str = '',
                                  proxies={}, proxy_host: str = None):
        '''
        获取最近几年的指数K线数据
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-index-candlesticks-history
        
        限速：10次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	现货指数，如BTC-USD
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts, 单独使用时，会返回最新的数据。
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M]UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/1Wutc/1Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	开始时间，Unix时间戳的毫秒数格式，如1597026383085
        o                 	String  	开盘价格
        h                 	String  	最高价格
        l                 	String  	最低价格
        c                 	String  	收盘价格
        confirm           	String  	K线状态0代表 K 线未完结，1代表 K 线已完结。
        '''
        return self.send_request(*_PublicEndpoints.get_history_index_candles, **to_local(locals()))

    # 获取标记价格K线数据
    def get_mark_price_candles(self, instId: str, after: str = '', before: str = '', bar: str = '', limit: str = '',
                               proxies={}, proxy_host: str = None):
        '''
        标记价格K线数据每个粒度最多可获取最近1,440条。
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-mark-price-candlesticks
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-SWAP
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts, 单独使用时，会返回最新的数据。
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M/3M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/1Wutc/1Mutc/3Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	开始时间，Unix时间戳的毫秒数格式，如1597026383085
        o                 	String  	开盘价格
        h                 	String  	最高价格
        l                 	String  	最低价格
        c                 	String  	收盘价格
        confirm           	String  	K线状态0代表 K 线未完结，1代表 K 线已完结。
        '''
        return self.send_request(*_PublicEndpoints.get_mark_price_candles, **to_local(locals()))

    # 获取标记价格历史K线数据
    def get_history_mark_price_candles(self, instId: str, after: str = '', before: str = '', bar: str = '',
                                       limit: str = '', proxies={}, proxy_host: str = None):
        '''
        获取最近几年的标记价格K线数据
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-mark-price-candlesticks-history
        
        限速：10次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-SWAP
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts, 单独使用时，会返回最新的数据。
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/1Wutc/1Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	开始时间，Unix时间戳的毫秒数格式，如1597026383085
        o                 	String  	开盘价格
        h                 	String  	最高价格
        l                 	String  	最低价格
        c                 	String  	收盘价格
        confirm           	String  	K线状态0代表 K 线未完结，1代表 K 线已完结。
        '''
        return self.send_request(*_PublicEndpoints.get_history_mark_price_candles, **to_local(locals()))

    # Oracle  上链交易数据
    def get_open_oracle(self, proxies={}, proxy_host: str = None):
        '''
        获取使用 Open Oracle 智能合约签名后加密资产价格。
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-oracle
        
        限速：1次/5s
        限速规则：IP
    
        
        返回参数:
        Parameter         	Type    	Description
        messages          	String  	数组包含对[ kind，timestamp，key，value]进行ABI编码的值，其中kind恒等于prices，timestamp是获取价格的时间戳，key是加密资产（例如，ETH），value是资产价格
        prices            	String  	价格
        signatures        	String  	每个消息的以太坊兼容ECDSA签名的数组
        timestamp         	String  	获取最新数据点的时间，Unix时间戳,如1597026387
        '''
        return self.send_request(*_PublicEndpoints.get_open_oracle, **to_local(locals()))

    # 获取法币汇率
    def get_exchange_rate(self, proxies={}, proxy_host: str = None):
        '''
        该接口提供的是2周的平均汇率数据
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-exchange-rate
        
        限速：1次/2s
        限速规则：IP
    
        
        返回参数:
        Parameter         	Type    	Description
        usdCny            	String  	人民币兑美元汇率
        '''
        return self.send_request(*_PublicEndpoints.get_exchange_rate, **to_local(locals()))

    # 获取指数成分数据
    def get_index_components(self, index: str, proxies={}, proxy_host: str = None):
        '''
        查询市场上的指数成分信息数据
        https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-index-components
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        index             	String  	是       	指数，如BTC-USDT
        返回参数:
        Parameter         	Type    	Description
        index             	String  	指数名称
        last              	String  	最新指数价格
        ts                	String  	数据产生时间，Unix时间戳的毫秒数格式， 如1597026383085
        components        	String  	成分
        > exch            	String  	交易所名称
        > symbol          	String  	采集的币对名称
        > symPx           	String  	采集的币对价格
        > wgt             	String  	权重
        > cnvPx           	String  	换算成指数后的价格
        '''
        return self.send_request(*_PublicEndpoints.get_index_components, **to_local(locals()))

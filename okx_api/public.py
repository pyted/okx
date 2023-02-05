from paux.param import to_local
from okx_api._client import Client


class _PublicEndpoints:
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
    get_liquidation_orders = ['/api/v5/public/liquidation-orders', 'GET']  # 获取平台公共爆仓单信息
    get_mark_price = ['/api/v5/public/mark-price', 'GET']  # 获取标记价格
    get_position_tiers = ['/api/v5/public/position-tiers', 'GET']  # 获取衍生品仓位档位
    get_interest_rate_loan_quota = ['/api/v5/public/interest-rate-loan-quota', 'GET']  # 获取市场借币杠杆利率和借币限额
    get_vip_interest_rate_loan_quota = ['/api/v5/public/vip-interest-rate-loan-quota', 'GET']  # 获取尊享借币杠杆利率和借币限额
    get_underlying = ['/api/v5/public/underlying', 'GET']  # 获取衍生品标的指数
    get_insurance_fund = ['/api/v5/public/insurance-fund', 'GET']  # 获取风险准备金余额
    get_convert_contract_coin = ['/api/v5/public/convert-contract-coin', 'GET']  # 张币转换
    get_option_trades = ['/api/v5/public/option-trades', 'GET']  # 获取期权公共成交数据


class Public(Client):
    # 获取交易产品基础信息
    def get_instruments(self, instType: str, uly: str = '', instFamily: str = '', instId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-instruments

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	可选      	标的指数，仅适用于交割/永续/期权，期权必填
        instFamily        	String  	否       	交易品种，仅适用于交割/永续/期权
        instId            	String  	否       	产品ID
        '''
        return self.send_request(*_PublicEndpoints.get_instruments, **to_local(locals()))

    # 获取交割和行权记录
    def get_delivery_exercise_history(self, instType: str, uly: str = '', instFamily: str = '', after: str = '',
                                      before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-delivery-exercise-history

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型FUTURES：交割合约OPTION：期权
        uly               	String  	可选      	标的指数uly与instFamily必须传一个,若传两个，以instFamily为主
        instFamily        	String  	可选      	交易品种uly与instFamily必须传一个,若传两个，以instFamily为主
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_PublicEndpoints.get_delivery_exercise_history, **to_local(locals()))

    # 获取持仓总量
    def get_open_interest(self, instType: str, uly: str = '', instFamily: str = '', instId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-open-interest

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	可选      	标的指数适用于交割/永续/期权期权情况下，uly和instFamily必须传一个
        instFamily        	String  	可选      	交易品种适用于交割/永续/期权期权情况下，uly和instFamily必须传一个
        instId            	String  	否       	产品ID，如BTC-USD-180216仅适用于交割/永续/期权
        '''
        return self.send_request(*_PublicEndpoints.get_open_interest, **to_local(locals()))

    # 获取永续合约当前资金费率
    def get_funding_rate(self, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-funding-rate

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID ，如BTC-USD-SWAP仅适用于永续
        '''
        return self.send_request(*_PublicEndpoints.get_funding_rate, **to_local(locals()))

    # 获取永续合约历史资金费率
    def get_funding_rate_history(self, instId: str, before: str = '', after: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-funding-rate-history

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID ，如BTC-USD-SWAP仅适用于永续
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的fundingTime
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的fundingTime
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_PublicEndpoints.get_funding_rate_history, **to_local(locals()))

    # 获取限价
    def get_price_limit(self, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-limit-price

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT-SWAP仅适用于交割/永续/期权
        '''
        return self.send_request(*_PublicEndpoints.get_price_limit, **to_local(locals()))

    # 获取期权定价
    def get_opt_summary(self, uly: str = '', instFamily: str = '', expTime: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-option-market-data

        请求参数：
        Parameter         	Type    	Required	Description
        uly               	String  	可选      	标的指数，仅适用于期权uly与instFamily必须传一个,若传两个，以instFamily为主
        instFamily        	String  	可选      	交易品种，仅适用于期权uly与instFamily必须传一个,若传两个，以instFamily为主
        expTime           	String  	否       	合约到期日，格式为"YYMMDD"，如 "200527"
        '''
        return self.send_request(*_PublicEndpoints.get_opt_summary, **to_local(locals()))

    # 获取预估交割/行权价格
    def get_estimated_price(self, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-estimated-delivery-exercise-price

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID， 如BTC-USD-200214仅适用于交割/期权
        '''
        return self.send_request(*_PublicEndpoints.get_estimated_price, **to_local(locals()))

    # 获取免息额度和币种折算率等级
    def get_discount_rate_interest_free_quota(self, ccy: str = '', discountLv: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-discount-rate-level-and-interest-free-quota

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种
        discountLv        	String  	否       	折算率等级1:第一档2:第二档3:第三档4:第四档5:第五档
        '''
        return self.send_request(*_PublicEndpoints.get_discount_rate_interest_free_quota, **to_local(locals()))

    # 获取系统时间
    def get_time(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-system-time
        '''
        return self.send_request(*_PublicEndpoints.get_time, **to_local(locals()))

    # 获取平台公共爆仓单信息
    def get_liquidation_orders(self, instType: str, mgnMode: str = '', instId: str = '', ccy: str = '', uly: str = '',
                               instFamily: str = '', alias: str = '', state: str = '', before: str = '',
                               after: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-liquidation-orders

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        mgnMode           	String  	否       	保证金模式cross：全仓isolated：逐仓
        instId            	String  	否       	产品ID，仅适用于币币杠杆
        ccy               	String  	否       	币种 ，仅适用于币币杠杆（全仓）
        uly               	String  	可选      	标的指数交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主
        instFamily        	String  	可选      	交易品种交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主
        alias             	String  	可选      	this_week：本周next_week：次周quarter：季度next_quarter：次季度交割合约情况下，该参数必填
        state             	String  	否       	状态unfilled：未成交filled：已成交默认为unfilled交割/永续合约情况下，该参数必填
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_PublicEndpoints.get_liquidation_orders, **to_local(locals()))

    # 获取标记价格
    def get_mark_price(self, instType: str, uly: str = '', instFamily: str = '', instId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-mark-price

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数适用于交割/永续/期权
        instFamily        	String  	否       	交易品种适用于交割/永续/期权
        instId            	String  	否       	产品ID，如BTC-USD-SWAP
        '''
        return self.send_request(*_PublicEndpoints.get_mark_price, **to_local(locals()))

    # 获取衍生品仓位档位
    def get_position_tiers(self, instType: str, tdMode: str, uly: str = '', instFamily: str = '', instId: str = '',
                           ccy: str = '', tier: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-position-tiers

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        tdMode            	String  	是       	保证金模式isolated：逐仓 ；cross：全仓
        uly               	String  	可选      	标的指数，支持多uly，半角逗号分隔，最大不超过3个当产品类型是永续、交割、期权之一时，uly与instFamily必须传一个，若传两个，以instFamily为主当产品类型是MARGIN时忽略
        instFamily        	String  	可选      	交易品种，支持多instFamily，半角逗号分隔，最大不超过5个当产品类型是永续、交割、期权之一时，uly与instFamily必须传一个，若传两个，以instFamily为主
        instId            	String  	可选      	产品ID，支持多instId，半角逗号分隔，最大不超过5个仅适用币币杠杆，instId和ccy必须传一个，若传两个，以instId为主
        ccy               	String  	可选      	保证金币种仅适用杠杆全仓，该值生效时，返回的是跨币种保证金模式和组合保证金模式下的借币量
        tier              	String  	否       	查指定档位
        '''
        return self.send_request(*_PublicEndpoints.get_position_tiers, **to_local(locals()))

    # 获取市场借币杠杆利率和借币限额
    def get_interest_rate_loan_quota(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-interest-rate-and-loan-quota-for-market-loans
        '''
        return self.send_request(*_PublicEndpoints.get_interest_rate_loan_quota, **to_local(locals()))

    # 获取尊享借币杠杆利率和借币限额
    def get_vip_interest_rate_loan_quota(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-interest-rate-and-loan-quota-for-vip-loans
        '''
        return self.send_request(*_PublicEndpoints.get_vip_interest_rate_loan_quota, **to_local(locals()))

    # 获取衍生品标的指数
    def get_underlying(self, instType: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-underlying

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权
        '''
        return self.send_request(*_PublicEndpoints.get_underlying, **to_local(locals()))

    # 获取风险准备金余额
    def get_insurance_fund(self, instType: str, type: str = '', uly: str = '', instFamily: str = '', ccy: str = '',
                           before: str = '', after: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-insurance-fund

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        type              	String  	否       	风险准备金类型liquidation_balance_deposit：强平注入 ；bankruptcy_loss：穿仓亏损 ；platform_revenue：平台收入注入默认返回全部类型
        uly               	String  	可选      	标的指数交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主
        instFamily        	String  	可选      	交易品种交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主
        ccy               	String  	可选      	币种， 仅适用币币杠杆，且必填写
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_PublicEndpoints.get_insurance_fund, **to_local(locals()))

    # 张币转换
    def get_convert_contract_coin(self, instId: str, sz: str, type: str = '', px: str = '', unit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-unit-convert

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，仅适用于交割/永续/期权
        sz                	String  	是       	数量，币转张时，为币的数量，张转币时，为张的数量。张的数量，只能是正整数
        type              	String  	否       	转换类型1: 币转张，当张为小数时，会进一取整2: 张转币默认为 1
        px                	String  	可选      	委托价格币本位合约的张币转换时必填；U本位合约，usdt 与张的转换时，必填；coin 与张的转换时，可不填；期权的张币转换时，可不填。
        unit              	String  	否       	币的单位，coin: 币，usds: usdt 或者 usdc仅适用于交割和永续合约的U本位合约
        '''
        return self.send_request(*_PublicEndpoints.get_convert_contract_coin, **to_local(locals()))

    # 获取期权公共成交数据
    def get_option_trades(self, instId: str = '', instFamily: str = '', optType: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-public-data-get-option-trades

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	可选      	产品ID，如 BTC-USD-221230-4000-C，instId和instFamily必须传一个，若传两个，以instId为主
        instFamily        	String  	可选      	交易品种，如 BTC-USD
        optType           	String  	否       	期权类型，C：看涨期权P：看跌期权
        '''
        return self.send_request(*_PublicEndpoints.get_option_trades, **to_local(locals()))

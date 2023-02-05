from paux.param import to_local
from okx_api._client import Client


class _AccountEndpoints:
    get_balance = ['/api/v5/account/balance', 'GET']  # 查看账户余额
    get_positions = ['/api/v5/account/positions', 'GET']  # 查看持仓信息
    get_positions_history = ['/api/v5/account/positions-history', 'GET']  # 查看历史持仓信息
    get_account_position_risk = ['/api/v5/account/account-position-risk', 'GET']  # 查看账户持仓风险
    get_bills = ['/api/v5/account/bills', 'GET']  # 账单流水查询（近七天）
    get_bills_archive = ['/api/v5/account/bills-archive', 'GET']  # 账单流水查询（近三月）
    get_config = ['/api/v5/account/config', 'GET']  # 查看账户配置
    set_set_position_mode = ['/api/v5/account/set-position-mode', 'POST']  # 设置持仓模式
    set_set_leverage = ['/api/v5/account/set-leverage', 'POST']  # 设置杠杆倍数
    get_max_size = ['/api/v5/account/max-size', 'GET']  # 获取最大可买卖/开仓数量
    get_max_avail_size = ['/api/v5/account/max-avail-size', 'GET']  # 获取最大可用数量
    set_margin_balance = ['/api/v5/account/position/margin-balance', 'POST']  # 调整保证金
    get_leverage_info = ['/api/v5/account/leverage-info', 'GET']  # 获取杠杆倍数
    get_max_loan = ['/api/v5/account/max-loan', 'GET']  # 获取交易产品最大可借
    get_trade_fee = ['/api/v5/account/trade-fee', 'GET']  # 获取当前账户交易手续费费率
    get_interest_accrued = ['/api/v5/account/interest-accrued', 'GET']  # 获取计息记录
    get_interest_rate = ['/api/v5/account/interest-rate', 'GET']  # 获取用户当前杠杆借币利率
    set_set_greeks = ['/api/v5/account/set-greeks', 'POST']  # 期权greeks的PA/BS切换
    set_set_isolated_mode = ['/api/v5/account/set-isolated-mode', 'POST']  # 逐仓交易设置
    get_max_withdrawal = ['/api/v5/account/max-withdrawal', 'GET']  # 查看账户最大可转余额
    get_risk_state = ['/api/v5/account/risk-state', 'GET']  # 查看账户特定风险状态
    set_quick_margin_borrow_repay = ['/api/v5/account/quick-margin-borrow-repay', 'POST']  # 一键借币模式手动借币还币
    get_quick_margin_borrow_repay_history = ['/api/v5/account/quick-margin-borrow-repay-history', 'GET']  # 获取一键借币还币历史
    set_borrow_repay = ['/api/v5/account/borrow-repay', 'POST']  # 尊享借币还币
    get_borrow_repay_history = ['/api/v5/account/borrow-repay-history', 'GET']  # 获取尊享借币还币历史
    get_vip_interest_accrued = ['/api/v5/account/vip-interest-accrued', 'GET']  # 获取尊享借币计息记录
    get_vip_interest_deducted = ['/api/v5/account/vip-interest-deducted', 'GET']  # 获取尊享借币扣息记录
    get_vip_loan_order_list = ['/api/v5/account/vip-loan-order-list', 'GET']  # 尊享借币订单列表
    get_vip_loan_order_detail = ['/api/v5/account/vip-loan-order-detail', 'GET']  # 尊享借币订单详情
    get_interest_limits = ['/api/v5/account/interest-limits', 'GET']  # 获取借币利率与限额
    set_simulated_margin = ['/api/v5/account/simulated_margin', 'POST']  # 组合保证金的虚拟持仓保证金计算
    get_greeks = ['/api/v5/account/greeks', 'GET']  # 查看账户Greeks
    get_position_tiers = ['/api/v5/account/position-tiers', 'GET']  # 获取组合保证金模式全仓限制
    set_set_riskOffset_type = ['/api/v5/account/set-riskOffset-type', 'POST']  # 设置组合保证金账户风险对冲模式
    set_activate_option = ['/api/v5/account/activate-option', 'POST']  # 开通期权交易


class Account(Client):
    # 查看账户余额
    def get_balance(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-balance

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        '''
        return self.send_request(*_AccountEndpoints.get_balance, **to_local(locals()))

    # 查看持仓信息
    def get_positions(self, instType: str = '', instId: str = '', posId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-positions

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	否       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权instType和instId同时传入的时候会校验instId与instType是否一致。
        instId            	String  	否       	交易产品ID，如：BTC-USD-190927-5000-C支持多个instId查询（不超过10个），半角逗号分隔
        posId             	String  	否       	持仓ID支持多个posId查询（不超过20个），半角逗号分割
        '''
        return self.send_request(*_AccountEndpoints.get_positions, **to_local(locals()))

    # 查看历史持仓信息
    def get_positions_history(self, instType: str = '', instId: str = '', mgnMode: str = '', type: str = '',
                              posId: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-positions-history

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	否       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        instId            	String  	否       	交易产品ID，如：BTC-USD-SWAP
        mgnMode           	String  	否       	保证金模式cross：全仓，isolated：逐仓
        type              	String  	否       	平仓类型1：部分平仓;2：完全平仓;3：强平;4：强减;5：ADL自动减仓;状态叠加时，以最新的平仓类型为准状态为准。
        posId             	String  	否       	持仓ID
        after             	String  	否       	查询仓位更新 (uTime) 之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询仓位更新 (uTime) 之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_AccountEndpoints.get_positions_history, **to_local(locals()))

    # 查看账户持仓风险
    def get_account_position_risk(self, instType: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-account-and-position-risk

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	否       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        '''
        return self.send_request(*_AccountEndpoints.get_account_position_risk, **to_local(locals()))

    # 账单流水查询（近七天）
    def get_bills(self, instType: str = '', ccy: str = '', mgnMode: str = '', ctType: str = '', type: str = '',
                  subType: str = '', after: str = '', before: str = '', begin: str = '', end: str = '',
                  limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-bills-details-last-7-days

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	否       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        ccy               	String  	否       	账单币种
        mgnMode           	String  	否       	仓位类型isolated：逐仓cross：全仓
        ctType            	String  	否       	linear： 正向合约inverse： 反向合约仅交割/永续有效
        type              	String  	否       	账单类型1：划转2：交易3：交割4：自动换币5：强平6：保证金划转7：扣息8：资金费9：自动减仓10：穿仓补偿11：系统换币12：策略划拨13：对冲减仓14: 大宗交易15: 一键借币18: 分润22: 一键还债
        subType           	String  	否       	账单子类型1：买入2：卖出3：开多4：开空5：平多6：平空9：市场借币扣息11：转入12：转出14：尊享借币扣息160：手动追加保证金161：手动减少保证金162：自动追加保证金114：自动换币买入115：自动换币卖出118：系统换币转入119：系统换币转出100：强减平多101：强减平空102：强减买入103：强减卖出104：强平平多105：强平平空106：强平买入107：强平卖出110：强平换币转入111：强平换币转出125：自动减仓平多126：自动减仓平空127：自动减仓买入128：自动减仓卖出131：对冲买入132：对冲卖出170：到期行权171：到期被行权172：到期作废112：交割平多113：交割平空117：交割/期权穿仓补偿173：资金费支出174：资金费收入200:系统转入201:手动转入202:系统转出203:手动转出204: 大宗交易买205: 大宗交易卖206: 大宗交易开多207: 大宗交易开空208: 大宗交易平多209: 大宗交易平空210: 手动借币211: 手动还币212: 自动借币213：自动还币"16：强制还币17：强制借币还息224: 还债转入225: 还债转出250: 分润支出;251: 分润退还;252: 分润收入;
        after             	String  	否       	请求此id之前（更旧的数据）的分页内容，传的值为对应接口的billId
        before            	String  	否       	请求此id之后（更新的数据）的分页内容，传的值为对应接口的billId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_AccountEndpoints.get_bills, **to_local(locals()))

    # 账单流水查询（近三月）
    def get_bills_archive(self, instType: str = '', ccy: str = '', mgnMode: str = '', ctType: str = '', type: str = '',
                          subType: str = '', after: str = '', before: str = '', begin: str = '', end: str = '',
                          limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-bills-details-last-3-months

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	否       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        ccy               	String  	否       	账单币种
        mgnMode           	String  	否       	仓位类型isolated：逐仓cross：全仓
        ctType            	String  	否       	linear： 正向合约inverse： 反向合约仅交割/永续有效
        type              	String  	否       	账单类型1：划转2：交易3：交割4：自动换币5：强平6：保证金划转7：扣息8：资金费9：自动减仓10：穿仓补偿11：系统换币12：策略划拨13：对冲减仓14: 大宗交易15: 一键借币22: 一键还债18: 分润
        subType           	String  	否       	账单子类型1：买入2：卖出3：开多4：开空5：平多6：平空9：市场借币扣息11：转入12：转出14：尊享借币扣息160：手动追加保证金161：手动减少保证金162：自动追加保证金114：自动换币买入115：自动换币卖出118：系统换币转入119：系统换币转出100：强减平多101：强减平空102：强减买入103：强减卖出104：强平平多105：强平平空106：强平买入107：强平卖出110：强平换币转入111：强平换币转出125：自动减仓平多126：自动减仓平空127：自动减仓买入128：自动减仓卖出131：对冲买入132：对冲卖出170：到期行权171：到期被行权172：到期作废112：交割平多113：交割平空117：交割/期权穿仓补偿173：资金费支出174：资金费收入200:系统转入201:手动转入202:系统转出203:手动转出204: 大宗交易买205: 大宗交易卖206: 大宗交易开多207: 大宗交易开空208: 大宗交易平多209: 大宗交易平空210: 手动借币211: 手动还币212: 自动借币213：自动还币"16：强制还币17：强制借币还息224: 还债转入225: 还债转出250: 分润支出;251: 分润退还;252: 分润收入;
        after             	String  	否       	请求此id之前（更旧的数据）的分页内容，传的值为对应接口的billId
        before            	String  	否       	请求此id之后（更新的数据）的分页内容，传的值为对应接口的billId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_AccountEndpoints.get_bills_archive, **to_local(locals()))

    # 查看账户配置
    def get_config(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-account-configuration
        '''
        return self.send_request(*_AccountEndpoints.get_config, **to_local(locals()))

    # 设置持仓模式
    def set_set_position_mode(self, posMode: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-set-position-mode

        请求参数：
        Parameter         	Type    	Required	Description
        posMode           	String  	是       	持仓方式long_short_mode：双向持仓net_mode：单向持仓仅适用交割/永续
        '''
        return self.send_request(*_AccountEndpoints.set_set_position_mode, **to_local(locals()))

    # 设置杠杆倍数
    def set_set_leverage(self, lever: str, mgnMode: str, instId: str = '', ccy: str = '', posSide: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-set-leverage

        请求参数：
        Parameter         	Type    	Required	Description
        lever             	String  	是       	杠杆倍数
        mgnMode           	String  	是       	保证金模式isolated：逐仓cross：全仓如果ccy有效传值，该参数值只能为cross。
        instId            	String  	可选      	产品ID：币对、合约instId和ccy至少要传一个；如果两个都传，默认使用instId
        ccy               	String  	可选      	保证金币种仅适用于跨币种保证金模式的全仓币币杠杆。设置自动借币的杠杆倍数时必填
        posSide           	String  	可选      	持仓方向long：双向持仓多头short：双向持仓空头仅适用于逐仓交割/永续在双向持仓且保证金模式为逐仓条件下必填
        '''
        return self.send_request(*_AccountEndpoints.set_set_leverage, **to_local(locals()))

    # 获取最大可买卖/开仓数量
    def get_max_size(self, instId: str, tdMode: str, ccy: str = '', px: str = '', leverage: str = '',
                     unSpotOffset: bool = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-maximum-buy-sell-amount-or-open-amount

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔
        tdMode            	String  	是       	交易模式cross：全仓isolated：逐仓cash：非保证金
        ccy               	String  	可选      	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        px                	String  	否       	委托价格当不填委托价时会按当前最新成交价计算当指定多个产品ID查询时，忽略该参数，按当前最新成交价计算
        leverage          	String  	否       	开仓杠杆倍数默认为当前杠杆倍数仅适用于币币杠杆/交割/永续
        unSpotOffset      	Boolean 	否       	true：禁止现货对冲，false：允许现货对冲默认为false仅适用于组合保证金模式开启现货对冲模式下有效，否则忽略此参数。
        '''
        return self.send_request(*_AccountEndpoints.get_max_size, **to_local(locals()))

    # 获取最大可用数量
    def get_max_avail_size(self, instId: str, tdMode: str, ccy: str = '', reduceOnly: bool = '',
                           unSpotOffset: bool = '', quickMgnType: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-maximum-available-tradable-amount

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔
        tdMode            	String  	是       	交易模式cross：全仓isolated：逐仓cash：非保证金
        ccy               	String  	可选      	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        reduceOnly        	Boolean 	否       	是否为只减仓模式，仅适用于币币杠杆
        unSpotOffset      	Boolean 	否       	true：禁止现货对冲，false：允许现货对冲默认为false仅适用于组合保证金模式开启现货对冲模式下有效，否则忽略此参数。
        quickMgnType      	String  	否       	一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动
        '''
        return self.send_request(*_AccountEndpoints.get_max_avail_size, **to_local(locals()))

    # 调整保证金
    def set_margin_balance(self, instId: str, posSide: str, type: str, amt: str, ccy: str = '', auto: bool = '',
                           loanTrans: bool = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-increase-decrease-margin

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID
        posSide           	String  	是       	持仓方向，默认值是netlong：双向持仓多头short：双向持仓空头net：单向持仓
        type              	String  	是       	增加/减少保证金add：增加，或者转入质押资产(一键借币)reduce：减少，或者转出质押资产（一键借币）
        amt               	String  	是       	增加或减少的保证金数量
        ccy               	String  	否       	增加或减少的保证金的币种，仅适用于逐仓自主划转和一键借币模式下的币币杠杆
        auto              	Boolean 	否       	是否自动借币转 true 或 false，默认false仅适用于逐仓自主划转保证金模式下的币币杠杆
        loanTrans         	Boolean 	否       	是否支持跨币种保证金模式或组合保证金模式下的借币转入/转出true 或 false，默认false
        '''
        return self.send_request(*_AccountEndpoints.set_margin_balance, **to_local(locals()))

    # 获取杠杆倍数
    def get_leverage_info(self, instId: str, mgnMode: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-leverage

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID支持多个instId查询，半角逗号分隔。instId个数不超过20个
        mgnMode           	String  	是       	保证金模式isolated：逐仓cross：全仓
        '''
        return self.send_request(*_AccountEndpoints.get_leverage_info, **to_local(locals()))

    # 获取交易产品最大可借
    def get_max_loan(self, instId: str, mgnMode: str, mgnCcy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-the-maximum-loan-of-instrument

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品 ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔
        mgnMode           	String  	是       	仓位类型isolated：逐仓cross：全仓
        mgnCcy            	String  	可选      	保证金币种，如BTC币币杠杆单币种全仓情况下必须指定保证金币种
        '''
        return self.send_request(*_AccountEndpoints.get_max_loan, **to_local(locals()))

    # 获取当前账户交易手续费费率
    def get_trade_fee(self, instType: str, instId: str = '', uly: str = '', instFamily: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-fee-rates

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        instId            	String  	否       	产品ID，如BTC-USDT仅适用于instType为币币/币币杠杆
        uly               	String  	否       	标的指数适用于交割/永续/期权，如BTC-USD
        instFamily        	String  	否       	交易品种适用于交割/永续/期权，如BTC-USD
        '''
        return self.send_request(*_AccountEndpoints.get_trade_fee, **to_local(locals()))

    # 获取计息记录
    def get_interest_accrued(self, type: str = '', ccy: str = '', instId: str = '', mgnMode: str = '', after: str = '',
                             before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-interest-accrued-data

        请求参数：
        Parameter         	Type    	Required	Description
        type              	String  	否       	借币类型1：尊享借币2：市场借币默认为市场借币
        ccy               	String  	否       	借贷币种，如BTC仅适用于市场借币仅适用于币币杠杆
        instId            	String  	否       	产品ID，如BTC-USDT仅适用于市场借币
        mgnMode           	String  	否       	保证金模式cross：全仓isolated：逐仓仅适用于市场借币
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_AccountEndpoints.get_interest_accrued, **to_local(locals()))

    # 获取用户当前杠杆借币利率
    def get_interest_rate(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-interest-rate

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种
        '''
        return self.send_request(*_AccountEndpoints.get_interest_rate, **to_local(locals()))

    # 期权greeks的PA/BS切换
    def set_set_greeks(self, greeksType: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-set-greeks-pa-bs

        请求参数：
        Parameter         	Type    	Required	Description
        greeksType        	String  	是       	希腊字母展示方式PA：币本位，BS：美元本位
        '''
        return self.send_request(*_AccountEndpoints.set_set_greeks, **to_local(locals()))

    # 逐仓交易设置
    def set_set_isolated_mode(self, isoMode: str, type: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-isolated-margin-trading-settings

        请求参数：
        Parameter         	Type    	Required	Description
        isoMode           	String  	是       	逐仓保证金划转模式automatic:开仓自动划转autonomy:自主划转quick_margin:一键借币
        type              	String  	是       	业务线类型MARGIN:币币杠杆CONTRACTS:合约
        '''
        return self.send_request(*_AccountEndpoints.set_set_isolated_mode, **to_local(locals()))

    # 查看账户最大可转余额
    def get_max_withdrawal(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-maximum-withdrawals

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        '''
        return self.send_request(*_AccountEndpoints.get_max_withdrawal, **to_local(locals()))

    # 查看账户特定风险状态
    def get_risk_state(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-account-risk-state
        '''
        return self.send_request(*_AccountEndpoints.get_risk_state, **to_local(locals()))

    # 一键借币模式手动借币还币
    def set_quick_margin_borrow_repay(self, instId: str, ccy: str, side: str, amt: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-manual-borrow-and-repay-in-quick-margin-mode

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT
        ccy               	String  	是       	借贷币种，如BTC
        side              	String  	是       	borrow：借币，repay：还币
        amt               	String  	是       	借/还币的数量
        '''
        return self.send_request(*_AccountEndpoints.set_quick_margin_borrow_repay, **to_local(locals()))

    # 获取一键借币还币历史
    def get_quick_margin_borrow_repay_history(self, instId: str = '', ccy: str = '', side: str = '', after: str = '',
                                              before: str = '', begin: str = '', end: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-manual-borrow-and-repay-history-in-quick-margin-mode

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	否       	产品ID，如 BTC-USDT
        ccy               	String  	否       	借贷币种，如BTC
        side              	String  	否       	borrow：借币，repay：还币
        after             	String  	否       	请求此 ID 之前（更旧的数据）的分页内容，传的值为对应接口的refId
        before            	String  	否       	请求此 ID 之后（更新的数据）的分页内容，传的值为对应接口的refId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_AccountEndpoints.get_quick_margin_borrow_repay_history, **to_local(locals()))

    # 尊享借币还币
    def set_borrow_repay(self, ccy: str, side: str, amt: str, ordId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-vip-loans-borrow-and-repay

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	是       	借贷币种，如BTC
        side              	String  	是       	borrow：借币，repay：还币
        amt               	String  	是       	借/还币的数量
        ordId             	String  	可选      	借币订单ID，还币时，该字段必填
        '''
        return self.send_request(*_AccountEndpoints.set_borrow_repay, **to_local(locals()))

    # 获取尊享借币还币历史
    def get_borrow_repay_history(self, ccy: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-borrow-and-repay-history-for-vip-loans

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	借贷币种，如BTC
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_AccountEndpoints.get_borrow_repay_history, **to_local(locals()))

    # 获取尊享借币计息记录
    def get_vip_interest_accrued(self, ccy: str = '', ordId: str = '', after: str = '', before: str = '',
                                 limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-vip-interest-accrued-data

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	借贷币种，如BTC，仅适用于币币杠杆
        ordId             	String  	否       	借币订单ID
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_AccountEndpoints.get_vip_interest_accrued, **to_local(locals()))

    # 获取尊享借币扣息记录
    def get_vip_interest_deducted(self, ordId: str = '', ccy: str = '', after: str = '', before: str = '',
                                  limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-vip-interest-deducted-data

        请求参数：
        Parameter         	Type    	Required	Description
        ordId             	String  	否       	借币订单ID
        ccy               	String  	否       	借贷币种，如BTC，仅适用于币币杠杆
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_AccountEndpoints.get_vip_interest_deducted, **to_local(locals()))

    # 尊享借币订单列表
    def get_vip_loan_order_list(self, ordId: str = '', state: str = '', ccy: str = '', after: str = '',
                                before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-vip-loan-order-list

        请求参数：
        Parameter         	Type    	Required	Description
        ordId             	String  	否       	借币订单ID
        state             	String  	否       	订单状态1:借币申请中2:借币中3:还币申请中4:已还币5:借币失败
        ccy               	String  	否       	借贷币种，如 BTC
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_AccountEndpoints.get_vip_loan_order_list, **to_local(locals()))

    # 尊享借币订单详情
    def get_vip_loan_order_detail(self, ordId: str, ccy: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-vip-loan-order-detail

        请求参数：
        Parameter         	Type    	Required	Description
        ordId             	String  	是       	借币订单ID
        ccy               	String  	否       	借贷币种，如 BTC
        after             	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        '''
        return self.send_request(*_AccountEndpoints.get_vip_loan_order_detail, **to_local(locals()))

    # 获取借币利率与限额
    def get_interest_limits(self, type: str = '', ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-borrow-interest-and-limit

        请求参数：
        Parameter         	Type    	Required	Description
        type              	String  	否       	借币类型1：尊享借币2：市场借币默认为市场借币
        ccy               	String  	否       	借贷币种，如BTC
        '''
        return self.send_request(*_AccountEndpoints.get_interest_limits, **to_local(locals()))

    # 组合保证金的虚拟持仓保证金计算
    def set_simulated_margin(self, instType: str = '', inclRealPos: bool = '', spotOffsetType: str = '',
                             simPos: object = '', instId: str = '', pos: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-position-builder

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	否       	产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权
        inclRealPos       	Boolean 	否       	是否代入已有仓位true：调整被代入的已有仓位信息false：不代入已有仓位，仅使用simPos里新增的模拟仓位进行计算,默认为True
        spotOffsetType    	String  	否       	现货对冲模式1：现货对冲模式U模式 2：现货对冲模式币模式 3：衍生品模式默认是 3
        simPos            	Array   	否       	调整持仓列表
        > instId          	String  	否       	交易产品ID
        > pos             	String  	否       	持仓量
        '''
        return self.send_request(*_AccountEndpoints.set_simulated_margin, **to_local(locals()))

    # 查看账户Greeks
    def get_greeks(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-greeks

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC
        '''
        return self.send_request(*_AccountEndpoints.get_greeks, **to_local(locals()))

    # 获取组合保证金模式全仓限制
    def get_position_tiers(self, instType: str, uly: str = '', instFamily: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-pm-limitation

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	可选      	标的指数，如BTC-USDT，支持多个查询（不超过3个），uly之间半角逗号分隔适用于交割/永续/期权uly与instFamily必须传一个,若传两个，以instFamily为主
        instFamily        	String  	可选      	交易品种，如BTC-USDT，支持多个查询（不超过5个），instFamily之间半角逗号分隔适用于交割/永续/期权uly与instFamily必须传一个,若传两个，以instFamily为主
        '''
        return self.send_request(*_AccountEndpoints.get_position_tiers, **to_local(locals()))

    # 设置组合保证金账户风险对冲模式
    def set_set_riskOffset_type(self, type: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-set-risk-offset-type

        请求参数：
        Parameter         	Type    	Required	Description
        type              	String  	是       	风险对冲模式1：现货对冲(USDT)2:现货对冲(币)3:衍生品对冲
        '''
        return self.send_request(*_AccountEndpoints.set_set_riskOffset_type, **to_local(locals()))

    # 开通期权交易
    def set_activate_option(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-account-activate-option
        '''
        return self.send_request(*_AccountEndpoints.set_activate_option, **to_local(locals()))

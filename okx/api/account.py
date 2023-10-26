'''
交易账户
https://www.okx.com/docs-v5/zh/#trading-account-rest-api
'''
from paux.param import to_local
from okx.api._client import Client


class _AccountEndpoints():
    get_balance = ['/api/v5/account/balance', 'GET']  # 查看账户余额
    get_positions = ['/api/v5/account/positions', 'GET']  # 查看持仓信息
    get_positions_history = ['/api/v5/account/positions-history', 'GET']  # 查看历史持仓信息
    get_account_position_risk = ['/api/v5/account/account-position-risk', 'GET']  # 查看账户持仓风险
    get_bills = ['/api/v5/account/bills', 'GET']  # 账单流水查询（近七天）
    get_bills_archive = ['/api/v5/account/bills-archive', 'GET']  # 账单流水查询（近三月）
    get_config = ['/api/v5/account/config', 'GET']  # 查看账户配置
    set_position_mode = ['/api/v5/account/set-position-mode', 'POST']  # 设置持仓模式
    set_leverage = ['/api/v5/account/set-leverage', 'POST']  # 设置杠杆倍数
    get_max_size = ['/api/v5/account/max-size', 'GET']  # 获取最大可买卖/开仓数量
    get_max_avail_size = ['/api/v5/account/max-avail-size', 'GET']  # 获取最大可用数量
    set_margin_balance = ['/api/v5/account/position/margin-balance', 'POST']  # 调整保证金
    get_leverage_info = ['/api/v5/account/leverage-info', 'GET']  # 获取杠杆倍数
    get_adjust_leverage_info = ['/api/v5/account/adjust-leverage-info', 'GET']  # 获取杠杆倍数预估信息
    get_max_loan = ['/api/v5/account/max-loan', 'GET']  # 获取交易产品最大可借
    get_trade_fee = ['/api/v5/account/trade-fee', 'GET']  # 获取当前账户交易手续费费率
    get_interest_accrued = ['/api/v5/account/interest-accrued', 'GET']  # 获取计息记录
    get_interest_rate = ['/api/v5/account/interest-rate', 'GET']  # 获取用户当前市场借币利率
    set_greeks = ['/api/v5/account/set-greeks', 'POST']  # 期权greeks的PA/BS切换
    set_isolated_mode = ['/api/v5/account/set-isolated-mode', 'POST']  # 逐仓交易设置
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
    get_position_tiers = ['/api/v5/account/position-tiers', 'GET']  # 获取组合保证金模式仓位限制
    set_riskOffset_type = ['/api/v5/account/set-riskOffset-type', 'POST']  # 设置组合保证金账户风险对冲模式
    set_activate_option = ['/api/v5/account/activate-option', 'POST']  # 开通期权交易
    set_auto_loan = ['/api/v5/account/set-auto-loan', 'POST']  # 设置自动借币
    set_account_level = ['/api/v5/account/set-account-level', 'POST']  # 设置账户模式
    set_mmp_reset = ['/api/v5/account/mmp-reset', 'POST']  # 重置 MMP 状态
    set_mmp_config = ['/api/v5/account/mmp-config', 'POST']  # 设置 MMP
    get_mmp_config = ['/api/v5/account/mmp-config', 'GET']  # 查看 MMP 配置


class Account(Client):

    # 查看账户余额
    def get_balance(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        获取交易账户中资金余额信息。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-balance
        
        限速：10次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        返回参数:
        Parameter         	Type    	Description
        uTime             	String  	账户信息的更新时间，Unix时间戳的毫秒数格式，如1597026383085
        totalEq           	String  	美金层面权益
        isoEq             	String  	美金层面逐仓仓位权益适用于单币种保证金模式和跨币种保证金模式和组合保证金模式
        adjEq             	String  	美金层面有效保证金适用于跨币种保证金模式和组合保证金模式
        ordFroz           	String  	美金层面全仓挂单占用保证金仅适用于跨币种保证金模式
        imr               	String  	美金层面占用保证金适用于跨币种保证金模式和组合保证金模式
        mmr               	String  	美金层面维持保证金适用于跨币种保证金模式和组合保证金模式
        borrowFroz        	String  	账户美金层面潜在借币占用保证金仅适用于跨币种保证金模式和组合保证金模式. 在其他账户模式下为"".
        mgnRatio          	String  	美金层面保证金率适用于跨币种保证金模式和组合保证金模式
        notionalUsd       	String  	以美金价值为单位的持仓数量，即仓位美金价值适用于跨币种保证金模式和组合保证金模式
        details           	Array   	各币种资产详细信息
        > ccy             	String  	币种
        > eq              	String  	币种总权益
        > cashBal         	String  	币种余额
        > uTime           	String  	币种余额信息的更新时间，Unix时间戳的毫秒数格式，如1597026383085
        > isoEq           	String  	币种逐仓仓位权益适用于单币种保证金模式和跨币种保证金模式和组合保证金模式
        > availEq         	String  	可用保证金适用于单币种保证金模式和跨币种保证金模式和组合保证金模式
        > disEq           	String  	美金层面币种折算权益
        > fixedBal        	String  	币种冻结金额
        > availBal        	String  	可用余额适用于简单交易模式、单币种保证金模式、跨币种保证金模式和组合保证金模式
        > frozenBal       	String  	币种占用金额
        > ordFrozen       	String  	挂单冻结数量
        > liab            	String  	币种负债额值为正数，如："21625.64"，适用于跨币种保证金模式和组合保证金模式
        > upl             	String  	未实现盈亏适用于单币种保证金模式和跨币种保证金模式和组合保证金模式
        > uplLiab         	String  	由于仓位未实现亏损导致的负债适用于跨币种保证金模式和组合保证金模式
        > crossLiab       	String  	币种全仓负债额适用于跨币种保证金模式和组合保证金模式
        > isoLiab         	String  	币种逐仓负债额适用于跨币种保证金模式和组合保证金模式
        > mgnRatio        	String  	保证金率适用于单币种保证金模式
        > interest        	String  	计息，应扣未扣利息。值为正数，如："9.01"，适用于跨币种保证金模式和组合保证金模式
        > twap            	String  	当前负债币种触发系统自动换币的风险0、1、2、3、4、5其中之一，数字越大代表您的负债币种触发自动换币概率越高适用于跨币种保证金模式和组合保证金模式
        > maxLoan         	String  	币种最大可借适用于跨币种保证金模式和组合保证金模式的全仓
        > eqUsd           	String  	币种权益美金价值
        > borrowFroz      	String  	币种美金层面潜在借币占用保证金仅适用于跨币种保证金模式和组合保证金模式. 在其他账户模式下为"".
        > notionalLever   	String  	币种杠杆倍数适用于单币种保证金模式
        > stgyEq          	String  	策略权益
        > isoUpl          	String  	逐仓未实现盈亏适用于单币种保证金模式和跨币种保证金模式和组合保证金模式
        > spotInUseAmt    	String  	现货对冲占用数量适用于组合保证金模式
        '''
        return self.send_request(*_AccountEndpoints.get_balance, **to_local(locals()))

    # 查看持仓信息
    def get_positions(self, instType: str = '', instId: str = '', posId: str = '', proxies={}, proxy_host: str = None):
        '''
        获取该账户下拥有实际持仓的信息。账户为买卖模式会显示净持仓（net），账户为开平仓模式下会分别返回开多（long）或开空（short）的仓位。按照仓位创建时间倒序排列。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-positions
        
        限速：10次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	否       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权instType和instId同时传入的时候会校验instId与instType是否一致。
        instId            	String  	否       	交易产品ID，如：BTC-USD-190927-5000-C支持多个instId查询（不超过10个），半角逗号分隔
        posId             	String  	否       	持仓ID支持多个posId查询（不超过20个）。存在有效期的属性，自最近一次完全平仓算起，满30天 posId 以及整个仓位会被清除。
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        mgnMode           	String  	保证金模式cross：全仓isolated：逐仓
        posId             	String  	持仓ID
        posSide           	String  	持仓方向long：开平仓模式开多，pos为正short：开平仓模式开空，pos为正net：买卖模式（交割/永续/期权：pos为正代表开多，pos为负代表开空。币币杠杆时，pos均为正，posCcy为交易货币时，代表开多；posCcy为计价货币时，代表开空。）
        pos               	String  	持仓数量，逐仓自主划转模式下，转入保证金后会产生pos为0的仓位
        baseBal           	String  	交易币余额，适用于币币杠杆（逐仓自主划转模式 和 一键借币模式）
        quoteBal          	String  	计价币余额 ，适用于币币杠杆（逐仓自主划转模式 和 一键借币模式）
        baseBorrowed      	String  	交易币已借，适用于 币币杠杆（逐仓一键借币模式）
        baseInterest      	String  	交易币计息，适用于 币币杠杆（逐仓一键借币模式）
        quoteBorrowed     	String  	计价币已借，适用于 币币杠杆（逐仓一键借币模式）
        quoteInterest     	String  	计价币计息，适用于 币币杠杆（逐仓一键借币模式）
        posCcy            	String  	仓位资产币种，仅适用于币币杠杆仓位
        availPos          	String  	可平仓数量，适用于币币杠杆,交割/永续（开平仓模式），期权对于杠杆仓位，平仓时，杠杆还清负债后，余下的部分会视为币币交易，如果想要减少币币交易的数量，可通过"获取最大可用数量"接口获取只减仓的可用数量。
        avgPx             	String  	开仓平均价
        upl               	String  	未实现收益（以标记价格计算）
        uplRatio          	String  	未实现收益率（以标记价格计算
        uplLastPx         	String  	以最新成交价格计算的未实现收益，主要做展示使用，实际值还是 upl
        uplRatioLastPx    	String  	以最新成交价格计算的未实现收益率
        instId            	String  	产品ID，如BTC-USD-180216
        lever             	String  	杠杆倍数，不适用于期权
        liqPx             	String  	预估强平价不适用于期权
        markPx            	String  	最新标记价格
        imr               	String  	初始保证金，仅适用于全仓
        margin            	String  	保证金余额，可增减，仅适用于逐仓
        mgnRatio          	String  	保证金率
        mmr               	String  	维持保证金
        liab              	String  	负债额，仅适用于币币杠杆
        liabCcy           	String  	负债币种，仅适用于币币杠杆
        interest          	String  	利息，已经生成的未扣利息
        tradeId           	String  	最新成交ID
        optVal            	String  	期权市值，仅适用于期权
        notionalUsd       	String  	以美金价值为单位的持仓数量
        adl               	String  	信号区分为5档，从1到5，数字越小代表adl强度越弱
        ccy               	String  	占用保证金的币种
        last              	String  	最新成交价
        idxPx             	String  	最新指数价格
        usdPx             	String  	美金价格
        bePx              	String  	盈亏平衡价
        deltaBS           	String  	美金本位持仓仓位delta，仅适用于期权
        deltaPA           	String  	币本位持仓仓位delta，仅适用于期权
        gammaBS           	String  	美金本位持仓仓位gamma，仅适用于期权
        gammaPA           	String  	币本位持仓仓位gamma，仅适用于期权
        thetaBS           	String  	美金本位持仓仓位theta，仅适用于期权
        thetaPA           	String  	币本位持仓仓位theta，仅适用于期权
        vegaBS            	String  	美金本位持仓仓位vega，仅适用于期权
        vegaPA            	String  	币本位持仓仓位vega，仅适用于期权
        cTime             	String  	持仓创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	最近一次持仓更新时间，Unix时间戳的毫秒数格式，如1597026383085
        spotInUseAmt      	String  	现货对冲占用数量适用于组合保证金模式
        spotInUseCcy      	String  	现货对冲占用币种，如BTC适用于组合保证金模式
        realizedPnl       	String  	已实现收益
        pnl               	String  	平仓订单累计收益额
        fee               	String  	累计手续费金额，正数代表平台返佣 ，负数代表平台扣除
        fundingFee        	String  	累计资金费用
        liqPenalty        	String  	累计爆仓罚金，有值时为负数。
        closeOrderAlgo    	Array   	平仓策略委托订单。调用策略委托下单，且closeFraction=1 时，该数组才会有值。
        > algoId          	String  	策略委托单ID
        > slTriggerPx     	String  	止损触发价
        > slTriggerPxType 	String  	止损触发价类型last：最新价格index：指数价格mark：标记价格
        > tpTriggerPx     	String  	止盈委托价
        > tpTriggerPxType 	String  	止盈触发价类型last：最新价格index：指数价格mark：标记价格
        > closeFraction   	String  	策略委托触发时，平仓的百分比。1 代表100%
        cTime             	String  	持仓创建时间，Unix时间戳的毫秒数格式，如1597026383085
        uTime             	String  	最近一次持仓更新时间，Unix时间戳的毫秒数格式，如1597026383085
        bizRefId          	String  	外部业务id，e.g. 体验券id
        bizRefType        	String  	外部业务类型
        '''
        return self.send_request(*_AccountEndpoints.get_positions, **to_local(locals()))

    # 查看历史持仓信息
    def get_positions_history(self, instType: str = '', instId: str = '', mgnMode: str = '', type: str = '',
                              posId: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                              proxy_host: str = None):
        '''
        获取最近3个月有更新的仓位信息，按照仓位更新时间倒序排列。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-positions-history
        
        限速：1次/10s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	否       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        instId            	String  	否       	交易产品ID，如：BTC-USD-SWAP
        mgnMode           	String  	否       	保证金模式cross：全仓，isolated：逐仓
        type              	String  	否       	平仓类型1：部分平仓;2：完全平仓;3：强平;4：强减;5：ADL自动减仓;状态叠加时，以最新的平仓类型为准状态为准。
        posId             	String  	否       	持仓ID。存在有效期的属性，自最近一次完全平仓算起，满30天 posId 会失效，之后的仓位，会使用新的 posId。
        after             	String  	否       	查询仓位更新 (uTime) 之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询仓位更新 (uTime) 之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	交易产品ID
        mgnMode           	String  	保证金模式cross：全仓，isolated：逐仓
        type              	String  	平仓类型1：部分平仓;2：完全平仓;3：强平;4：强减;5：ADL自动减仓;状态叠加时，以最新的平仓类型为准状态为准。
        cTime             	String  	仓位创建时间
        uTime             	String  	仓位更新时间
        openAvgPx         	String  	开仓均价
        closeAvgPx        	String  	平仓均价
        posId             	String  	仓位ID
        openMaxPos        	String  	最大持仓量
        closeTotalPos     	String  	累计平仓量
        realizedPnl       	String  	已实现收益
        fee               	String  	累计手续费金额，正数代表平台返佣 ，负数代表平台扣除
        fundingFee        	String  	累计资金费用
        liqPenalty        	String  	累计爆仓罚金，有值时为负数。
        pnl               	String  	平仓收益额
        pnlRatio          	String  	平仓收益率
        lever             	String  	杠杆倍数
        direction         	String  	持仓方向long：多short：空仅适用于币币杠杆/交割/永续/期权
        triggerPx         	String  	触发标记价格
        uly               	String  	标的指数
        ccy               	String  	占用保证金的币种
        '''
        return self.send_request(*_AccountEndpoints.get_positions_history, **to_local(locals()))

    # 查看账户持仓风险
    def get_account_position_risk(self, instType: str = '', proxies={}, proxy_host: str = None):
        '''
        查看账户整体风险。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-account-and-position-risk
        
        限速：10次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	否       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	获取账户信息数据的时间，Unix时间戳的毫秒数格式，如1597026383085
        adjEq             	String  	美金层面有效保证金适用于跨币种保证金模式和组合保证金模式
        balData           	Array   	币种资产信息
        > ccy             	String  	币种
        > eq              	String  	币种总权益
        > disEq           	String  	美金层面币种折算权益
        posData           	Array   	持仓详细信息
        > instType        	String  	产品类型
        > mgnMode         	String  	保证金模式cross：全仓isolated：逐仓
        > posId           	String  	持仓ID
        > instId          	String  	产品ID，如BTC-USD-180216
        > pos             	String  	以张为单位的持仓数量，逐仓自主划转模式下，转入保证金后会产生pos为0的仓位
        > baseBal         	String  	交易币余额，适用于币币杠杆（逐仓自主划转模式和逐仓一键借币模式）
        > quoteBal        	String  	计价币余额 ，适用于币币杠杆（逐仓自主划转模式和逐仓一键借币模式）
        > posSide         	String  	持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式（交割/永续/期权：pos为正代表开多，pos为负代表开空。币币杠杆：posCcy为交易货币时，代表开多；posCcy为计价货币时，代表开空。）
        > posCcy          	String  	仓位资产币种，仅适用于币币杠杆仓位
        > ccy             	String  	占用保证金的币种
        > notionalCcy     	String  	以币为单位的持仓数量
        > notionalUsd     	String  	以美金价值为单位的持仓数量
        '''
        return self.send_request(*_AccountEndpoints.get_account_position_risk, **to_local(locals()))

    # 账单流水查询（近七天）
    def get_bills(self, instType: str = '', ccy: str = '', mgnMode: str = '', ctType: str = '', type: str = '',
                  subType: str = '', after: str = '', before: str = '', begin: str = '', end: str = '', limit: str = '',
                  proxies={}, proxy_host: str = None):
        '''
        帐户资产流水是指导致帐户余额增加或减少的行为。本接口可以查询最近7天的账单数据。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-bills-details-last-7-days
        
        限速：5次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	否       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        ccy               	String  	否       	账单币种
        mgnMode           	String  	否       	仓位类型isolated：逐仓cross：全仓
        ctType            	String  	否       	linear： 正向合约inverse： 反向合约仅交割/永续有效
        type              	String  	否       	账单类型1：划转2：交易3：交割4：自动换币5：强平6：保证金划转7：扣息8：资金费9：自动减仓10：穿仓补偿11：系统换币12：策略划拨13：对冲减仓14: 大宗交易15: 一键借币22: 一键还债24: 价差交易250: 分润支出;251: 分润退还;252: 分润收入;
        subType           	String  	否       	请参看官方文档
        after             	String  	否       	请求此id之前（更旧的数据）的分页内容，传的值为对应接口的billId
        before            	String  	否       	请求此id之后（更新的数据）的分页内容，传的值为对应接口的billId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        billId            	String  	账单ID
        type              	String  	账单类型
        subType           	String  	账单子类型
        ts                	String  	余额更新完成的时间，Unix时间戳的毫秒数格式，如1597026383085
        balChg            	String  	账户层面的余额变动数量
        posBalChg         	String  	仓位层面的余额变动数量
        bal               	String  	账户层面的余额数量
        posBal            	String  	仓位层面的余额数量
        sz                	String  	数量
        px                	String  	价格，与 subType 相关。为成交价格时有 1: 买入 2: 卖出 3：开多 4：开空 5：平多 6：平空 204: 大宗交易买 205: 大宗交易卖 206: 大宗交易开多 207: 大宗交易开空 208: 大宗交易平多 209: 大宗交易平空 114：自动换币买入 115：自动换币卖出强平价格，100：强减平多 101：强减平空 102：强减买入 103：强减卖出 104：强平平多 105：强平平空 106：强平买入 107：强平卖出 16：强制还币 17：强制借币还息 110：强平换币转入 111：强平换币转出交割价格，112：交割平多 113：交割平空行权价格，170：到期行权 171：到期被行权 172：到期作废标记价格，173：资金费支出 174：资金费收入
        ccy               	String  	账户余额币种
        pnl               	String  	收益
        fee               	String  	手续费正数代表平台返佣 ，负数代表平台扣除
        mgnMode           	String  	保证金模式isolated：逐仓cross：全仓账单不是由仓位变化产生的，该字段返回 ""
        instId            	String  	产品ID，如BTC-USD-190927-5000-C
        ordId             	String  	订单ID当type为2：交易时，返回相应订单id。无订单时，该字段返回 ""
        execType          	String  	流动性方向T：takerM：maker
        from              	String  	转出账户6：资金账户18：交易账户仅适用于资金划转，不是资金划转时，返回 ""
        to                	String  	转入账户6：资金账户18：交易账户仅适用于资金划转，不是资金划转时，返回 ""
        notes             	String  	备注
        interest          	String  	利息
        tag               	String  	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        fillTime          	String  	最新成交时间
        tradeId           	String  	最新成交ID
        clOrdId           	String  	客户自定义订单ID
        fillIdxPx         	String  	交易执行时的指数价格对于交叉现货币对，返回 baseCcy-USDT 的指数价格。 例如LTC-ETH，该字段返回LTC-USDT的指数价格。
        fillMarkPx        	String  	成交时的标记价格，仅适用于 交割/永续/期权
        fillPxVol         	String  	成交时的隐含波动率，仅适用于期权，其他业务线返回空字符串""
        fillPxUsd         	String  	成交时的期权价格，以USD为单位，仅适用于期权，其他业务线返回空字符串""
        fillMarkVol       	String  	成交时的标记波动率，仅适用于期权，其他业务线返回空字符串""
        fillFwdPx         	String  	成交时的远期价格，仅适用于期权，其他业务线返回空字符串""
        '''
        return self.send_request(*_AccountEndpoints.get_bills, **to_local(locals()))

    # 账单流水查询（近三月）
    def get_bills_archive(self, instType: str = '', ccy: str = '', mgnMode: str = '', ctType: str = '', type: str = '',
                          subType: str = '', after: str = '', before: str = '', begin: str = '', end: str = '',
                          limit: str = '', proxies={}, proxy_host: str = None):
        '''
        帐户资产流水是指导致帐户余额增加或减少的行为。本接口可以查询最近3个月的账单数据。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-bills-details-last-3-months
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	否       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        ccy               	String  	否       	账单币种
        mgnMode           	String  	否       	仓位类型isolated：逐仓cross：全仓
        ctType            	String  	否       	linear： 正向合约inverse： 反向合约仅交割/永续有效
        type              	String  	否       	账单类型1：划转2：交易3：交割4：自动换币5：强平6：保证金划转7：扣息8：资金费9：自动减仓10：穿仓补偿11：系统换币12：策略划拨13：对冲减仓14: 大宗交易15: 一键借币22: 一键还债24: 价差交易250: 分润支出;251: 分润退还;252: 分润收入;
        subType           	String  	否       	请参考官方文档
        after             	String  	否       	请求此id之前（更旧的数据）的分页内容，传的值为对应接口的billId
        before            	String  	否       	请求此id之后（更新的数据）的分页内容，传的值为对应接口的billId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        billId            	String  	账单ID
        type              	String  	账单类型
        subType           	String  	账单子类型
        ts                	String  	余额更新完成的时间，Unix时间戳的毫秒数格式，如1597026383085
        balChg            	String  	账户层面的余额变动数量
        posBalChg         	String  	仓位层面的余额变动数量
        bal               	String  	账户层面的余额数量
        posBal            	String  	仓位层面的余额数量
        sz                	String  	数量
        px                	String  	价格，与 subType 相关。为成交价格时有 1: 买入 2: 卖出 3：开多 4：开空 5：平多 6：平空 204: 大宗交易买 205: 大宗交易卖 206: 大宗交易开多 207: 大宗交易开空 208: 大宗交易平多 209: 大宗交易平空 114：自动换币买入 115：自动换币卖出强平价格，100：强减平多 101：强减平空 102：强减买入 103：强减卖出 104：强平平多 105：强平平空 106：强平买入 107：强平卖出 16：强制还币 17：强制借币还息 110：强平换币转入 111：强平换币转出交割价格，112：交割平多 113：交割平空行权价格，170：到期行权 171：到期被行权 172：到期作废标记价格，173：资金费支出 174：资金费收入
        ccy               	String  	账户余额币种
        pnl               	String  	收益
        fee               	String  	手续费正数代表平台返佣 ，负数代表平台扣除
        mgnMode           	String  	保证金模式isolated：逐仓cross：全仓无仓位类型字段，该字段返回 ""
        instId            	String  	产品ID，如BTC-USD-190927-5000-C
        ordId             	String  	订单ID当type为2：交易时，返回相应订单id。无订单时，该字段返回 ""
        execType          	String  	流动性方向T：takerM：maker
        from              	String  	转出账户6：资金账户18：交易账户仅适用于资金划转，不是资金划转时，返回 ""
        to                	String  	转入账户6：资金账户18：交易账户仅适用于资金划转，不是资金划转时，返回 ""
        notes             	String  	备注
        interest          	String  	利息
        tag               	String  	订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。
        fillTime          	String  	最新成交时间
        tradeId           	String  	最新成交ID
        clOrdId           	String  	客户自定义订单ID
        fillIdxPx         	String  	交易执行时的指数价格对于交叉现货币对，返回 baseCcy-USDT 的指数价格。 例如LTC-ETH，该字段返回LTC-USDT的指数价格。
        fillMarkPx        	String  	成交时的标记价格，仅适用于 交割/永续/期权
        fillPxVol         	String  	成交时的隐含波动率，仅适用于期权，其他业务线返回空字符串""
        fillPxUsd         	String  	成交时的期权价格，以USD为单位，仅适用于期权，其他业务线返回空字符串""
        fillMarkVol       	String  	成交时的标记波动率，仅适用于期权，其他业务线返回空字符串""
        fillFwdPx         	String  	成交时的远期价格，仅适用于期权，其他业务线返回空字符串""
        '''
        return self.send_request(*_AccountEndpoints.get_bills_archive, **to_local(locals()))

    # 查看账户配置
    def get_config(self, proxies={}, proxy_host: str = None):
        '''
        查看当前账户的配置信息。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-account-configuration
        
        限速：5次/2s
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        uid               	String  	当前请求的账户ID，账户uid和app上的一致
        mainUid           	String  	当前请求的母账户ID如果 uid = mainUid，代表当前账号为母账户；如果 uid != mainUid，代表当前账户为子账户。
        acctLv            	String  	账户层级1：简单交易模式2：单币种保证金模式3：跨币种保证金模式4：组合保证金模式
        posMode           	String  	持仓方式long_short_mode：开平仓模式net_mode：买卖模式仅适用交割/永续
        autoLoan          	Boolean 	是否自动借币true：自动借币false：非自动借币
        greeksType        	String  	当前希腊字母展示方式PA：币本位BS：美元本位
        level             	String  	当前在平台上真实交易量的用户等级，例如lv1
        levelTmp          	String  	特约用户的临时体验用户等级，例如lv3
        ctIsoMode         	String  	衍生品的逐仓保证金划转模式automatic：开仓划转autonomy：自主划转
        mgnIsoMode        	String  	币币杠杆的逐仓保证金划转模式automatic：开仓划转quick_margin：一键借币（对于新的账户，包括新的子账户，有些默认是开仓划转，另外的默认是一键借币）
        spotOffsetType    	String  	现货对冲类型1：现货对冲模式U模式2：现货对冲模式币模式3：非现货对冲模式适用于组合保证金模式
        roleType          	String  	用户角色0：普通用户1：带单者2：跟单者
        traderInsts       	Array   	当前账号已经设置的带单合约，仅适用于带单者
        opAuth            	String  	是否开通期权交易0：未开通1：已经开通
        kycLv             	String  	母账户KYC等级0: 未认证1: 已完成 level 1 认证2: 已完成 level 2 认证3: 已完成 level 3认证如果请求来自子账户, kycLv 为其母账户的等级如果请求来自母账户, kycLv 为当前请求的母账户等级
        label             	String  	当前请求API key的备注名，不超过50位字母（区分大小写）或数字，可以是纯字母或纯数字。
        ip                	String  	当前请求API key绑定的ip地址，多个ip用半角逗号隔开，如：117.37.203.58,117.37.203.57。如果没有绑定ip，会返回空字符串""
        perm              	String  	当前请求的 API key权限read_only：读取trade：交易withdraw：提币
        '''
        return self.send_request(*_AccountEndpoints.get_config, **to_local(locals()))

    # 设置持仓模式
    def set_position_mode(self, posMode: str, proxies={}, proxy_host: str = None):
        '''
        单币种账户和跨币种账户模式：交割和永续合约支持开平仓模式和买卖模式。买卖模式只会有一个方向的仓位；开平仓模式可以分别持有多、空2个方向的仓位。<!- 1-2-3 -->组合保证金模式：交割和永续仅支持买卖模式
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-set-position-mode
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        posMode           	String  	是       	持仓方式long_short_mode：开平仓模式net_mode：买卖模式仅适用交割/永续
        返回参数:
        Parameter         	Type    	Description
        posMode           	String  	持仓方式
        '''
        return self.send_request(*_AccountEndpoints.set_position_mode, **to_local(locals()))

    # 设置杠杆倍数
    def set_leverage(self, lever: str, mgnMode: str, instId: str = '', ccy: str = '', posSide: str = '', proxies={},
                         proxy_host: str = None):
        '''
        一个产品可以有如下10种杠杆倍数的设置场景：
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-set-leverage
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	可选      	产品ID：币对、合约全仓下，instId和ccy至少要传一个；如果两个都传，默认使用instId
        ccy               	String  	可选      	保证金币种仅适用于跨币种保证金模式和组合保证金模式的全仓币币杠杆。设置自动借币的杠杆倍数时必填
        lever             	String  	是       	杠杆倍数
        mgnMode           	String  	是       	保证金模式isolated：逐仓cross：全仓如果ccy有效传值，该参数值只能为cross。
        posSide           	String  	可选      	持仓方向long：开平仓模式开多short：开平仓模式开空仅适用于逐仓交割/永续在开平仓模式且保证金模式为逐仓条件下必填
        返回参数:
        Parameter         	Type    	Description
        lever             	String  	杠杆倍数
        mgnMode           	String  	保证金模式isolated：逐仓cross：全仓
        instId            	String  	产品ID
        posSide           	String  	持仓方向
        '''
        return self.send_request(*_AccountEndpoints.set_leverage, **to_local(locals()))

    # 获取最大可买卖/开仓数量
    def get_max_size(self, instId: str, tdMode: str, ccy: str = '', px: str = '', leverage: str = '',
                     unSpotOffset: bool = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/max-size
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-maximum-buy-sell-amount-or-open-amount
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔
        tdMode            	String  	是       	交易模式cross：全仓isolated：逐仓cash：非保证金
        ccy               	String  	可选      	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        px                	String  	否       	委托价格当不填委托价时会按当前最新成交价计算当指定多个产品ID查询时，忽略该参数，按当前最新成交价计算
        leverage          	String  	否       	开仓杠杆倍数默认为当前杠杆倍数仅适用于币币杠杆/交割/永续
        unSpotOffset      	Boolean 	否       	true：禁止现货对冲，false：允许现货对冲默认为false仅适用于组合保证金模式开启现货对冲模式下有效，否则忽略此参数。
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        ccy               	String  	保证金币种
        maxBuy            	String  	币币/币币杠杆：最大可买的交易币数量单币种保证金模式下的全仓杠杆订单，为交易币数量交割/永续/期权：最大可开多的合约张数
        maxSell           	String  	币币/币币杠杆：最大可卖的计价币数量单币种保证金模式下的全仓杠杆订单，为交易币数量交割/永续/期权：最大可开空的合约张数
        '''
        return self.send_request(*_AccountEndpoints.get_max_size, **to_local(locals()))

    # 获取最大可用数量
    def get_max_avail_size(self, instId: str, tdMode: str, ccy: str = '', reduceOnly: bool = '', px: str = '',
                           unSpotOffset: bool = '', quickMgnType: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/max-avail-size
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-maximum-available-tradable-amount
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔
        tdMode            	String  	是       	交易模式cross：全仓isolated：逐仓cash：非保证金
        ccy               	String  	可选      	保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
        reduceOnly        	Boolean 	否       	是否为只减仓模式，仅适用于币币杠杆
        px                	String  	否       	对应平仓价格下的可用数量，默认为市价。仅适用于杠杆只减仓
        unSpotOffset      	Boolean 	否       	true：禁止现货对冲，false：允许现货对冲默认为false仅适用于组合保证金模式开启现货对冲模式下有效，否则忽略此参数。
        quickMgnType      	String  	否       	一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        availBuy          	String  	最大买入可用数量
        availSell         	String  	最大卖出可用数量
        '''
        return self.send_request(*_AccountEndpoints.get_max_avail_size, **to_local(locals()))

    # 调整保证金
    def set_margin_balance(self, instId: str, posSide: str, type: str, amt: str, ccy: str = '', auto: bool = '',
                           proxies={}, proxy_host: str = None):
        '''
        增加或者减少逐仓保证金。减少保证金可能会导致实际杠杆倍数发生变化。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-increase-decrease-margin
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID
        posSide           	String  	是       	持仓方向，默认值是netlong：开平仓模式开多short：开平仓模式开空net：买卖模式
        type              	String  	是       	增加/减少保证金add：增加，或者转入质押资产(一键借币)reduce：减少，或者转出质押资产（一键借币）
        amt               	String  	是       	增加或减少的保证金数量
        ccy               	String  	否       	增加或减少的保证金的币种，仅适用于逐仓自主划转和一键借币模式下的币币杠杆
        auto              	Boolean 	否       	是否自动借币转 true 或 false，默认false仅适用于逐仓自主划转保证金模式下的币币杠杆
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        posSide           	String  	持仓方向
        amt               	String  	已增加/减少的保证金数量
        type              	String  	增加/减少保证金
        leverage          	String  	调整保证金后的实际杠杆倍数
        ccy               	String  	增加或减少的保证金的币种
        '''
        return self.send_request(*_AccountEndpoints.set_margin_balance, **to_local(locals()))

    # 获取杠杆倍数
    def get_leverage_info(self, instId: str, mgnMode: str, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/leverage-info
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-leverage
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID支持多个instId查询，半角逗号分隔。instId个数不超过20个
        mgnMode           	String  	是       	保证金模式isolated：逐仓cross：全仓
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        mgnMode           	String  	保证金模式
        posSide           	String  	持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式开平仓模式下会返回两个方向的杠杆倍数
        lever             	String  	杠杆倍数
        '''
        return self.send_request(*_AccountEndpoints.get_leverage_info, **to_local(locals()))

    # 获取杠杆倍数预估信息
    def get_adjust_leverage_info(self, instType: str, mgnMode: str, lever: str, instId: str = '', ccy: str = '',
                                 posSide: str = '', proxies={}, proxy_host: str = None):
        '''
        获取指定杠杆倍数下，相关的预估信息。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-leverage-estimated-info
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约
        mgnMode           	String  	是       	保证金模式isolated：逐仓cross：全仓
        lever             	String  	是       	杠杆倍数
        instId            	String  	可选      	产品 ID，如 BTC-USDT必填的场景有：交割永续，逐仓杠杆，以及单币种全仓杠杆。
        ccy               	String  	可选      	保证金币种，如 BTC单币种保证金模式、跨币种保证金模式和组合保证金模式的全仓杠杆时必填。
        posSide           	String  	否       	持仓方向net: 默认值，代表买卖模式long: 开平模式下的多仓short：开平模式下的空仓仅适用交割、永续。
        返回参数:
        Parameter         	Type    	Description
        estAvailQuoteTrans	String  	对应杠杆倍数下，计价货币预估可转出的保证金数量全仓时，为交易账户最大可转出逐仓时，为逐仓仓位可减少的保证金
        estAvailTrans     	String  	对应杠杆倍数下，交易货币的预估可转出的保证金数量全仓时，为交易账户最大可转出逐仓时，为逐仓仓位可减少的保证金
        estLiqPx          	String  	对应杠杆倍数下的预估强平价，仅在有仓位时有值
        estMgn            	String  	对应杠杆倍数下，仓位预估所需的保证金数量对于杠杆仓位，为所需交易货币保证金对于交割或永续仓位，为仓位所需保证金
        estQuoteMgn       	String  	对应杠杆倍数下，仓位预估所需的计价货币保证金数量
        estMaxAmt         	String  	对于杠杆，为对应杠杆倍数下，交易货币预估最大可借对于交割和永续，为对应杠杆倍数下，预估的最大可开张数
        estQuoteMaxAmt    	String  	对应杠杆倍数下，杠杆计价货币预估最大可借
        existOrd          	Boolean 	当前是否存在挂单true：存在挂单false：不存在挂单
        maxLever          	String  	最大杠杆倍数
        minLever          	String  	最小杠杆倍数
        '''
        return self.send_request(*_AccountEndpoints.get_adjust_leverage_info, **to_local(locals()))

    # 获取交易产品最大可借
    def get_max_loan(self, instId: str, mgnMode: str, mgnCcy: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/max-loan
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-the-maximum-loan-of-instrument
        
        限速：20 次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品 ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔
        mgnMode           	String  	是       	仓位类型isolated：逐仓cross：全仓
        mgnCcy            	String  	可选      	保证金币种，如BTC币币杠杆单币种全仓情况下必须指定保证金币种
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品 ID
        mgnMode           	String  	仓位类型
        mgnCcy            	String  	保证金币种
        maxLoan           	String  	最大可借
        ccy               	String  	币种
        side              	String  	订单方向
        '''
        return self.send_request(*_AccountEndpoints.get_max_loan, **to_local(locals()))

    # 获取当前账户交易手续费费率
    def get_trade_fee(self, instType: str, instId: str = '', uly: str = '', instFamily: str = '', proxies={},
                      proxy_host: str = None):
        '''
        GET /api/v5/account/trade-fee
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-fee-rates
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
        instId            	String  	否       	产品ID，如BTC-USDT仅适用于instType为币币/币币杠杆
        uly               	String  	否       	标的指数适用于交割/永续/期权，如BTC-USD
        instFamily        	String  	否       	交易品种适用于交割/永续/期权，如BTC-USD
        返回参数:
        Parameter         	Type    	Description
        level             	String  	手续费等级
        taker             	String  	对于币币/杠杆，为 USDT&USDⓈ&Crypto 交易区的吃单手续费率；对于永续，交割和期权合约，为币本位合约费率
        maker             	String  	对于币币/杠杆，为 USDT&USDⓈ&Crypto 交易区的挂单手续费率；对于永续，交割和期权合约，为币本位合约费率
        takerU            	String  	USDT 合约吃单手续费率，仅适用于交割/永续
        makerU            	String  	USDT 合约挂单手续费率，仅适用于交割/永续
        delivery          	String  	交割手续费率
        exercise          	String  	行权手续费率
        instType          	String  	产品类型
        takerUSDC         	String  	USDC 交易区的吃单手续费率，包括 USDC 现货和 USDC 合约
        makerUSDC         	String  	USDC 交易区的挂单手续费率，包括 USDC 现货和 USDC 合约
        ts                	String  	数据返回时间，Unix时间戳的毫秒数格式，如1597026383085
        category          	String  	币种类别（已废弃）
        '''
        return self.send_request(*_AccountEndpoints.get_trade_fee, **to_local(locals()))

    # 获取计息记录
    def get_interest_accrued(self, type: str = '', ccy: str = '', instId: str = '', mgnMode: str = '', after: str = '',
                             before: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/interest-accrued
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-interest-accrued-data
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        type              	String  	否       	借币类型1：尊享借币2：市场借币默认为市场借币
        ccy               	String  	否       	借贷币种，如BTC仅适用于市场借币仅适用于币币杠杆
        instId            	String  	否       	产品ID，如BTC-USDT仅适用于市场借币
        mgnMode           	String  	否       	保证金模式cross：全仓isolated：逐仓仅适用于市场借币
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        type              	String  	类型1：尊享借币2：市场借币
        ccy               	String  	借贷币种，如BTC
        instId            	String  	产品ID，如BTC-USD-180216仅适用于市场借币
        mgnMode           	String  	保证金模式cross：全仓isolated：逐仓
        interest          	String  	利息
        interestRate      	String  	计息利率(小时)
        liab              	String  	计息负债
        ts                	String  	计息时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_AccountEndpoints.get_interest_accrued, **to_local(locals()))

    # 获取用户当前市场借币利率
    def get_interest_rate(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/interest-rate
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-interest-rate
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种
        返回参数:
        Parameter         	Type    	Description
        interestRate      	String  	市场借币利率(当前小时)
        ccy               	String  	币种
        '''
        return self.send_request(*_AccountEndpoints.get_interest_rate, **to_local(locals()))

    # 期权greeks的PA/BS切换
    def set_greeks(self, greeksType: str, proxies={}, proxy_host: str = None):
        '''
        设置greeks的展示方式。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-set-greeks-pa-bs
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        greeksType        	String  	是       	希腊字母展示方式PA：币本位，BS：美元本位
        返回参数:
        Parameter         	Type    	Description
        greeksType        	String  	当前希腊字母展示方式
        '''
        return self.send_request(*_AccountEndpoints.set_greeks, **to_local(locals()))

    # 逐仓交易设置
    def set_isolated_mode(self, isoMode: str, type: str, proxies={}, proxy_host: str = None):
        '''
        可以通过该接口设置币币杠杆和交割、永续的逐仓仓位保证金的划转模式
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-isolated-margin-trading-settings
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        isoMode           	String  	是       	逐仓保证金划转模式automatic:开仓自动划转autonomy:自主划转 (仅适用在合约)quick_margin:一键借币 (仅适用在币币杠杆)
        type              	String  	是       	业务线类型MARGIN:币币杠杆CONTRACTS:合约
        返回参数:
        Parameter         	Type    	Description
        isoMode           	String  	逐仓保证金划转模式automatic:开仓自动划转autonomy:自主划转quick_margin:一键借币
        '''
        return self.send_request(*_AccountEndpoints.set_isolated_mode, **to_local(locals()))

    # 查看账户最大可转余额
    def get_max_withdrawal(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        当指定币种时会返回该币种的交易账户到资金账户的最大可划转数量，不指定币种会返回所有拥有的币种资产可划转数量。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-maximum-withdrawals
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种
        maxWd             	String  	最大可划转数量（不包含跨币种保证金模式/组合保证金模式借币金额）
        maxWdEx           	String  	最大可划转数量（包含跨币种保证金模式/组合保证金模式借币金额）
        spotOffsetMaxWd   	String  	现货对冲不支持借币最大可转数量仅适用于组合保证金模式
        spotOffsetMaxWdEx 	String  	现货对冲支持借币的最大可转数量仅适用于组合保证金模式
        '''
        return self.send_request(*_AccountEndpoints.get_max_withdrawal, **to_local(locals()))

    # 查看账户特定风险状态
    def get_risk_state(self, proxies={}, proxy_host: str = None):
        '''
        仅适用于PM账户
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-account-risk-state
        
        限速：10次/2s
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        atRisk            	String  	自动借币模式下的账户风险状态true： 当前账户为特定风险状态false： 当前不是特定风险状态
        atRiskIdx         	Array   	衍生品的risk unit列表
        atRiskMgn         	Array   	杠杆的risk unit列表
        ts                	String  	接口数据返回时间 ，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_AccountEndpoints.get_risk_state, **to_local(locals()))

    # 一键借币模式手动借币还币
    def set_quick_margin_borrow_repay(self, instId: str, ccy: str, side: str, amt: str, proxies={},
                                      proxy_host: str = None):
        '''
        POST /api/v5/account/quick-margin-borrow-repay
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-manual-borrow-and-repay-in-quick-margin-mode
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT
        ccy               	String  	是       	借贷币种，如BTC
        side              	String  	是       	borrow：借币，repay：还币
        amt               	String  	是       	借/还币的数量
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID，如BTC-USDT
        ccy               	String  	借贷币种，如BTC
        side              	String  	borrow：借币，repay：还币
        amt               	String  	借/还币的数量
        '''
        return self.send_request(*_AccountEndpoints.set_quick_margin_borrow_repay, **to_local(locals()))

    # 获取一键借币还币历史
    def get_quick_margin_borrow_repay_history(self, instId: str = '', ccy: str = '', side: str = '', after: str = '',
                                              before: str = '', begin: str = '', end: str = '', limit: str = '',
                                              proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/quick-margin-borrow-repay-history
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-borrow-and-repay-history-in-quick-margin-mode
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	否       	产品ID，如 BTC-USDT
        ccy               	String  	否       	借贷币种，如BTC
        side              	String  	否       	borrow：借币，repay：还币
        after             	String  	否       	请求此 ID 之前（更旧的数据）的分页内容，传的值为对应接口的refId
        before            	String  	否       	请求此 ID 之后（更新的数据）的分页内容，传的值为对应接口的refId
        begin             	String  	否       	筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085
        end               	String  	否       	筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID，如 BTC-USDT
        ccy               	String  	借贷币种，如BTC
        side              	String  	borrow：借币，repay：还币
        accBorrowed       	String  	累计借币
        amt               	String  	借/还币的数量
        refId             	String  	对应记录ID，借币或还币的ID
        ts                	String  	借/还币时间
        '''
        return self.send_request(*_AccountEndpoints.get_quick_margin_borrow_repay_history, **to_local(locals()))

    # 尊享借币还币
    def set_borrow_repay(self, ccy: str, side: str, amt: str, ordId: str = '', proxies={}, proxy_host: str = None):
        '''
        单个币种的借币订单数量最多为20个
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-vip-loans-borrow-and-repay
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	借贷币种，如BTC
        side              	String  	是       	borrow：借币，repay：还币
        amt               	String  	是       	借/还币的数量
        ordId             	String  	可选      	借币订单ID，还币时，该字段必填
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	借贷币种，如BTC
        side              	String  	borrow：借币，repay：还币
        amt               	String  	已借/还币的数量
        ordId             	String  	借币订单ID
        state             	String  	订单状态1:借币申请中2:借币中3:还币申请中4:已还币5:借币失败
        '''
        return self.send_request(*_AccountEndpoints.set_borrow_repay, **to_local(locals()))

    # 获取尊享借币还币历史
    def get_borrow_repay_history(self, ccy: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                                 proxy_host: str = None):
        '''
        GET /api/v5/account/borrow-repay-history
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-borrow-and-repay-history-for-vip-loans
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	借贷币种，如BTC
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	借贷币种，如BTC
        type              	String  	类型1：借币2：还币3：扣息失败系统还币
        tradedLoan        	String  	借/还币数量
        usedLoan          	String  	当前账户已借额度
        ts                	String  	借/还币时间
        '''
        return self.send_request(*_AccountEndpoints.get_borrow_repay_history, **to_local(locals()))

    # 获取尊享借币计息记录
    def get_vip_interest_accrued(self, ccy: str = '', ordId: str = '', after: str = '', before: str = '',
                                 limit: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/vip-interest-accrued
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-vip-interest-accrued-data
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	借贷币种，如BTC，仅适用于币币杠杆
        ordId             	String  	否       	借币订单ID
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ordId             	String  	借币订单ID
        ccy               	String  	借贷币种，如BTC
        interest          	String  	利息
        interestRate      	String  	计息利率(小时)
        liab              	String  	计息负债
        ts                	String  	计息时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_AccountEndpoints.get_vip_interest_accrued, **to_local(locals()))

    # 获取尊享借币扣息记录
    def get_vip_interest_deducted(self, ordId: str = '', ccy: str = '', after: str = '', before: str = '',
                                  limit: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/vip-interest-deducted
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-vip-interest-deducted-data
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ordId             	String  	否       	借币订单ID
        ccy               	String  	否       	借贷币种，如BTC，仅适用于币币杠杆
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ordId             	String  	借币订单ID
        ccy               	String  	借贷币种，如BTC
        interest          	String  	利息
        interestRate      	String  	计息利率(小时)
        liab              	String  	计息负债
        ts                	String  	计息时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_AccountEndpoints.get_vip_interest_deducted, **to_local(locals()))

    # 尊享借币订单列表
    def get_vip_loan_order_list(self, ordId: str = '', state: str = '', ccy: str = '', after: str = '',
                                before: str = '', limit: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/vip-loan-order-list
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-vip-loan-order-list
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ordId             	String  	否       	借币订单ID
        state             	String  	否       	订单状态1:借币申请中2:借币中3:还币申请中4:已还币5:借币失败
        ccy               	String  	否       	借贷币种，如 BTC
        after             	String  	否       	请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	订单创建时间，Unix时间戳的毫秒数格式，如1597026383085
        nextRefreshTime   	String  	下一次理论刷新时间，Unix时间戳的毫秒数格式，如1597026383085
        ccy               	String  	借贷币种，如 BTC
        ordId             	String  	订单ID
        state             	String  	订单状态1:借币申请中2:借币中3:还币申请中4:已还币5:业务异常，借币失败
        origRate          	String  	订单原始利率
        curRate           	String  	借贷币种当前利率
        dueAmt            	String  	待还数量
        borrowAmt         	String  	借币数量
        repayAmt          	String  	还币数量
        '''
        return self.send_request(*_AccountEndpoints.get_vip_loan_order_list, **to_local(locals()))

    # 尊享借币订单详情
    def get_vip_loan_order_detail(self, ordId: str, ccy: str = '', before: str = '', after: str = '', limit: str = '',
                                  proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/vip-loan-order-detail
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-vip-loan-order-detail
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ordId             	String  	是       	借币订单ID
        ccy               	String  	否       	借贷币种，如 BTC
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	返回结果的数量，最大为100，默认100条
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	操作时间
        ccy               	String  	借贷币种，如BTC
        type              	String  	操作类型1:借币2:还币3:系统还币4:利率刷新
        rate              	String  	订单当前利率（日利率）
        amt               	String  	借还数量
        failReason        	String  	失败原因
        '''
        return self.send_request(*_AccountEndpoints.get_vip_loan_order_detail, **to_local(locals()))

    # 获取借币利率与限额
    def get_interest_limits(self, type: str = '', ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/account/interest-limits
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-borrow-interest-and-limit
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        type              	String  	否       	借币类型1：尊享借币2：市场借币默认为市场借币
        ccy               	String  	否       	借贷币种，如BTC
        返回参数:
        Parameter         	Type    	Description
        debt              	String  	当前负债，单位为USDT
        interest          	String  	当前记息，单位为USDT仅适用于市场借币
        nextDiscountTime  	String  	下次扣息时间，Unix时间戳的毫秒数格式，如1597026383085
        nextInterestTime  	String  	下次计息时间，Unix时间戳的毫秒数格式，如1597026383085
        loanAlloc         	String  	当前交易账户尊享借币可用额度的比率（百分比）1. 范围为[0, 100]. 精度为 0.01% (2位小数)2. 0 代表母账户没有为子账户分配；3. "" 代表母子账户共享
        records           	Array   	各币种详细信息
        > ccy             	String  	借贷币种，如BTC
        > rate            	String  	日利率
        > loanQuota       	String  	母账户维度借币限额如果已配置可用额度，该字段代表当前交易账户的借币限额
        > surplusLmt      	String  	母子账户剩余可借如果已配置可用额度，该字段代表当前交易账户的剩余可借
        > surplusLmtDetails	Array   	母子账户剩余可借额度详情，母子账户剩余可借额度的值取该数组中的最小值，可以用来判断是什么原因导致可借额度不足仅适用于尊享借币
        >> allAcctRemainingQuota	String  	母子账户剩余额度
        >> curAcctRemainingQuota	String  	当前账户剩余额度仅适用于为子账户分配限额的场景
        >> platRemainingQuota	String  	平台剩余额度，当平台剩余额度大于curAcctRemainingQuota或者allAcctRemainingQuota时，会显示大于某个值，如">1000"
        > usedLmt         	String  	母子账户已借额度如果已配置可用额度，该字段代表当前交易账户的已借额度
        > interest        	String  	已计未扣利息仅适用于市场借币
        > posLoan         	String  	当前账户负债占用（锁定额度内）仅适用于尊享借币
        > availLoan       	String  	当前账户剩余可用（锁定额度内）仅适用于尊享借币
        > usedLoan        	String  	当前账户已借额度仅适用于尊享借币
        > avgRate         	String  	币种已借平均(小时)利率，仅适用于尊享借币
        '''
        return self.send_request(*_AccountEndpoints.get_interest_limits, **to_local(locals()))

    # 组合保证金的虚拟持仓保证金计算
    def set_simulated_margin(self, instType: str = '', inclRealPos: bool = '', spotOffsetType: str = '',
                             simPos: list = [], proxies={}, proxy_host: str = None):
        '''
        计算用户的模拟头寸或当前头寸的投资组合保证金信息，一次请求最多添加200个虚拟仓位
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-position-builder
        
        限速：2次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	否       	产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权
        inclRealPos       	Boolean 	否       	是否代入已有仓位true：调整被代入的已有仓位信息false：不代入已有仓位，仅使用simPos里新增的模拟仓位进行计算,默认为True
        spotOffsetType    	String  	否       	现货对冲模式1：现货对冲模式U模式 2：现货对冲模式币模式 3：衍生品模式默认是 3
        simPos            	Array   	否       	模拟仓位列表
        > instId          	String  	否       	交易产品ID
        > pos             	String  	否       	持仓量
        返回参数:
        Parameter         	Type    	Description
        riskUnit          	String  	账户内所有持仓的riskUnit
        ts                	String  	账户信息的更新时间，Unix时间戳的毫秒数格式，如1597026383085
        mmr               	String  	riskUnit维度的维持保证金
        imr               	String  	riskUnit维度的最低初始保证金
        acctImr           	String  	账户维度的最低初始保证金
        acctMmr           	String  	账户维度的维持保证金
        mr1               	String  	现货&波动率压力测试值
        mr2               	String  	时间价值压力测试值
        mr3               	String  	波动率跨期压力测试值
        mr4               	String  	基差压力测试值
        mr5               	String  	利率风险压力测试值
        mr6               	String  	极端市场波动压力测试值
        mr7               	String  	减仓成本压力测试值
        posData           	Array   	持仓列表
        > instId          	String  	产品ID，如BTC-USD-180216
        > instType        	String  	产品类型
        > pos             	String  	持仓量
        > notionalUsd     	String  	以美金价值为单位的持仓数量
        > delta           	String  	期权价格对uly价格的敏感度
        > gamma           	String  	delta对uly价格的敏感度
        > vega            	String  	期权价格对隐含波动率的敏感度
        > theta           	String  	期权价格对剩余期限的敏感度
        '''
        return self.send_request(*_AccountEndpoints.set_simulated_margin, **to_local(locals()))

    # 查看账户Greeks
    def get_greeks(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        获取账户资产的greeks信息。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-greeks
        
        限速：10次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC
        返回参数:
        Parameter         	Type    	Description
        deltaBS           	String  	美金本位账户资产delta
        deltaPA           	String  	币本位账户资产delta
        gammaBS           	String  	美金本位账户资产gamma，仅适用于期权
        gammaPA           	String  	币本位账户资产gamma，仅适用于期权
        thetaBS           	String  	美金本位账户资产theta，仅适用于期权
        thetaPA           	String  	币本位账户资产theta，仅适用于期权
        vegaBS            	String  	美金本位账户资产vega，仅适用于期权
        vegaPA            	String  	币本位账户资产vega，仅适用于期权
        ccy               	String  	币种
        ts                	String  	获取greeks的时间，Unix时间戳的毫秒数格式，如 1597026383085
        '''
        return self.send_request(*_AccountEndpoints.get_greeks, **to_local(locals()))

    # 获取组合保证金模式仓位限制
    def get_position_tiers(self, instType: str, uly: str = '', instFamily: str = '', proxies={},
                           proxy_host: str = None):
        '''
        仅支持获取组合保证金模式下，交割、永续和期权的全仓仓位限制。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-pm-position-limitation
        
        限速：10次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	可选      	标的指数，如BTC-USDT，支持多个查询（不超过3个），uly之间半角逗号分隔适用于交割/永续/期权uly与instFamily必须传一个,若传两个，以instFamily为主
        instFamily        	String  	可选      	交易品种，如BTC-USDT，支持多个查询（不超过5个），instFamily之间半角逗号分隔适用于交割/永续/期权uly与instFamily必须传一个,若传两个，以instFamily为主
        返回参数:
        Parameter         	Type    	Description
        uly               	String  	标的指数适用于交割/永续/期权
        instFamily        	String  	交易品种适用于交割/永续/期权
        maxSz             	String  	最大持仓量
        posType           	String  	限仓类型，仅适用于组合保证金模式下的期权全仓。1：所有合约挂单 + 持仓张数，2：所有合约总挂单张数，3：所有合约总挂单单数，4：同方向合约挂单 + 持仓张数，5：单一合约总挂单单数，6：单一合约挂单 + 持仓张数，7：单笔挂单张数"
        '''
        return self.send_request(*_AccountEndpoints.get_position_tiers, **to_local(locals()))

    # 设置组合保证金账户风险对冲模式
    def set_riskOffset_type(self, type: str, proxies={}, proxy_host: str = None):
        '''
        设置 Portfolio Margin 账户风险对冲模式
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-set-risk-offset-type
        
        限速：10次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        type              	String  	是       	风险对冲模式1：现货对冲(USDT)2:现货对冲(币)3:衍生品对冲
        返回参数:
        Parameter         	Type    	Description
        type              	String  	风险对冲模式1：现货对冲(USDT)2:现货对冲(币)3:衍生品对冲
        '''
        return self.send_request(*_AccountEndpoints.set_riskOffset_type, **to_local(locals()))

    # 开通期权交易
    def set_activate_option(self, proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/account/activate-option
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-activate-option
        
        限速：5次/2s
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	开通时间
        '''
        return self.send_request(*_AccountEndpoints.set_activate_option, **to_local(locals()))

    # 设置自动借币
    def set_auto_loan(self, autoLoan: bool = '', proxies={}, proxy_host: str = None):
        '''
        仅适用于跨币种保证金模式和组合保证金模式
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-set-auto-loan
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        autoLoan          	Boolean 	否       	是否自动借币有效值为true,false默认为true
        返回参数:
        Parameter         	Type    	Description
        autoLoan          	Boolean 	是否自动借币
        '''
        return self.send_request(*_AccountEndpoints.set_auto_loan, **to_local(locals()))

    # 设置账户模式
    def set_account_level(self, acctLv: str, proxies={}, proxy_host: str = None):
        '''
        账户模式的首次设置，需要在网页或手机app上进行。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-set-account-mode
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        acctLv            	String  	是       	账户模式1: 简单交易模式2: 单币种保证金模式3: 跨币种保证金模式4: 组合保证金模式
        返回参数:
        Parameter         	Type    	Description
        acctLv            	String  	账户模式
        '''
        return self.send_request(*_AccountEndpoints.set_account_level, **to_local(locals()))

    # 重置 MMP 状态
    def set_mmp_reset(self, instFamily: str, instType: str = '', proxies={}, proxy_host: str = None):
        '''
        一旦 MMP 被触发，可以使用该接口解冻。<!- 1-2-3 -->仅适用于组合保证金账户模式下的期权订单，且有 MMP 权限。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-reset-mmp-status
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	否       	交易产品类型OPTION:期权默认为期权
        instFamily        	String  	是       	交易品种
        返回参数:
        Parameter         	Type    	Description
        result            	Boolean 	重置结果true:将做市商保护状态重置为了 inactive 状态false：重置失败
        '''
        return self.send_request(*_AccountEndpoints.set_mmp_reset, **to_local(locals()))

    # 设置 MMP
    def set_mmp_config(self, instFamily: str, timeInterval: str, frozenInterval: str, qtyLimit: str, proxies={},
                       proxy_host: str = None):
        '''
        可以使用该接口进行 MMP 的配置。<!- 1-2-3 -->仅适用于组合保证金账户模式下的期权订单，且有 MMP 权限。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-set-mmp
        
        限速：2次/10s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instFamily        	String  	是       	交易品种
        timeInterval      	String  	是       	时间窗口 (毫秒)。"0" 代表不使用 MMP
        frozenInterval    	String  	是       	冻结时间长度 (毫秒)。"0" 代表一直冻结，直到调用 "重置 MMP 状态" 接口解冻
        qtyLimit          	String  	是       	成交数量的上限需大于 0
        返回参数:
        Parameter         	Type    	Description
        instFamily        	String  	交易品种
        timeInterval      	String  	时间窗口 (毫秒)
        frozenInterval    	String  	冻结时间长度 (毫秒)
        qtyLimit          	String  	成交张数的上限
        '''
        return self.send_request(*_AccountEndpoints.set_mmp_config, **to_local(locals()))

    # 查看 MMP 配置
    def get_mmp_config(self, instFamily: str = '', proxies={}, proxy_host: str = None):
        '''
        可以使用该接口获取 MMP 的配置信息。<!- 1-2-3 -->仅适用于组合保证金账户模式下的期权订单，且有 MMP 权限。
        https://www.okx.com/docs-v5/zh/#trading-account-rest-api-get-mmp-config
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        instFamily        	String  	否       	交易品种
        返回参数:
        Parameter         	Type    	Description
        instFamily        	String  	交易品种
        mmpFrozen         	Boolean 	是否 MMP 被触发.true或者false
        mmpFrozenUntil    	String  	如果配置了frozenInterval且mmpFrozen = true，则为不再触发MMP时的时间戳（单位为ms），否则为“”
        timeInterval      	String  	时间窗口 (毫秒)。"0" 代表不使用 MMP
        frozenInterval    	String  	冻结时间长度 (毫秒)。"0" 代表一直冻结，直到调用 "重置 MMP 状态" 接口解冻
        qtyLimit          	String  	成交张数的上限
        '''
        return self.send_request(*_AccountEndpoints.get_mmp_config, **to_local(locals()))

'''
子账户
https://www.okx.com/docs-v5/zh/#sub-account-rest-api
'''
from paux.param import to_local
from okx.api._client import Client


class _SubAccountEndpoints():
    get_list = ['/api/v5/users/subaccount/list', 'GET']  # 查看子账户列表
    set_modify_apikey = ['/api/v5/users/subaccount/modify-apikey', 'POST']  # 重置子账户的APIKey
    get_account_balances = ['/api/v5/account/subaccount/balances', 'GET']  # 获取子账户交易账户余额
    get_assert_balances = ['/api/v5/asset/subaccount/balances', 'GET']  # 获取子账户资金账户余额
    get_max_withdrawal = ['/api/v5/account/subaccount/max-withdrawal', 'GET']  # 获取子账户最大可转余额
    get_bills = ['/api/v5/asset/subaccount/bills', 'GET']  # 查询子账户转账记录
    get_managed_subaccount_bills = ['/api/v5/asset/subaccount/managed-subaccount-bills', 'GET']  # 查询托管子账户转账记录
    set_transfer = ['/api/v5/asset/subaccount/transfer', 'POST']  # 子账户间资金划转
    set_transfer_out = ['/api/v5/users/subaccount/set-transfer-out', 'POST']  # 设置子账户主动转出权限
    get_entrust_subaccount_list = ['/api/v5/users/entrust-subaccount-list', 'GET']  # 查看被托管的子账户列表
    get_if_rebate = ['/api/v5/users/partner/if-rebate', 'GET']  # 获取用户的节点返佣信息
    set_loan_allocation = ['/api/v5/account/subaccount/set-loan-allocation', 'POST']  # 设置子账户尊享借币比率
    get_interest_limits = ['/api/v5/account/subaccount/interest-limits', 'GET']  # 获取子账户借币利率与限额


class SubAccount(Client):

    # 查看子账户列表
    def get_list(self, enable: str = '', subAcct: str = '', after: str = '', before: str = '', limit: str = '',
                 proxies={}, proxy_host: str = None):
        '''
        仅适用于母账户
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-get-sub-account-list
        
        限速：2次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        enable            	String  	否       	子账户状态true: 正常使用false: 冻结
        subAcct           	String  	否       	子账户名称
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        type              	String  	子账户类型1: 普通子账户2: 资管子账户5: 托管子账户 - Copper
        enable            	Boolean 	子账户状态true: 正常使用false: 冻结
        subAcct           	String  	子账户名称
        uid               	String  	子账户UID
        label             	String  	子账户备注
        mobile            	String  	子账户绑定手机号
        gAuth             	Boolean 	子账户是否开启的登录时的谷歌验证true: 已开启false: 未开启
        canTransOut       	Boolean 	是否可以主动转出true: 可以转出false: 不可转出
        ts                	String  	子账户创建时间，Unix时间戳的毫秒数格式 ，如1597026383085
        '''
        return self.send_request(*_SubAccountEndpoints.get_list, **to_local(locals()))

    # 重置子账户的APIKey
    def set_modify_apikey(self, subAcct: str, apiKey: str, label: str = '', perm: str = '', ip: str = '', proxies={},
                          proxy_host: str = None):
        '''
        仅适用于母账户,且母账户APIKey必须绑定IP
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-reset-the-api-key-of-a-sub-account
        
        限速：1次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        subAcct           	String  	是       	子账户名称
        apiKey            	String  	是       	子账户API的公钥
        label             	String  	否       	子账户APIKey的备注，如果填写该字段，则该字段会被重置
        perm              	String  	否       	子账户APIKey权限read_only：读取trade：交易多个权限用半角逗号隔开。如果填写该字段，则该字段会被重置。
        ip                	String  	否       	子账户APIKey绑定ip地址，多个ip用半角逗号隔开，最多支持20个ip。如果填写该字段，那该字段会被重置。如果ip传""，则表示解除IP绑定。
        返回参数:
        Parameter         	Type    	Description
        subAcct           	String  	子账户名称
        label             	String  	APIKey的备注
        apiKey            	String  	API公钥
        perm              	String  	APIKey权限
        ip                	String  	APIKey绑定的ip地址
        ts                	String  	创建时间
        '''
        return self.send_request(*_SubAccountEndpoints.set_modify_apikey, **to_local(locals()))

    # 获取子账户交易账户余额
    def get_account_balances(self, subAcct: str, proxies={}, proxy_host: str = None):
        '''
        获取子账户交易账户余额（适用于母账户）
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-get-sub-account-trading-balance
        
        限速：6次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        subAcct           	String  	是       	子账户名称
        返回参数:
        Parameter         	Type    	Description
        uTime             	String  	获取账户信息的最新时间，Unix时间戳的毫秒数格式，如1597026383085
        totalEq           	String  	美金层面权益
        isoEq             	String  	美金层面逐仓仓位权益适用于单币种保证金模式和跨币种保证金模式和组合保证金模式
        adjEq             	String  	美金层面有效保证金适用于跨币种保证金模式和组合保证金模式
        ordFroz           	String  	美金层面全仓挂单占用保证金适用于跨币种保证金模式和组合保证金模式
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
        > isoEq           	String  	币种逐仓仓位权益适用于单币种保证金模式和跨币种保证金模式
        > availEq         	String  	可用保证金适用于单币种保证金模式和跨币种保证金模式
        > disEq           	String  	美金层面币种折算权益
        > availBal        	String  	可用余额适用于简单交易模式
        > frozenBal       	String  	币种占用金额
        > ordFrozen       	String  	挂单冻结数量
        > liab            	String  	币种负债额适用于跨币种保证金模式和组合保证金模式
        > upl             	String  	未实现盈亏适用于单币种保证金模式和跨币种保证金模式和组合保证金模式
        > uplLiab         	String  	由于仓位未实现亏损导致的负债适用于跨币种保证金模式和组合保证金模式
        > crossLiab       	String  	币种全仓负债额适用于跨币种保证金模式和组合保证金模式
        > isoLiab         	String  	币种逐仓负债额适用于跨币种保证金模式和组合保证金模式
        > mgnRatio        	String  	保证金率适用于单币种保证金模式
        > interest        	String  	计息适用于跨币种保证金模式和组合保证金模式
        > twap            	String  	当前负债币种触发系统自动换币的风险0、1、2、3、4、5其中之一，数字越大代表您的负债币种触发自动换币概率越高适用于跨币种保证金模式和组合保证金模式
        > maxLoan         	String  	币种最大可借适用于跨币种保证金模式和组合保证金模式的全仓
        > eqUsd           	String  	币种权益美金价值
        > borrowFroz      	String  	币种美金层面潜在借币占用保证金仅适用于跨币种保证金模式和组合保证金模式. 在其他账户模式下为"".
        > notionalLever   	String  	币种杠杆倍数适用于单币种保证金模式
        '''
        return self.send_request(*_SubAccountEndpoints.get_account_balances, **to_local(locals()))

    # 获取子账户资金账户余额
    def get_assert_balances(self, subAcct: str, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        获取子账户资金账户余额（适用于母账户）
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-get-sub-account-funding-balance
        
        限速：6次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        subAcct           	String  	是       	子账户名称
        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种，如BTC
        bal               	String  	余额
        frozenBal         	String  	冻结（不可用）
        availBal          	String  	可用余额
        '''
        return self.send_request(*_SubAccountEndpoints.get_assert_balances, **to_local(locals()))

    # 获取子账户最大可转余额
    def get_max_withdrawal(self, subAcct: str, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        获取子账户最大可转余额（适用于母账户）。不指定币种会返回所有拥有的币种资产可划转数量。
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-get-sub-account-maximum-withdrawals
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        subAcct           	String  	是       	子账户名称
        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种
        maxWd             	String  	最大可划转数量（不包含跨币种保证金模式借币金额）
        maxWdEx           	String  	最大可划转数量（包含跨币种保证金模式借币金额）
        spotOffsetMaxWd   	String  	现货对冲不支持借币最大可转数量仅适用于组合保证金模式
        spotOffsetMaxWdEx 	String  	现货对冲支持借币的最大可转数量仅适用于组合保证金模式
        '''
        return self.send_request(*_SubAccountEndpoints.get_max_withdrawal, **to_local(locals()))

    # 查询子账户转账记录
    def get_bills(self, ccy: str = '', type: str = '', subAcct: str = '', after: str = '', before: str = '',
                  limit: str = '', proxies={}, proxy_host: str = None):
        '''
        仅适用于母账户
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-get-history-of-sub-account-transfer
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如 BTC
        type              	String  	否       	划转类型0：母账户转子账户1：子账户转母账户
        subAcct           	String  	否       	子账户名称
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳的毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳的毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        billId            	String  	账单ID
        ccy               	String  	账户余额币种
        amt               	String  	划转金额
        type              	String  	账单类型
        subAcct           	String  	子账户名称
        ts                	String  	账单ID创建时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_SubAccountEndpoints.get_bills, **to_local(locals()))

    # 查询托管子账户转账记录
    def get_managed_subaccount_bills(self, ccy: str = '', type: str = '', subAcct: str = '', subUid: str = '',
                                     after: str = '', before: str = '', limit: str = '', proxies={},
                                     proxy_host: str = None):
        '''
        仅适用于交易团队母账户查看托管给自己的托管子账户转账记录
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-get-history-of-managed-sub-account-transfer
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC
        type              	String  	否       	划转类型0：母账户转子账户1：子账户转母账户
        subAcct           	String  	否       	子账户名称
        subUid            	String  	否       	子账户UID
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，默认返回100条
        返回参数:
        Parameter         	Type    	Description
        billId            	String  	账单ID
        ccy               	String  	账户余额币种
        amt               	String  	划转金额
        type              	String  	账单类型
        subAcct           	String  	子账户名称
        subUid            	String  	子账户UID
        ts                	String  	账单ID创建时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_SubAccountEndpoints.get_managed_subaccount_bills, **to_local(locals()))

    # 子账户间资金划转
    def set_transfer(self, ccy: str, amt: str, from_: str, to: str, fromSubAccount: str, toSubAccount: str,
                     loanTrans: bool = '', omitPosRisk: str = '', proxies={}, proxy_host: str = None):
        '''
        母账户控制子账户与子账户之间划转（仅适用于母账户）
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-master-accounts-manage-the-transfers-between-sub-accounts
        
        限速：1次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种
        amt               	String  	是       	划转数量
        from              	String  	是       	转出子账户类型6：资金账户18：交易账户
        to                	String  	是       	转出子账户类型6：资金账户18：交易账户
        fromSubAccount    	String  	是       	转出子账户的子账户名称
        toSubAccount      	String  	是       	转入子账户的子账户名称
        loanTrans         	Boolean 	否       	是否支持跨币种保证金模式或组合保证金模式下的借币转入/转出true 或 false，默认false
        omitPosRisk       	String  	否       	是否忽略仓位风险默认为false仅适用于组合保证金模式
        返回参数:
        Parameter         	Type    	Description
        transId           	String  	划转ID
        '''
        data = to_local(locals())
        data['from'] = data['from_']
        del data['from_']
        return self.send_request(*_SubAccountEndpoints.set_transfer, **data)

    # 设置子账户主动转出权限
    def set_transfer_out(self, subAcct: str, canTransOut: bool = '', proxies={}, proxy_host: str = None):
        '''
        设置子账户转出权限（仅适用于母账户），默认可转出至母账户。
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-set-permission-of-transfer-out
        
        限速：1次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        subAcct           	String  	是       	子账户名称，支持设置多个（不超过20个），子账户名称之间半角逗号分隔
        canTransOut       	Boolean 	否       	是否可以主动转出，默认为truefalse：不可转出true：可以转出
        返回参数:
        Parameter         	Type    	Description
        subAcct           	String  	子账户名称
        canTransOut       	Boolean 	是否可以主动转出false：不可转出true：可以转出
        '''
        return self.send_request(*_SubAccountEndpoints.set_transfer_out, **to_local(locals()))

    # 查看被托管的子账户列表
    def get_entrust_subaccount_list(self, subAcct: str = '', proxies={}, proxy_host: str = None):
        '''
        交易团队使用该接口查看当前托管中的子账户列表
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-get-custody-trading-sub-account-list
        
        限速：1次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        subAcct           	String  	否       	子账户名称
        返回参数:
        Parameter         	Type    	Description
        subAcct           	String  	子账户名称
        '''
        return self.send_request(*_SubAccountEndpoints.get_entrust_subaccount_list, **to_local(locals()))

    # 获取用户的节点返佣信息
    def get_if_rebate(self, apiKey: str, proxies={}, proxy_host: str = None):
        '''
        该接口用于节点查询用户的返佣信息
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-get-the-user-39-s-affiliate-rebate-information
        
        限速：20次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        apiKey            	String  	是       	用户的 API key，仅支持使用被邀请人母账号的 API key
        返回参数:
        Parameter         	Type    	Description
        result            	Boolean 	用户是否与当前节点有邀请关系。true,false
        type              	String  	是否有节点返佣0有节点返佣1没有节点返佣，因为调用该接口的账户不是节点身份2没有节点返佣，因为不存在邀请/召回关系，如：api key不存在4没有节点返佣，因为用户的手续费等级大于等于VIP6
        '''
        return self.send_request(*_SubAccountEndpoints.get_if_rebate, **to_local(locals()))

    # 设置子账户尊享借币比率
    def set_loan_allocation(self, enable: bool, alloc: object = '', proxies={}, proxy_host: str = None):
        '''
        为子账户设置 VIP 尊享借币可用额度的比率（百分比），仅适用于有交易权限的母账户 API key.
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-set-sub-accounts-vip-loan-allocation
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        enable            	Boolean 	是       	为子账户设置 VIP 尊享借币可用额度的比率。true或者false
        alloc             	Array of objects	否       	如果 enable = false, 将不会验证该参数
        > subAcct         	String  	是       	子账户名称
        > loanAlloc       	String  	是       	子账户尊享借币可用额度的比率（百分比）范围为[0, 100]. 精度为 0.01% (2位小数)"0" 代表取消子账户的 VIP 借币额度。
        返回参数:
        Parameter         	Type    	Description
        result            	String  	请求结果，枚举值为true,false
        '''
        return self.send_request(*_SubAccountEndpoints.set_loan_allocation, **to_local(locals()))

    # 获取子账户借币利率与限额
    def get_interest_limits(self, subAcct: str, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        仅适用于母账户的 API key, 仅返回尊享借币信息。
        https://www.okx.com/docs-v5/zh/#sub-account-rest-api-get-sub-account-borrow-interest-and-limit
        
        限速：5次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        subAcct           	String  	是       	子账户名称， 只能填写一个
        ccy               	String  	否       	借贷币种，如BTC
        返回参数:
        Parameter         	Type    	Description
        subAcct           	String  	子账户名称
        interest          	String  	可忽略，只返回 “”
        nextDiscountTime  	String  	下次扣息时间，Unix时间戳的毫秒数格式，如1597026383085
        nextInterestTime  	String  	下次计息时间，Unix时间戳的毫秒数格式，如1597026383085
        loanAlloc         	String  	当前交易账户尊享借币可用额度的比率（百分比）1. 范围为[0, 100]. 精度为 0.01% (2位小数)2. 0 代表母账户没有为子账户分配；3. "" 代表母子账户共享
        records           	Array   	各币种详细信息
        > ccy             	String  	借贷币种，如BTC
        > rate            	String  	日利率
        > loanQuota       	String  	母账户维度借币限额如果已配置可用额度，该字段代表当前交易账户（子账户）的借币限额
        > surplusLmt      	String  	母子账户剩余可借如果已配置可用额度，该字段代表当前交易账户（子账户）的剩余可借
        > surplusLmtDetails	Array   	母子账户剩余可借额度详情，母子账户剩余可借额度的值取该数组中的最小值，可以用来判断是什么原因导致可借额度不足仅适用于尊享借币
        >> allAcctRemainingQuota	String  	母子账户剩余额度
        >> curAcctRemainingQuota	String  	当前子账户剩余额度仅适用于为子账户分配限额的场景
        >> platRemainingQuota	String  	平台剩余额度，当平台剩余额度大于curAcctRemainingQuota或者allAcctRemainingQuota时，会显示大于某个值，如">1000"
        > usedLmt         	String  	母子账户已借额度如果已配置可用额度，该字段代表当前交易账户（子账户）的已借额度
        > interest        	String  	可忽略，只返回 “”
        > posLoan         	String  	当前账户负债占用（子账户，锁定额度内）仅适用于尊享借币
        > availLoan       	String  	当前账户剩余可用（子账户，锁定额度内）仅适用于尊享借币
        > usedLoan        	String  	当前账户（子账户）已借额度仅适用于尊享借币
        > avgRate         	String  	币种已借平均(小时)利率，仅适用于尊享借币
        '''
        return self.send_request(*_SubAccountEndpoints.get_interest_limits, **to_local(locals()))

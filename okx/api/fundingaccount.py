'''
资金账户
https://www.okx.com/docs-v5/zh/#funding-account-rest-api
'''
from paux.param import to_local
from okx.api._client import Client


class _FundingAccountEndpoints():
    get_assert_currencies = ['/api/v5/asset/currencies', 'GET']  # 获取币种列表
    get_balances = ['/api/v5/asset/balances', 'GET']  # 获取资金账户余额
    get_non_tradable_assets = ['/api/v5/asset/non-tradable-assets', 'GET']  # 获取不可交易资产
    get_asset_valuation = ['/api/v5/asset/asset-valuation', 'GET']  # 获取账户资产估值
    set_transfer = ['/api/v5/asset/transfer', 'POST']  # 资金划转
    get_transfer_state = ['/api/v5/asset/transfer-state', 'GET']  # 获取资金划转状态
    get_bills = ['/api/v5/asset/bills', 'GET']  # 获取资金流水
    get_deposit_lightning = ['/api/v5/asset/deposit-lightning', 'GET']  # 闪电网络充币
    get_deposit_address = ['/api/v5/asset/deposit-address', 'GET']  # 获取充值地址信息
    get_deposit_history = ['/api/v5/asset/deposit-history', 'GET']  # 获取充值记录
    set_withdrawal = ['/api/v5/asset/withdrawal', 'POST']  # 提币
    set_withdrawal_lightning = ['/api/v5/asset/withdrawal-lightning', 'POST']  # 闪电网络提币
    set_cancel_withdrawal = ['/api/v5/asset/cancel-withdrawal', 'POST']  # 撤销提币
    get_withdrawal_history = ['/api/v5/asset/withdrawal-history', 'GET']  # 获取提币记录
    get_deposit_withdraw_status = ['/api/v5/asset/deposit-withdraw-status', 'GET']  # 获取充值/提现的详细状态
    set_convert_dust_assets = ['/api/v5/asset/convert-dust-assets', 'POST']  # 小额资产兑换
    get_exchange_list = ['/api/v5/asset/exchange-list', 'GET']  # 获取交易所列表（公共）
    get_convert_currencies = ['/api/v5/asset/convert/currencies', 'GET']  # 获取闪兑币种列表
    get_currency_pair = ['/api/v5/asset/convert/currency-pair', 'GET']  # 获取闪兑币对信息
    set_estimate_quote = ['/api/v5/asset/convert/estimate-quote', 'POST']  # 闪兑预估询价
    set_trade = ['/api/v5/asset/convert/trade', 'POST']  # 闪兑交易
    get_history = ['/api/v5/asset/convert/history', 'GET']  # 获取闪兑交易历史


class FundingAccount(Client):

    # 获取币种列表
    def get_assert_currencies(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        获取平台所有币种列表。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-currencies
        
        限速：6 次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种名称，如BTC
        name              	String  	币种名称，不显示则无对应名称
        logoLink          	String  	币种Logo链接
        chain             	String  	币种链信息有的币种下有多个链，必须要做区分，如USDT下有USDT-ERC20，USDT-TRC20多个链
        canDep            	Boolean 	当前是否可充值false：不可链上充值true：可以链上充值
        canWd             	Boolean 	当前是否可提币false：不可链上提币true：可以链上提币
        canInternal       	Boolean 	当前是否可内部转账false：不可内部转账true：可以内部转账
        minDep            	String  	币种单笔最小充值量
        minWd             	String  	币种单笔最小提币量
        maxWd             	String  	币种单笔最大提币量
        wdTickSz          	String  	提币精度,表示小数点后的位数。提币手续费精度与提币精度保持一致。内部转账提币精度为小数点后8位。
        wdQuota           	String  	过去24小时内提币额度（包含链上提币和内部转账），单位为USD
        usedWdQuota       	String  	过去24小时内已用提币额度，单位为USD
        minFee            	String  	普通地址最小提币手续费数量适用于链上提币
        maxFee            	String  	普通地址最大提币手续费数量适用于链上提币
        minFeeForCtAddr   	String  	合约地址最小提币手续费数量适用于链上提币
        maxFeeForCtAddr   	String  	合约地址最大提币手续费数量适用于链上提币
        mainNet           	Boolean 	当前链是否为主链
        needTag           	Boolean 	当前链是否需要标签（tag/memo）信息，如EOS该字段为true
        minDepArrivalConfirm	String  	充值到账最小网络确认数。币已到账但不可提。
        minWdUnlockConfirm	String  	提现解锁最小网络确认数
        depQuotaFixed     	String  	充币固定限额，单位为USD没有充币限制则返回""
        usedDepQuotaFixed 	String  	已用充币固定额度，单位为USD没有充币限制则返回""
        depQuoteDailyLayer2	String  	Layer2网络每日充值上限
        '''
        return self.send_request(*_FundingAccountEndpoints.get_assert_currencies, **to_local(locals()))

    # 获取资金账户余额
    def get_balances(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        获取资金账户所有资产列表，查询各币种的余额、冻结和可用等信息。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-balance
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种，如BTC
        bal               	String  	余额
        frozenBal         	String  	冻结余额
        availBal          	String  	可用余额
        '''
        return self.send_request(*_FundingAccountEndpoints.get_balances, **to_local(locals()))

    # 获取不可交易资产
    def get_non_tradable_assets(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/asset/non-tradable-assets
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-non-tradable-assets
        
        限速：6 次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种名称，如CELT
        name              	String  	币种中文名称，不显示则无对应名称
        logoLink          	String  	币种Logo链接
        bal               	String  	可提余额
        canWd             	Boolean 	是否可提false: 不可提true: 可提
        chain             	String  	支持提币的链
        minWd             	String  	币种单笔最小提币量
        wdAll             	Boolean 	该币种资产是否必须一次性全部提取
        fee               	String  	提币固定手续费，单位是USDT。提币手续费精度为小数点后8位。
        ctAddr            	String  	合约地址后6位
        wdTickSz          	String  	提币精度,表示小数点后的位数
        needTag           	Boolean 	提币的链是否需要标签（tag/memo）信息
        '''
        return self.send_request(*_FundingAccountEndpoints.get_non_tradable_assets, **to_local(locals()))

    # 获取账户资产估值
    def get_asset_valuation(self, ccy: str = '', proxies={}, proxy_host: str = None):
        '''
        查看账户资产估值
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-account-asset-valuation
        
        限速：1次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	资产估值对应的单位BTC 、USDTUSD 、CNY 、JPY、KRW、RUB、EURVND 、IDR 、INR、PHP、THB、TRYAUD 、SGD 、ARS、SAR、AED、IQD默认为  BTC 为单位的估值
        返回参数:
        Parameter         	Type    	Description
        totalBal          	String  	账户总资产估值
        ts                	String  	数据更新时间，Unix时间戳的毫秒数格式，如 1597026383085
        details           	Object  	各个账户的资产估值
        > funding         	String  	资金账户
        > trading         	String  	交易账户
        > classic         	String  	经典账户 (已废弃)
        > earn            	String  	金融账户
        '''
        return self.send_request(*_FundingAccountEndpoints.get_asset_valuation, **to_local(locals()))

    # 资金划转
    def set_transfer(self, ccy: str, amt: str, from_:str, to: str, type: str = '', subAcct: str = '',
                     loanTrans: bool = '', omitPosRisk: str = '', clientId: str = '', proxies={},
                     proxy_host: str = None):
        '''
        调用时，API Key 需要有交易权限。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-funds-transfer
        
        限速：1 次/s
        限速规则：UserID + Currency
    
        请求参数:
        Parameter         	Type    	Required	Description

        type              	String  	否       	划转类型0：账户内划转1：母账户转子账户(仅适用于母账户APIKey)2：子账户转母账户(仅适用于母账户APIKey)3：子账户转母账户(仅适用于子账户APIKey)4：子账户转子账户(仅适用于子账户APIKey，且目标账户需要是同一母账户下的其他子账户。子账户主动转出权限默认是关闭的，权限调整参考设置子账户主动转出权限。)默认是0如果您希望通过母账户API Key控制子账户之间的划转，参考接口子账户间资金划转
        ccy               	String  	是       	划转币种，如USDT
        amt               	String  	是       	划转数量
        from              	String  	是       	转出账户6：资金账户18：交易账户
        to                	String  	是       	转入账户6：资金账户18：交易账户
        subAcct           	String  	可选      	子账户名称当type为1/2/4时，该字段必填
        loanTrans         	Boolean 	否       	是否支持跨币种保证金模式或组合保证金模式下的借币转出true：支持借币转出false：不支持借币转出默认为false
        omitPosRisk       	String  	否       	是否忽略仓位风险默认为false仅适用于组合保证金模式
        clientId          	String  	否       	客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        返回参数:
        Parameter         	Type    	Description
        transId           	String  	划转 ID
        ccy               	String  	划转币种
        from              	String  	转出账户
        amt               	String  	划转量
        to                	String  	转入账户
        clientId          	String  	客户自定义ID
        '''
        data = to_local(locals())
        data['form'] = data['form_']
        del data['from_']

        return self.send_request(*_FundingAccountEndpoints.set_transfer, **data)

    # 获取资金划转状态
    def get_transfer_state(self, transId: str = '', clientId: str = '', type: str = '', proxies={},
                           proxy_host: str = None):
        '''
        获取最近2个星期内的资金划转状态数据
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-funds-transfer-state
        
        限速：10 次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        transId           	String  	可选      	划转IDtransId和clientId必须传一个，若传两个，以transId为主
        clientId          	String  	可选      	客户自定义ID
        type              	String  	否       	划转类型0：账户内划转1：母账户转子账户(仅适用于母账户APIKey)2：子账户转母账户(仅适用于母账户APIKey)3：子账户转母账户(仅适用于子账户APIKey)4：子账户转子账户(仅适用于子账户APIKey，且目标账户需要是同一母账户下的其他子账户)默认是0
        返回参数:
        Parameter         	Type    	Description
        transId           	String  	划转 ID
        clientId          	String  	客户自定义 ID
        ccy               	String  	划转币种
        amt               	String  	划转量
        type              	String  	划转类型0：账户内划转1：母账户转子账户(仅适用于母账户APIKey)2：子账户转母账户(仅适用于母账户APIKey)3：子账户转母账户(仅适用于子账户APIKey)4：子账户转子账户(仅适用于子账户APIKey，且目标账户需要是同一母账户下的其他子账户)
        from              	String  	转出账户6：资金账户18：交易账户
        to                	String  	转入账户6：资金账户18：交易账户
        subAcct           	String  	子账户名称
        instId            	String  	已废弃
        toInstId          	String  	已废弃
        state             	String  	转账状态success：成功pending：处理中failed：失败
        '''
        return self.send_request(*_FundingAccountEndpoints.get_transfer_state, **to_local(locals()))

    # 获取资金流水
    def get_bills(self, ccy: str = '', type: str = '', clientId: str = '', after: str = '', before: str = '',
                  limit: str = '', proxies={}, proxy_host: str = None):
        '''
        查询资金账户账单流水
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-asset-bills-details
        
        限速：6 次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种
        type              	String  	否       	请参考官方文档
        clientId          	String  	否       	转账或提币的客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为 100，不填默认返回 100 条
        返回参数:
        Parameter         	Type    	Description
        billId            	String  	账单 ID
        ccy               	String  	账户余额币种
        clientId          	String  	转账或提币的客户自定义ID
        balChg            	String  	账户层面的余额变动数量
        bal               	String  	账户层面的余额数量
        type              	String  	账单类型
        ts                	String  	账单创建时间，Unix 时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_FundingAccountEndpoints.get_bills, **to_local(locals()))

    # 闪电网络充币
    def get_deposit_lightning(self, ccy: str, amt: str, to: str = '', proxies={}, proxy_host: str = None):
        '''
        一个用户在最近24小时内可以生成不超过1万个不同的invoice。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-lightning-deposits
        
        限速：2次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种，仅支持BTC
        amt               	String  	是       	充值数量，推荐在0.000001〜0.1之间
        to                	String  	否       	资金充值到账账户6：资金账户18：交易账户默认是6
        返回参数:
        Parameter         	Type    	Description
        invoice           	String  	invoice 号码
        cTime             	String  	生成invoice时间
        '''
        return self.send_request(*_FundingAccountEndpoints.get_deposit_lightning, **to_local(locals()))

    # 获取充值地址信息
    def get_deposit_address(self, ccy: str, proxies={}, proxy_host: str = None):
        '''
        获取各个币种的充值地址，包括曾使用过的老地址。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-deposit-address
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种，如BTC
        返回参数:
        Parameter         	Type    	Description
        addr              	String  	充值地址
        tag               	String  	部分币种充值需要标签，若不需要则不返回此字段
        memo              	String  	部分币种充值需要 memo，若不需要则不返回此字段
        pmtId             	String  	部分币种充值需要此字段（payment_id），若不需要则不返回此字段
        addrEx            	Object  	充值地址备注，部分币种充值需要，若不需要则不返回此字段如币种TONCOIN的充值地址备注标签名为comment,则该字段返回：{'comment':'123456'}
        ccy               	String  	币种，如BTC
        chain             	String  	币种链信息有的币种下有多个链，必须要做区分，如USDT下有USDT-ERC20，USDT-TRC20多个链
        to                	String  	转入账户6：资金账户18：交易账户
        selected          	Boolean 	该地址是否为页面选中的地址
        ctAddr            	String  	合约地址后6位
        '''
        return self.send_request(*_FundingAccountEndpoints.get_deposit_address, **to_local(locals()))

    # 获取充值记录
    def get_deposit_history(self, ccy: str = '', depId: str = '', fromWdId: str = '', txId: str = '', type: str = '',
                            state: str = '', after: str = '', before: str = '', limit: object = '', proxies={},
                            proxy_host: str = None):
        '''
        根据币种，充值状态，时间范围获取充值记录，按照时间倒序排列，默认返回 100 条数据。<!- 1-2-3 -->支持Websocket订阅，参考充值信息频道。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-deposit-history
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种名称，如BTC
        depId             	String  	否       	充值记录 ID
        fromWdId          	String  	否       	内部转账发起者提币申请 ID如果该笔充值来自于内部转账，则该字段展示内部转账发起者的提币申请 ID
        txId              	String  	否       	区块转账哈希记录
        type              	String  	否       	充值方式3：内部转账4：链上充值
        state             	String  	否       	充值状态0：等待确认1：确认到账2：充值成功8：因该币种暂停充值而未到账，恢复充值后自动到账11：命中地址黑名单12：账户或充值被冻结13：子账户充值拦截14：KYC限额
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1654041600000
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1656633600000
        limit             	string  	否       	返回的结果集数量，默认为100，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种名称，如BTC
        chain             	String  	币种链信息有的币种下有多个链，必须要做区分，如USDT下有USDT-ERC20，USDT-TRC20多个链
        amt               	String  	充值数量
        from              	String  	充值账户如果该笔充值来自于内部转账，则该字段展示内部转账发起者的账户信息，可以是手机号、邮箱、账户名称，其他情况返回""
        areaCodeFrom      	String  	如果from为手机号，该字段为该手机号的区号
        to                	String  	到账地址如果该笔充值来自于链上充值，则该字段展示链上地址，其他情况返回""
        txId              	String  	区块转账哈希记录
        ts                	String  	充值记录创建时间，Unix 时间戳的毫秒数格式，如1655251200000
        state             	String  	充值状态0：等待确认1：确认到账2：充值成功8：因该币种暂停充值而未到账，恢复充值后自动到账11：命中地址黑名单12：账户或充值被冻结13：子账户充值拦截14：KYC限额
        depId             	String  	充值记录 ID
        fromWdId          	String  	内部转账发起者提币申请 ID如果该笔充值来自于内部转账，则该字段展示内部转账发起者的提币申请 ID，其他情况返回""
        actualDepBlkConfirm	String  	最新的充币网络确认数
        '''
        return self.send_request(*_FundingAccountEndpoints.get_deposit_history, **to_local(locals()))

    # 提币
    def set_withdrawal(self, ccy: str, amt: str, dest: str, toAddr: str, fee: str, chain: str = '', areaCode: str = '',
                       rcvrInfo: str = '', clientId: str = '', proxies={}, proxy_host: str = None):
        '''
        用户提币。普通子账户不支持提币。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-withdrawal
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种，如USDT
        amt               	String  	是       	提币数量该数量不包含手续费
        dest              	String  	是       	提币方式3：内部转账4：链上提币
        toAddr            	String  	是       	如果选择链上提币，toAddr必须是认证过的数字货币地址。某些数字货币地址格式为地址:标签，如ARDOR-7JF3-8F2E-QUWZ-CAN7F:123456如果选择内部转账，toAddr必须是接收方地址，可以是邮箱、手机或者账户名（只有子账户才有账户名）。
        fee               	String  	是       	提币到数字货币地址所需网络手续费可以通过接口获取币种列表获取内部转账无需手续费
        chain             	String  	可选      	币种链信息如USDT下有USDT-ERC20，USDT-TRC20多个链如果没有不填此参数，则默认为主链对于无效资产提币，不填此参数，则默认为唯一的提币链适用于链上提币，链信息可以通过接口获取币种列表获取
        areaCode          	String  	可选      	手机区号，如86当toAddr为手机号时，该参数必填适用于内部转账
        rcvrInfo          	String  	可选      	接收方信息特定 国家/地区 认证用户做链上提币需要提供此信息
        > walletType      	String  	是       	钱包类型exchange：提币到交易所钱包private：提币到私人钱包如果提币到交易所钱包，必须提供exchId,rcvrFirstName,rcvrLastName提币到私人钱包，则不需要提供其他信息
        > exchId          	String  	可选      	交易所 ID可以通过获取交易所列表（公共）接口查询支持的交易所如果交易所不在支持的交易所列表中，该字段填0
        > rcvrFirstName   	String  	可选      	接收方名字，如Bruce
        > rcvrLastName    	String  	可选      	接收方姓氏，如Wayne
        clientId          	String  	否       	客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	提币币种
        chain             	String  	币种链信息有的币种下有多个链，必须要做区分，如USDT下有USDT-ERC20，USDT-TRC20多个链
        amt               	String  	提币数量
        wdId              	String  	提币申请ID
        clientId          	String  	客户自定义ID
        '''
        return self.send_request(*_FundingAccountEndpoints.set_withdrawal, **to_local(locals()))

    # 闪电网络提币
    def set_withdrawal_lightning(self, ccy: str, invoice: str, memo: str = '', rcvrInfo: str = '', proxies={},
                                 proxy_host: str = None):
        '''
        单笔提币金额最大值为"0.1BTC"，最小值暂定为"0.000001BTC"，最近24小时内最大提币数量为"1BTC"。子账户不支持提币。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-lightning-withdrawals
        
        限速：2次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	是       	币种，如BTC
        invoice           	String  	是       	invoice 号码
        memo              	String  	否       	闪电网络提币的备注
        rcvrInfo          	String  	可选      	接收方信息特定 国家/地区 认证用户做链上提币需要提供此信息
        > walletType      	String  	是       	钱包类型exchange：提币到交易所钱包private：提币到私人钱包如果提币到交易所钱包，必须提供exchId,rcvrFirstName,rcvrLastName提币到私人钱包，则不需要提供其他信息
        > exchId          	String  	可选      	交易所 ID可以通过获取交易所列表（公共）接口查询支持的交易所如果交易所不在支持的交易所列表中，该字段填0
        > rcvrFirstName   	String  	可选      	接收方名字，如Bruce
        > rcvrLastName    	String  	可选      	接收方姓氏，如Wayne
        返回参数:
        Parameter         	Type    	Description
        wdId              	String  	提币申请 ID
        cTime             	String  	提币申请 ID生成时间
        '''
        return self.send_request(*_FundingAccountEndpoints.set_withdrawal_lightning, **to_local(locals()))

    # 撤销提币
    def set_cancel_withdrawal(self, wdId: str, proxies={}, proxy_host: str = None):
        '''
        可以撤销普通提币，但不支持撤销闪电网络上的提币。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-cancel-withdrawal
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        wdId              	String  	是       	提币申请ID
        返回参数:
        Parameter         	Type    	Description
        wdId              	String  	提币申请ID
        '''
        return self.send_request(*_FundingAccountEndpoints.set_cancel_withdrawal, **to_local(locals()))

    # 获取提币记录
    def get_withdrawal_history(self, ccy: str = '', wdId: str = '', clientId: str = '', txId: str = '', type: str = '',
                               state: str = '', after: str = '', before: str = '', limit: object = '', proxies={},
                               proxy_host: str = None):
        '''
        根据币种，提币状态，时间范围获取提币记录，按照时间倒序排列，默认返回100条数据。<!- 1-2-3 -->支持Websocket订阅，参考提币信息频道。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-withdrawal-history
        
        限速：6 次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	String  	否       	币种名称，如BTC
        wdId              	String  	否       	提币申请ID
        clientId          	String  	否       	客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        txId              	String  	否       	区块转账哈希记录
        type              	String  	否       	提币方式3：内部转账4：链上提币
        state             	String  	否       	提币状态-3：撤销中-2：已撤销-1：失败0：等待提币1：提币中2：提币成功7: 审核通过10: 等待划转4,5,6,8,9,12: 等待客服审核
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1654041600000
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1656633600000
        limit             	string  	否       	返回的结果集数量，默认为100，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种
        chain             	String  	币种链信息有的币种下有多个链，必须要做区分，如USDT下有USDT-ERC20，USDT-TRC20多个链
        nonTradableAsset  	Boolean 	是否为不可交易资产true：不可交易资产，false：可交易资产
        amt               	String  	数量
        ts                	String  	提币申请时间，Unix 时间戳的毫秒数格式，如1655251200000
        from              	String  	提币账户可以是邮箱/手机号
        areaCodeFrom      	String  	如果from为手机号，该字段为该手机号的区号
        to                	String  	收币地址
        areaCodeTo        	String  	如果to为手机号，该字段为该手机号的区号
        tag               	String  	部分币种提币需要标签，若不需要则不返回此字段
        pmtId             	String  	部分币种提币需要此字段（payment_id），若不需要则不返回此字段
        memo              	String  	部分币种提币需要此字段，若不需要则不返回此字段
        addrEx            	Object  	提币地址备注，部分币种提币需要，若不需要则不返回此字段。如币种TONCOIN的提币地址备注标签名为comment,则该字段返回：{'comment':'123456'}
        txId              	String  	提币哈希记录内部转账该字段返回""
        fee               	String  	提币手续费数量
        feeCcy            	String  	提币手续费币种，如USDT
        state             	String  	提币状态-3：撤销中-2：已撤销-1：失败0：等待提币1：提币中2：提币成功7: 审核通过10: 等待划转4,5,6,8,9,12: 等待客服审核
        wdId              	String  	提币申请ID
        clientId          	String  	客户自定义ID
        '''
        return self.send_request(*_FundingAccountEndpoints.get_withdrawal_history, **to_local(locals()))

    # 获取充值/提现的详细状态
    def get_deposit_withdraw_status(self, wdId: str = '', txId: str = '', ccy: str = '', to: str = '', chain: str = '',
                                    proxies={}, proxy_host: str = None):
        '''
        获取充值与提现的详细状态信息与预估完成时间。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-deposit-withdraw-status
        
        限速：1次/2s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        wdId              	String  	可选      	提币申请ID，用于查询资金提现wdId与txId必传其一也仅可传其一
        txId              	String  	可选      	区块转账哈希记录ID，用于查询资金充值wdId与txId必传其一也仅可传其一
        ccy               	String  	可选      	币种，如USDT查询充值时必填，需要与txId一并提供
        to                	String  	可选      	资金充值到账账户地址查询充值时必填，需要与txId一并提供
        chain             	String  	可选      	币种链信息，例如 USDT-ERC20查询充值时必填，需要与txId一并提供
        返回参数:
        Parameter         	Type    	Description
        estCompleteTime   	String  	预估完成时间时区为 UTC+8；格式为 MM/dd/yyyy, h:mm:ss AM/PMestCompleteTime仅为预估完成时间，仅供参考
        state             	String  	充值/提现的现处于的详细阶段提示冒号前面代表阶段，后面代表状态
        txId              	String  	区块转账哈希记录如查询的是提现，则txId返回为空""，此时提现如生成了txId将一并返回
        wdId              	String  	提币申请ID如查询的是充值，则wdId返回为空""
        '''
        return self.send_request(*_FundingAccountEndpoints.get_deposit_withdraw_status, **to_local(locals()))

    # 小额资产兑换
    def set_convert_dust_assets(self, ccy: object, proxies={}, proxy_host: str = None):
        '''
        将资金账户中的小额资产转化为OKB。24小时之内只能兑换5次。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-small-assets-convert
        
        限速：1次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        ccy               	Array of strings	是       	需要转换的币种资产，如 ["BTC","USDT"]
        返回参数:
        Parameter         	Type    	Description
        totalCnvAmt       	String  	兑换后总OKB数量
        details           	Array of objects	各币种资产转换详情
        > ccy             	String  	币种资产,如BTC
        > amt             	String  	转换前币种资产数量
        > cnvAmt          	String  	转换后的OKB数量
        > fee             	String  	兑换手续费，单位为OKB
        '''
        return self.send_request(*_FundingAccountEndpoints.set_convert_dust_assets, **to_local(locals()))

    # 获取交易所列表（公共）
    def get_exchange_list(self, proxies={}, proxy_host: str = None):
        '''
        公共接口无须鉴权
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-exchange-list-public
        
        限速：6次/s
        限速规则：IP
    
        
        返回参数:
        Parameter         	Type    	Description
        exchName          	String  	交易所名称，如1xbet
        exchId            	String  	交易所 ID，如did:ethr:0xfeb4f99829a9acdf52979abee87e83addf22a7e1
        '''
        return self.send_request(*_FundingAccountEndpoints.get_exchange_list, **to_local(locals()))

    # 获取闪兑币种列表
    def get_convert_currencies(self, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/asset/convert/currencies
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-convert-currencies
        
        限速：6次/s
        限速规则：UserID
    
        
        返回参数:
        Parameter         	Type    	Description
        ccy               	String  	币种名称，如BTC
        min               	String  	支持闪兑的最小值(已废弃)
        max               	String  	支持闪兑的最大值(已废弃)
        '''
        return self.send_request(*_FundingAccountEndpoints.get_convert_currencies, **to_local(locals()))

    # 获取闪兑币对信息
    def get_currency_pair(self, fromCcy: str, toCcy: str, proxies={}, proxy_host: str = None):
        '''
        GET /api/v5/asset/convert/currency-pair
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-convert-currency-pair
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        fromCcy           	String  	是       	消耗币种，如USDT
        toCcy             	String  	是       	获取币种，如BTC
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	币对，如BTC-USDT
        baseCcy           	String  	交易货币币种，如BTC-USDT中的BTC
        baseCcyMax        	String  	交易货币支持闪兑的最大值
        baseCcyMin        	String  	交易货币支持闪兑的最小值
        quoteCcy          	String  	计价货币币种，如BTC-USDT中的USDT
        quoteCcyMax       	String  	计价货币支持闪兑的最大值
        quoteCcyMin       	String  	计价货币支持闪兑的最小值
        '''
        return self.send_request(*_FundingAccountEndpoints.get_currency_pair, **to_local(locals()))

    # 闪兑预估询价
    def set_estimate_quote(self, baseCcy: str, quoteCcy: str, side: str, rfqSz: str, rfqSzCcy: str, clQReqId: str = '',
                           tag: str = '', proxies={}, proxy_host: str = None):
        '''
        POST /api/v5/asset/convert/estimate-quote
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-estimate-quote
        
        限速：10次/s限速：1次/5s
        限速规则：UserID限速规则：Instrument
    
        请求参数:
        Parameter         	Type    	Required	Description

        baseCcy           	String  	是       	交易货币币种，如BTC-USDT中的BTC
        quoteCcy          	String  	是       	计价货币币种，如BTC-USDT中的USDT
        side              	String  	是       	交易方向买：buy卖：sell描述的是对于baseCcy的交易方向
        rfqSz             	String  	是       	询价数量
        rfqSzCcy          	String  	是       	询价币种
        clQReqId          	String  	否       	客户端自定义的订单标识字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签适用于broker用户
        返回参数:
        Parameter         	Type    	Description
        quoteTime         	String  	生成报价时间，Unix时间戳的毫秒数格式
        ttlMs             	String  	报价有效期，单位为毫秒
        clQReqId          	String  	客户端自定义的订单标识
        quoteId           	String  	报价ID
        baseCcy           	String  	交易货币币种，如 BTC-USDT 中BTC
        quoteCcy          	String  	计价货币币种，如 BTC-USDT 中USDT
        side              	String  	交易方向买：buy卖：sell
        origRfqSz         	String  	原始报价的数量
        rfqSz             	String  	实际报价的数量
        rfqSzCcy          	String  	报价的币种
        cnvtPx            	String  	闪兑价格，单位为计价币
        baseSz            	String  	闪兑交易币数量
        quoteSz           	String  	闪兑计价币数量
        '''
        return self.send_request(*_FundingAccountEndpoints.set_estimate_quote, **to_local(locals()))

    # 闪兑交易
    def set_trade(self, quoteId: str, baseCcy: str, quoteCcy: str, side: str, sz: str, szCcy: str, clTReqId: str = '',
                  tag: str = '', proxies={}, proxy_host: str = None):
        '''
        闪兑交易前需要先询价。
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-convert-trade
        
        限速：10次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        quoteId           	String  	是       	报价ID
        baseCcy           	String  	是       	交易货币币种，如BTC-USDT中的BTC
        quoteCcy          	String  	是       	计价货币币种，如BTC-USDT中的USDT
        side              	String  	是       	交易方向buy：买sell：卖描述的是对于baseCcy的交易方向
        sz                	String  	是       	用户报价数量报价数量应不大于预估询价中的询价数量
        szCcy             	String  	是       	用户报价币种
        clTReqId          	String  	否       	用户自定义的订单标识字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签适用于broker用户
        返回参数:
        Parameter         	Type    	Description
        tradeId           	String  	成交ID
        quoteId           	String  	报价ID
        clTReqId          	String  	用户自定义的订单标识
        state             	String  	状态fullyFilled：交易成功rejected：交易失败
        instId            	String  	币对，如BTC-USDT
        baseCcy           	String  	交易货币币种，如BTC-USDT中BTC
        quoteCcy          	String  	计价货币币种，如BTC-USDT中USDT
        side              	String  	交易方向买：buy卖：sell
        fillPx            	String  	成交价格，单位为计价币
        fillBaseSz        	String  	成交的交易币数量
        fillQuoteSz       	String  	成交的计价币数量
        ts                	String  	闪兑交易时间，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        '''
        return self.send_request(*_FundingAccountEndpoints.set_trade, **to_local(locals()))

    # 获取闪兑交易历史
    def get_history(self, after: str = '', before: str = '', limit: str = '', tag: str = '', proxies={},
                    proxy_host: str = None):
        '''
        GET /api/v5/asset/convert/history
        https://www.okx.com/docs-v5/zh/#funding-account-rest-api-get-convert-history
        
        限速：6次/s
        限速规则：UserID
    
        请求参数:
        Parameter         	Type    	Required	Description

        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	返回的结果集数量，默认为100，最大为100
        tag               	String  	否       	订单标签适用于broker用户如果闪兑交易带上了tag,查询时必须也带上此参数
        返回参数:
        Parameter         	Type    	Description
        tradeId           	String  	成交ID
        state             	String  	fullyFilled：交易成功rejected：交易失败
        instId            	String  	币对，如BTC-USDT
        baseCcy           	String  	交易货币币种，如BTC-USDT中的BTC
        quoteCcy          	String  	计价货币币种，如BTC-USDT中的USDT
        side              	String  	交易方向买：buy卖：sell
        fillPx            	String  	成交价格，单位为计价币
        fillBaseSz        	String  	成交的交易币数量
        fillQuoteSz       	String  	成交的计价币数量
        ts                	String  	闪兑交易时间，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        '''
        return self.send_request(*_FundingAccountEndpoints.get_history, **to_local(locals()))

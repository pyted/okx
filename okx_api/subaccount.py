from paux.param import to_local
from okx_api._client import Client


class _SubAccountEndpoints:
    get_list = ['/api/v5/users/subaccount/list', 'GET']  # 查看子账户列表
    set_modify_apikey = ['/api/v5/users/subaccount/modify-apikey', 'POST']  # 重置子账户的APIKey
    get_account_balances = ['/api/v5/account/subaccount/balances', 'GET']  # 获取子账户交易账户余额
    get_asset_balances = ['/api/v5/asset/subaccount/balances', 'GET']  # 获取子账户资金账户余额
    get_bills = ['/api/v5/asset/subaccount/bills', 'GET']  # 查询子账户转账记录
    set_transfer = ['/api/v5/asset/subaccount/transfer', 'POST']  # 子账户间资金划转
    set_set_transfer_out = ['/api/v5/users/subaccount/set-transfer-out', 'POST']  # 设置子账户主动转出权限
    get_entrust_subaccount_list = ['/api/v5/users/entrust-subaccount-list', 'GET']  # 查看被托管的子账户列表
    get_if_rebate = ['/api/v5/users/partner/if-rebate', 'GET']  # 获取用户的节点返佣信息


class SubAccount(Client):
    # 查看子账户列表
    def get_list(self, enable: str = '', subAcct: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-subaccount-view-sub-account-list

        请求参数：
        Parameter         	Type    	Required	Description
        enable            	String  	否       	子账户状态，true：正常使用false：冻结
        subAcct           	String  	否       	子账户名称
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_SubAccountEndpoints.get_list, **to_local(locals()))

    # 重置子账户的APIKey
    def set_modify_apikey(self, subAcct: str, apiKey: str, label: str = '', perm: str = '', ip: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-subaccount-reset-the-apikey-of-a-sub-account

        请求参数：
        Parameter         	Type    	Required	Description
        subAcct           	String  	是       	子账户名称
        apiKey            	String  	是       	子账户API的公钥
        label             	String  	否       	子账户APIKey的备注，如果填写该字段，则该字段会被重置
        perm              	String  	否       	子账户APIKey权限read_only：只读 ；trade：交易多个权限用半角逗号隔开。如果填写该字段，则该字段会被重置
        ip                	String  	否       	子账户APIKey绑定ip地址，多个ip用半角逗号隔开，最多支持20个ip。如果填写该字段，那该字段会被重置如果ip传""，则表示解除IP绑定
        '''
        return self.send_request(*_SubAccountEndpoints.set_modify_apikey, **to_local(locals()))

    # 获取子账户交易账户余额
    def get_account_balances(self, subAcct: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-subaccount-get-sub-account-trading-balance

        请求参数：
        Parameter         	Type    	Required	Description
        subAcct           	String  	是       	子账户名称
        '''
        return self.send_request(*_SubAccountEndpoints.get_account_balances, **to_local(locals()))

    # 获取子账户资金账户余额
    def get_asset_balances(self, subAcct: str, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-subaccount-get-sub-account-funding-balance

        请求参数：
        Parameter         	Type    	Required	Description
        subAcct           	String  	是       	子账户名称
        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        '''
        return self.send_request(*_SubAccountEndpoints.get_asset_balances, **to_local(locals()))

    # 查询子账户转账记录
    def get_bills(self, ccy: str = '', type: str = '', subAcct: str = '', after: str = '', before: str = '',
                  limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-subaccount-history-of-sub-account-transfer

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如 BTC
        type              	String  	否       	0: 母账户转子账户  ；1: 子账户转母账户
        subAcct           	String  	否       	子账户名称
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_SubAccountEndpoints.get_bills, **to_local(locals()))

    # 子账户间资金划转
    def set_transfer(self, ccy: str, amt: str, _from: str, to: str, fromSubAccount: str, toSubAccount: str,
                     loanTrans: bool = '', omitPosRisk: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-subaccount-master-accounts-manage-the-transfers-between-sub-accounts

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	是       	币种
        amt               	String  	是       	划转数量
        from              	String  	是       	6：资金账户18：交易账户
        to                	String  	是       	6：资金账户18：交易账户
        fromSubAccount    	String  	是       	转出子账户的子账户名称
        toSubAccount      	String  	是       	转入子账户的子账户名称
        loanTrans         	Boolean 	否       	是否支持跨币种保证金模式或组合保证金模式下的借币转入/转出true 或 false，默认false
        omitPosRisk       	String  	否       	是否忽略仓位风险默认为false仅适用于组合保证金模式
        '''
        data = to_local(locals())
        data['from'] = data['_from']
        del data['_from']
        return self.send_request(*_SubAccountEndpoints.set_transfer, **data)

    # 设置子账户主动转出权限
    def set_set_transfer_out(self, subAcct: str, canTransOut: bool = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-subaccount-set-permission-of-transfer-out

        请求参数：
        Parameter         	Type    	Required	Description
        subAcct           	String  	是       	子账户名称，支持设置多个（不超过20个），子账户名称之间半角逗号分隔
        canTransOut       	Boolean 	否       	是否可以主动转出，默认为truefalse：不可转出true：可以转出
        '''
        return self.send_request(*_SubAccountEndpoints.set_set_transfer_out, **to_local(locals()))

    # 查看被托管的子账户列表
    def get_entrust_subaccount_list(self, subAcct: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-subaccount-get-custody-trading-sub-account-list

        请求参数：
        Parameter         	Type    	Required	Description
        subAcct           	String  	否       	子账户名称
        '''
        return self.send_request(*_SubAccountEndpoints.get_entrust_subaccount_list, **to_local(locals()))

    # 获取用户的节点返佣信息
    def get_if_rebate(self, apiKey: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-subaccount-get-the-user-39-s-affiliate-rebate-information

        请求参数：
        Parameter         	Type    	Required	Description
        apiKey            	String  	是       	用户的 API key
        '''
        return self.send_request(*_SubAccountEndpoints.get_if_rebate, **to_local(locals()))

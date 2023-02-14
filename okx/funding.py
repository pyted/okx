from paux.param import to_local
from okx._client import Client


class _FundingEndpoints:
    get_currencies = ['/api/v5/asset/currencies', 'GET']  # 获取币种列表
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
    get_saving_balance = ['/api/v5/asset/saving-balance', 'GET']  # 获取余币宝余额
    set_purchase_redempt = ['/api/v5/asset/purchase_redempt', 'POST']  # 余币宝申购/赎回
    set_lending_rate = ['/api/v5/asset/set-lending-rate', 'POST']  # 设置余币宝借贷利率
    get_lending_history = ['/api/v5/asset/lending-history', 'GET']  # 获取余币宝出借明细
    get_lending_rate_summary = ['/api/v5/asset/lending-rate-summary', 'GET']  # 获取市场借贷信息（公共）
    get_lending_rate_history = ['/api/v5/asset/lending-rate-history', 'GET']  # 获取市场借贷历史（公共）


class Funding(Client):
    # 获取币种列表
    def get_currencies(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-currencies

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        '''
        return self.send_request(*_FundingEndpoints.get_currencies, **to_local(locals()))

    # 获取资金账户余额
    def get_balances(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-balance

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        '''
        return self.send_request(*_FundingEndpoints.get_balances, **to_local(locals()))

    # 获取不可交易资产
    def get_non_tradable_assets(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-non-tradable-assets

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔
        '''
        return self.send_request(*_FundingEndpoints.get_non_tradable_assets, **to_local(locals()))

    # 获取账户资产估值
    def get_asset_valuation(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-account-asset-valuation

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	资产估值对应的单位BTC 、USDTUSD 、CNY 、JPY、KRW、RUB、EURVND 、IDR 、INR、PHP、THB、TRYAUD 、SGD 、ARS、SAR、AED、IQD默认为  BTC 为单位的估值
        '''
        return self.send_request(*_FundingEndpoints.get_asset_valuation, **to_local(locals()))

    # 资金划转
    def set_transfer(self, ccy: str, amt: str, _from: str, to: str, subAcct: str = '', type: str = '',
                     loanTrans: bool = '', clientId: str = '', omitPosRisk: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-funds-transfer

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	是       	币种，如USDT
        amt               	String  	是       	划转数量
        from              	String  	是       	转出账户6：资金账户18：交易账户
        to                	String  	是       	转入账户6：资金账户18：交易账户
        subAcct           	String  	可选      	子账户名称，type 为1，2或4：subAcct 为必填项
        type              	String  	否       	划转类型0：账户内划转1：母账户转子账户(仅适用于母账户APIKey)2：子账户转母账户(仅适用于母账户APIKey)3：子账户转母账户(仅适用于子账户APIKey)4：子账户转子账户(仅适用于子账户APIKey，且目标账户需要是同一母账户下的其他子账户)默认是0
        loanTrans         	Boolean 	否       	是否支持跨币种保证金模式或组合保证金模式下的借币转入/转出true 或 false，默认false
        clientId          	String  	否       	客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        omitPosRisk       	String  	否       	是否忽略仓位风险默认为false仅适用于组合保证金模式
        '''
        data = to_local(locals())
        data['from'] = data['_from']
        del data['_from']
        return self.send_request(*_FundingEndpoints.set_transfer, **data)

    # 获取资金划转状态
    def get_transfer_state(self, transId: str = '', clientId: str = '', type: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-funds-transfer-state

        请求参数：
        Parameter         	Type    	Required	Description
        transId           	String  	可选      	划转IDtransId和clientId必须传一个，若传两个，以transId为主
        clientId          	String  	可选      	客户自定义ID
        type              	String  	否       	划转类型0：账户内划转1：母账户转子账户(仅适用于母账户APIKey)2：子账户转母账户(仅适用于母账户APIKey)3：子账户转母账户(仅适用于子账户APIKey)4：子账户转子账户(仅适用于子账户APIKey，且目标账户需要是同一母账户下的其他子账户)默认是0
        '''
        return self.send_request(*_FundingEndpoints.get_transfer_state, **to_local(locals()))

    # 获取资金流水
    def get_bills(self, ccy: str = '', type: str = '', clientId: str = '', after: str = '', before: str = '',
                  limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-asset-bills-details

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种
        type              	String  	否       	账单类型1：充值2：提现13：撤销提现20：转出至子账户（主体是母账户）21：从子账户转入（主体是母账户）22：转出到母账户（主体是子账户）23：母账户转入（主体是子账户）28：领取47：系统冲正48：活动得到49：活动送出50：预约得到51：预约扣除52：发红包53：抢红包54：红包退还61：兑换68：领取卡券权益69：发送卡券权益72：收币73：送币74：送币退还75：申购余币宝76：赎回余币宝77：派发78：锁定79：节点投票80：锁仓挖矿81：投票赎回82：锁仓赎回83：锁仓挖矿收益84：违约金85：算力挖矿收益86：云算力支付87：云算力收益88：补贴收益89：存币收益90：挖矿申购91：挖矿赎回92：补充质押物93：赎回质押物94：投资95：借款人借款96：投资本金转入97：借款人借款转出98：借款人借款利息转出99：投资人投资利息转入102：提前还款违约金转入103：提前还款违约金转出104：抵押借贷手续费转入105：抵押借贷手续费转出106：逾期手续费转入107：逾期手续费转出108：逾期利息转出109：借款还款逾期利息转入110：平仓质押物转入到系统账号111：平仓质押物转出到系统账号112：爆仓质押物转入到系统账号113：爆仓质押物转出到系统账号114：风险准备金转入115：风险准备金转出116：创建订单117：完成订单118：取消订单119：商家解冻保证金120：商家添加保证金121：FiatGateway 创建订单122：FiatGateway 取消订单123：FiatGateway 完成订单124：Jumpstart 解锁125：手动注入126：利息注入127：投资手续费转入128：投资手续费转出129：奖励转入130：从交易账户转入131：转出至交易账户132：客服冻结133：客服解冻134：客服转交135：跨链兑换136：兑换137：ETH2.0申购138：ETH2.0兑换139：ETH2.0收益143：系统退款145：系统回收146：客户回馈147：sushi 增发收益150：节点返佣151：邀请奖励152：经纪商返佣153：新手奖励154：拆盲盒奖励155：福利中心提现156：返佣卡返佣157：红包160：双币赢申购161：双币赢回款162：双币赢收益163：双币赢退款169：2022春节红包172：助力人返佣173：手续费返现174：支付175：锁定质押物176：借款转入177：添加质押物178：减少质押物179：还款180：释放质押物181：偿还空投糖果182：反馈奖励183：邀请好友奖励184：瓜分奖池奖励185：经纪商闪兑返佣186：0元领ETH187：闪兑划转188：插槽竞拍兑换189：盲盒奖励193：卡支付购买195：不可交易资产提币196：不可交易资产提币撤销197：不可交易资产充值198：无效资产减少199：有效资产增加200：买入202：价格锁定申购203：价格锁定回款204：价格锁定收益205：价格锁定退款207：双币赢精简版申购208：双币赢精简版回款209：双币赢精简版收益210：双币赢精简版退款211：投聪夺币中奖212：多币种借贷锁定质押物213：多币种质押物转出用户帐户214：多币种质押物返还用户215：多币种借贷释放质押物216：多币种借贷划转到用户帐户217：多币种借贷借款转入218：多币种借贷还款219：多币种还款由用户帐户转入220：已下架数字货币221：提币手续费支出222：提币手续费退款223：带单分润224：服务费225：鲨鱼鳍申购226：鲨鱼鳍回款227：鲨鱼鳍收益228：鲨鱼鳍退款229：空投发放230：换币完成232：利息补贴已入账233：经纪商佣金补偿
        clientId          	String  	否       	转账或提币的客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为 100，不填默认返回 100 条
        '''
        return self.send_request(*_FundingEndpoints.get_bills, **to_local(locals()))

    # 闪电网络充币
    def get_deposit_lightning(self, ccy: str, amt: str, to: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-lightning-deposits

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	是       	币种，仅支持BTC
        amt               	String  	是       	充值数量，推荐在0.000001〜0.1之间
        to                	String  	否       	资金充值到账账户6: 资金账户18: 交易账户不填写此参数，默认到账资金账户
        '''
        return self.send_request(*_FundingEndpoints.get_deposit_lightning, **to_local(locals()))

    # 获取充值地址信息
    def get_deposit_address(self, ccy: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-deposit-address

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	是       	币种，如BTC
        '''
        return self.send_request(*_FundingEndpoints.get_deposit_address, **to_local(locals()))

    # 获取充值记录
    def get_deposit_history(self, ccy: str = '', depId: str = '', fromWdId: str = '', txId: str = '', type: str = '',
                            state: str = '', after: str = '', before: str = '', limit: object = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-deposit-history

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种名称，如BTC
        depId             	String  	否       	充值记录 ID
        fromWdId          	String  	否       	内部转账发起者提币申请 ID如果该笔充值来自于内部转账，则该字段展示内部转账发起者的提币ID
        txId              	String  	否       	区块转账哈希记录
        type              	String  	否       	充值方式3：内部转账4：链上充值
        state             	String  	否       	充值状态0：等待确认1：确认到账2：充值成功8：因该币种暂停充值而未到账，恢复充值后自动到账11：命中地址黑名单12：账户或充值被冻结13：子账户充值拦截
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1654041600000
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1656633600000
        limit             	string  	否       	返回的结果集数量，默认为100，最大为100，不填默认返回100条
        '''
        return self.send_request(*_FundingEndpoints.get_deposit_history, **to_local(locals()))

    # 提币
    def set_withdrawal(self, ccy: str, amt: str, dest: str, toAddr: str, fee: str, chain: str = '', areaCode: str = '',
                       clientId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-withdrawal

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	是       	币种，如USDT
        amt               	String  	是       	数量
        dest              	String  	是       	提币方式3：内部转账4：链上提币
        toAddr            	String  	是       	如果选择链上提币，toAddr必须是认证过的数字货币地址。某些数字货币地址格式为地址:标签，如ARDOR-7JF3-8F2E-QUWZ-CAN7F:123456如果选择内部转账，toAddr必须是接收方地址，可以是邮箱、手机或者账户名。
        fee               	String  	是       	网络手续费≥0，提币到数字货币地址所需网络手续费可通过获取币种列表接口查询
        chain             	String  	可选      	币种链信息如USDT下有USDT-ERC20，USDT-TRC20，USDT-Omni多个链如果没有不填此参数，则默认为主链
        areaCode          	String  	可选      	手机区号当toAddr为手机号时，该参数必填
        clientId          	String  	否       	客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        '''
        return self.send_request(*_FundingEndpoints.set_withdrawal, **to_local(locals()))

    # 闪电网络提币
    def set_withdrawal_lightning(self, ccy: str, invoice: str, memo: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-lightning-withdrawals

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	是       	币种，如BTC
        invoice           	String  	是       	invoice 号码
        memo              	String  	否       	闪电网络提币的备注
        '''
        return self.send_request(*_FundingEndpoints.set_withdrawal_lightning, **to_local(locals()))

    # 撤销提币
    def set_cancel_withdrawal(self, wdId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-cancel-withdrawal

        请求参数：
        Parameter         	Type    	Required	Description
        wdId              	String  	是       	提币申请ID
        '''
        return self.send_request(*_FundingEndpoints.set_cancel_withdrawal, **to_local(locals()))

    # 获取提币记录
    def get_withdrawal_history(self, ccy: str = '', wdId: str = '', clientId: str = '', txId: str = '', type: str = '',
                               state: str = '', after: str = '', before: str = '', limit: object = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-withdrawal-history

        请求参数：
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
        '''
        return self.send_request(*_FundingEndpoints.get_withdrawal_history, **to_local(locals()))

    # 获取充值/提现的详细状态
    def get_deposit_withdraw_status(self, wdId: str = '', txId: str = '', ccy: str = '', to: str = '', chain: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-deposit-withdraw-status

        请求参数：
        Parameter         	Type    	Required	Description
        wdId              	String  	可选      	提币申请ID，用于查询资金提现wdId与txId必传其一也仅可传其一
        txId              	String  	可选      	区块转账哈希记录ID，用于查询资金充值wdId与txId必传其一也仅可传其一
        ccy               	String  	可选      	币种，如USDT查询充值时必填，需要与txId一并提供
        to                	String  	可选      	资金充值到账账户地址查询充值时必填，需要与txId一并提供
        chain             	String  	可选      	币种链信息，例如 USDT-ERC20查询充值时必填，需要与txId一并提供
        '''
        return self.send_request(*_FundingEndpoints.get_deposit_withdraw_status, **to_local(locals()))

    # 小额资产兑换
    def set_convert_dust_assets(self, ccy: object):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-small-assets-convert

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	Array   	是       	需要转换的币种资产
        '''
        return self.send_request(*_FundingEndpoints.set_convert_dust_assets, **to_local(locals()))

    # 获取余币宝余额
    def get_saving_balance(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-saving-balance

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC
        '''
        return self.send_request(*_FundingEndpoints.get_saving_balance, **to_local(locals()))

    # 余币宝申购/赎回
    def set_purchase_redempt(self, ccy: str, amt: str, side: str, rate: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-savings-purchase-redemption

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	是       	币种名称，如BTC
        amt               	String  	是       	申购/赎回 数量
        side              	String  	是       	操作类型purchase：申购redempt：赎回
        rate              	String  	是       	申购年利率仅适用于申购，新申购的利率会覆盖上次申购的利率参数取值范围在1%到365%之间
        '''
        return self.send_request(*_FundingEndpoints.set_purchase_redempt, **to_local(locals()))

    # 设置余币宝借贷利率
    def set_lending_rate(self, ccy: str, rate: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-set-lending-rate

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	是       	币种名称，如BTC
        rate              	String  	是       	贷出利率参数取值范围在1%到365%之间
        '''
        return self.send_request(*_FundingEndpoints.set_lending_rate, **to_local(locals()))

    # 获取余币宝出借明细
    def get_lending_history(self, ccy: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-lending-history

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为 100，不填默认返回 100 条
        '''
        return self.send_request(*_FundingEndpoints.get_lending_history, **to_local(locals()))

    # 获取市场借贷信息（公共）
    def get_lending_rate_summary(self, ccy: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-public-borrow-info-public

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC
        '''
        return self.send_request(*_FundingEndpoints.get_lending_rate_summary, **to_local(locals()))

    # 获取市场借贷历史（公共）
    def get_lending_rate_history(self, ccy: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-funding-get-public-borrow-history-public

        请求参数：
        Parameter         	Type    	Required	Description
        ccy               	String  	否       	币种，如BTC
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_FundingEndpoints.get_lending_rate_history, **to_local(locals()))

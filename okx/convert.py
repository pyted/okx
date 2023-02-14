from paux.param import to_local
from okx._client import Client


class _ConvertEndpoints:
    get_currencies = ['/api/v5/asset/convert/currencies', 'GET']  # 获取闪兑币种列表
    get_currency_pair = ['/api/v5/asset/convert/currency-pair', 'GET']  # 获取闪兑币对信息
    set_estimate_quote = ['/api/v5/asset/convert/estimate-quote', 'POST']  # 闪兑预估询价
    set_trade = ['/api/v5/asset/convert/trade', 'POST']  # 闪兑交易
    get_history = ['/api/v5/asset/convert/history', 'GET']  # 获取闪兑交易历史


class Convert(Client):
    # 获取闪兑币种列表
    def get_currencies(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-convert-get-convert-currencies
        '''
        return self.send_request(*_ConvertEndpoints.get_currencies, **to_local(locals()))

    # 获取闪兑币对信息
    def get_currency_pair(self, fromCcy: str, toCcy: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-convert-get-convert-currency-pair

        请求参数：
        Parameter         	Type    	Required	Description
        fromCcy           	String  	是       	消耗币种，如USDT
        toCcy             	String  	是       	获取币种，如BTC
        '''
        return self.send_request(*_ConvertEndpoints.get_currency_pair, **to_local(locals()))

    # 闪兑预估询价
    def set_estimate_quote(self, baseCcy: str, quoteCcy: str, side: str, rfqSz: str, rfqSzCcy: str, clQReqId: str = '',
                           tag: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-convert-estimate-quote

        请求参数：
        Parameter         	Type    	Required	Description
        baseCcy           	String  	是       	交易货币币种，如BTC-USDT中的BTC
        quoteCcy          	String  	是       	计价货币币种，如BTC-USDT中的USDT
        side              	String  	是       	交易方向买：buy卖：sell描述的是对于baseCcy的交易方向
        rfqSz             	String  	是       	询价数量
        rfqSzCcy          	String  	是       	询价币种
        clQReqId          	String  	否       	客户端自定义的订单标识字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签适用于broker用户
        '''
        return self.send_request(*_ConvertEndpoints.set_estimate_quote, **to_local(locals()))

    # 闪兑交易
    def set_trade(self, quoteId: str, baseCcy: str, quoteCcy: str, side: str, sz: str, szCcy: str, clTReqId: str = '',
                  tag: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-convert-convert-trade

        请求参数：
        Parameter         	Type    	Required	Description
        quoteId           	String  	是       	报价ID
        baseCcy           	String  	是       	交易货币币种，如BTC-USDT中的BTC
        quoteCcy          	String  	是       	计价货币币种，如BTC-USDT中的USDT
        side              	String  	是       	交易方向买：buy卖：sell描述的是对于baseCcy的交易方向
        sz                	String  	是       	用户报价数量报价数量应不大于预估询价中的询价数量
        szCcy             	String  	是       	用户报价币种
        clTReqId          	String  	否       	用户自定义的订单标识字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
        tag               	String  	否       	订单标签适用于broker用户
        '''
        return self.send_request(*_ConvertEndpoints.set_trade, **to_local(locals()))

    # 获取闪兑交易历史
    def get_history(self, after: str = '', before: str = '', limit: str = '', tag: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-convert-get-convert-history

        请求参数：
        Parameter         	Type    	Required	Description
        after             	String  	否       	查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        before            	String  	否       	查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085
        limit             	String  	否       	返回的结果集数量，默认为100，最大为100
        tag               	String  	否       	订单标签适用于broker用户
        '''
        return self.send_request(*_ConvertEndpoints.get_history, **to_local(locals()))

'''
行情数据
https://www.okx.com/docs-v5/zh/#order-book-trading-market-data
'''
from paux.param import to_local
from okx.api._client import Client


class _MarketEndpoints():
    get_tickers = ['/api/v5/market/tickers', 'GET']  # GET / 获取所有产品行情信息
    get_ticker = ['/api/v5/market/ticker', 'GET']  # GET / 获取单个产品行情信息
    get_books = ['/api/v5/market/books', 'GET']  # GET / 获取产品深度
    get_books_lite = ['/api/v5/market/books-lite', 'GET']  # GET / 获取产品轻量深度
    get_candles = ['/api/v5/market/candles', 'GET']  # GET / 获取交易产品K线数据
    get_history_candles = ['/api/v5/market/history-candles', 'GET']  # GET / 获取交易产品历史K线数据
    get_trades = ['/api/v5/market/trades', 'GET']  # GET / 获取交易产品公共成交数据
    get_history_trades = ['/api/v5/market/history-trades', 'GET']  # GET / 获取交易产品公共历史成交数据
    get_instrument_family_trades = ['/api/v5/market/option/instrument-family-trades', 'GET']  # GET / 获取期权品种公共成交数据
    get_option_trades = ['/api/v5/public/option-trades', 'GET']  # GET / 获取期权公共成交数据
    get_platform_24_volume = ['/api/v5/market/platform-24-volume', 'GET']  # GET / 获取平台24小时总成交量


class Market(Client):

    # GET / 获取所有产品行情信息
    def get_tickers(self, instType: str, uly: str = '', instFamily: str = '', proxies={}, proxy_host: str = None):
        '''
        获取产品行情信息
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-tickers
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instType          	String  	是       	产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数适用于交割/永续/期权，如BTC-USD
        instFamily        	String  	否       	交易品种适用于交割/永续/期权，如BTC-USD
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品ID
        last              	String  	最新成交价
        lastSz            	String  	最新成交的数量
        askPx             	String  	卖一价
        askSz             	String  	卖一价的挂单数数量
        bidPx             	String  	买一价
        bidSz             	String  	买一价的挂单数量
        open24h           	String  	24小时开盘价
        high24h           	String  	24小时最高价
        low24h            	String  	24小时最低价
        volCcy24h         	String  	24小时成交量，以币为单位如果是衍生品合约，数值为交易货币的数量。如果是币币/币币杠杆，数值为计价货币的数量。
        vol24h            	String  	24小时成交量，以张为单位如果是衍生品合约，数值为合约的张数。如果是币币/币币杠杆，数值为交易货币的数量。
        sodUtc0           	String  	UTC 0  时开盘价
        sodUtc8           	String  	UTC+8 时开盘价
        ts                	String  	ticker数据产生时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_MarketEndpoints.get_tickers, **to_local(locals()))

    # GET / 获取单个产品行情信息
    def get_ticker(self, instId: str, proxies={}, proxy_host: str = None):
        '''
        获取产品行情信息
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-ticker
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-SWAP
        返回参数:
        Parameter         	Type    	Description
        instType          	String  	产品类型
        instId            	String  	产品ID
        last              	String  	最新成交价
        lastSz            	String  	最新成交的数量
        askPx             	String  	卖一价
        askSz             	String  	卖一价对应的数量
        bidPx             	String  	买一价
        bidSz             	String  	买一价对应的数量
        open24h           	String  	24小时开盘价
        high24h           	String  	24小时最高价
        low24h            	String  	24小时最低价
        volCcy24h         	String  	24小时成交量，以币为单位如果是衍生品合约，数值为交易货币的数量。如果是币币/币币杠杆，数值为计价货币的数量。
        vol24h            	String  	24小时成交量，以张为单位如果是衍生品合约，数值为合约的张数。如果是币币/币币杠杆，数值为交易货币的数量。
        sodUtc0           	String  	UTC 0  时开盘价
        sodUtc8           	String  	UTC+8 时开盘价
        ts                	String  	ticker数据产生时间，Unix时间戳的毫秒数格式，如1597026383085
        '''
        return self.send_request(*_MarketEndpoints.get_ticker, **to_local(locals()))

    # GET / 获取产品深度
    def get_books(self, instId: str, sz: str = '', proxies={}, proxy_host: str = None):
        '''
        获取产品深度列表
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-order-book
        
        限速：40次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT
        sz                	String  	否       	深度档位数量，最大值可传400，即买卖深度共800条不填写此参数，默认返回1档深度数据
        返回参数:
        Parameter         	Type    	Description
        asks              	Array   	卖方深度
        bids              	Array   	买方深度
        ts                	String  	深度产生的时间
        '''
        return self.send_request(*_MarketEndpoints.get_books, **to_local(locals()))

    # GET / 获取产品轻量深度
    def get_books_lite(self, instId: str, proxies={}, proxy_host: str = None):
        '''
        可以更快地获取前25档的深度信息。
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-order-lite-book
        
        限速：6次/1s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT
        返回参数:
        Parameter         	Type    	Description
        asks              	Array   	卖方深度
        bids              	Array   	买方深度
        ts                	String  	深度产生的时间
        '''
        return self.send_request(*_MarketEndpoints.get_books_lite, **to_local(locals()))

    # GET / 获取交易产品K线数据
    def get_candles(self, instId: str, bar: str = '', after: str = '', before: str = '', limit: str = '', proxies={},
                    proxy_host: str = None):
        '''
        获取K线数据。K线数据按请求的粒度分组返回，K线数据每个粒度最多可获取最近1,440条。
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-candlesticks
        
        限速：40次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-190927-5000-C
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts, 单独使用时，会返回最新的数据。
        limit             	String  	否       	分页返回的结果集数量，最大为300，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	开始时间，Unix时间戳的毫秒数格式，如1597026383085
        o                 	String  	开盘价格
        h                 	String  	最高价格
        l                 	String  	最低价格
        c                 	String  	收盘价格
        vol               	String  	交易量，以张为单位如果是衍生品合约，数值为合约的张数。如果是币币/币币杠杆，数值为交易货币的数量。
        volCcy            	String  	交易量，以币为单位如果是衍生品合约，数值为交易货币的数量。如果是币币/币币杠杆，数值为计价货币的数量。
        volCcyQuote       	String  	交易量，以计价货币为单位如：BTC-USDT 和 BTC-USDT-SWAP, 单位均是 USDT；BTC-USD-SWAP 单位是 USD
        confirm           	String  	K线状态0代表 K 线未完结，1代表 K 线已完结。
        '''
        return self.send_request(*_MarketEndpoints.get_candles, **to_local(locals()))

    # GET / 获取交易产品历史K线数据
    def get_history_candles(self, instId: str, after: str = '', before: str = '', bar: str = '', limit: str = '',
                            proxies={}, proxy_host: str = None):
        '''
        获取最近几年的历史k线数据(1s k线支持查询最近3个月的数据)
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-candlesticks-history
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USD-200927
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts, 单独使用时，会返回最新的数据。
        bar               	String  	否       	时间粒度，默认值1m如 [1s/1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        ts                	String  	开始时间，Unix时间戳的毫秒数格式，如1597026383085
        o                 	String  	开盘价格
        h                 	String  	最高价格
        l                 	String  	最低价格
        c                 	String  	收盘价格
        vol               	String  	交易量，以张为单位如果是衍生品合约，数值为合约的张数。如果是币币/币币杠杆，数值为交易货币的数量。
        volCcy            	String  	交易量，以币为单位如果是衍生品合约，数值为交易货币的数量。如果是币币/币币杠杆，数值为计价货币的数量。
        volCcyQuote       	String  	交易量，以计价货币为单位如：BTC-USDT 和 BTC-USDT-SWAP, 单位均是 USDT；BTC-USD-SWAP 单位是 USD
        confirm           	String  	K线状态0代表 K 线未完结，1代表 K 线已完结。
        '''
        return self.send_request(*_MarketEndpoints.get_history_candles, **to_local(locals()))

    # GET / 获取交易产品公共成交数据
    def get_trades(self, instId: str, limit: str = '', proxies={}, proxy_host: str = None):
        '''
        查询市场上的成交信息数据
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-trades
        
        限速：100次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT
        limit             	String  	否       	分页返回的结果集数量，最大为500，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        tradeId           	String  	成交ID
        px                	String  	成交价格
        sz                	String  	成交数量
        side              	String  	成交方向buy：买sell：卖
        ts                	String  	成交时间，Unix时间戳的毫秒数格式， 如1597026383085
        '''
        return self.send_request(*_MarketEndpoints.get_trades, **to_local(locals()))

    # GET / 获取交易产品公共历史成交数据
    def get_history_trades(self, instId: str, type: str = '', after: str = '', before: str = '', limit: str = '',
                           proxies={}, proxy_host: str = None):
        '''
        查询市场上的成交信息数据，可以分页获取最近3个月的数据。
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-trades-history
        
        限速：10次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	是       	产品ID，如BTC-USDT
        type              	String  	否       	分页类型1：tradeId 分页2：时间戳分页默认为1：tradeId 分页
        after             	String  	否       	请求此 ID 或 ts 之前的分页内容，传的值为对应接口的 tradeId 或 ts
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的 tradeId。不支持时间戳分页。单独使用时，会返回最新的数据。
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        tradeId           	String  	成交ID
        px                	String  	成交价格
        sz                	String  	成交数量
        side              	String  	成交方向buy：买sell：卖
        ts                	String  	成交时间，Unix时间戳的毫秒数格式， 如1597026383085
        '''
        return self.send_request(*_MarketEndpoints.get_history_trades, **to_local(locals()))

    # GET / 获取期权品种公共成交数据
    def get_instrument_family_trades(self, instFamily: str, proxies={}, proxy_host: str = None):
        '''
        查询期权同一个交易品种下的成交信息数据，最多返回100条。
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-option-trades-by-instrument-family
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instFamily        	String  	是       	交易品种，如 BTC-USD，适用于期权
        返回参数:
        Parameter         	Type    	Description
        vol24h            	String  	24小时成交量，以张为单位
        optType           	String  	期权类型，C：看涨期权P：看跌期权
        tradeInfo         	Array   	成交数据列表
        > instId          	String  	产品ID
        > tradeId         	String  	成交ID
        > px              	String  	成交价格
        > sz              	String  	成交数量
        > side            	String  	成交方向buy：买sell：卖
        > ts              	String  	成交时间，Unix时间戳的毫秒数格式， 如1597026383085
        '''
        return self.send_request(*_MarketEndpoints.get_instrument_family_trades, **to_local(locals()))

    # GET / 获取期权公共成交数据
    def get_option_trades(self, instId: str = '', instFamily: str = '', optType: str = '', proxies={},
                          proxy_host: str = None):
        '''
        最多返回最近的100条成交数据
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-option-trades
        
        限速：20次/2s
        限速规则：IP
    
        请求参数:
        Parameter         	Type    	Required	Description

        instId            	String  	可选      	产品ID，如 BTC-USD-221230-4000-C，instId和instFamily必须传一个，若传两个，以instId为主
        instFamily        	String  	可选      	交易品种，如 BTC-USD
        optType           	String  	否       	期权类型，C：看涨期权P：看跌期权
        返回参数:
        Parameter         	Type    	Description
        instId            	String  	产品ID
        instFamily        	String  	交易品种
        tradeId           	String  	成交ID
        px                	String  	成交价格
        sz                	String  	成交数量
        side              	String  	成交方向buy：买sell：卖
        optType           	String  	期权类型，C：看涨期权 P：看跌期权 ，仅适用于期权
        fillVol           	String  	成交时的隐含波动率（对应成交价格）
        fwdPx             	String  	成交时的远期价格
        idxPx             	String  	成交时的指数价格
        markPx            	String  	成交时的标记价格
        ts                	String  	成交时间，Unix时间戳的毫秒数格式， 如1597026383085
        '''
        return self.send_request(*_MarketEndpoints.get_option_trades, **to_local(locals()))

    # GET / 获取平台24小时总成交量
    def get_platform_24_volume(self, proxies={}, proxy_host: str = None):
        '''
        24小时成交量滚动计算
        https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-24h-total-volume
        
        限速：2次/2s
        限速规则：IP
    
        
        返回参数:
        Parameter         	Type    	Description
        volUsd            	String  	订单簿交易近24小时总成交量，以美元为单位
        volCny            	String  	订单簿交易近24小时总成交量，以人民币为单位
        ts                	String  	接口返回数据时间
        '''
        return self.send_request(*_MarketEndpoints.get_platform_24_volume, **to_local(locals()))

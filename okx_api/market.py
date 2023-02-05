from paux.param import to_local
from okx_api._client import Client


class _MarketEndpoints:
    get_tickers = ['/api/v5/market/tickers', 'GET']  # 获取所有产品行情信息
    get_ticker = ['/api/v5/market/ticker', 'GET']  # 获取单个产品行情信息
    get_index_tickers = ['/api/v5/market/index-tickers', 'GET']  # 获取指数行情
    get_books = ['/api/v5/market/books', 'GET']  # 获取产品深度
    get_books_lite = ['/api/v5/market/books-lite', 'GET']  # 获取产品轻量深度
    get_candles = ['/api/v5/market/candles', 'GET']  # 获取交易产品K线数据
    get_history_candles = ['/api/v5/market/history-candles', 'GET']  # 获取交易产品历史K线数据
    get_index_candles = ['/api/v5/market/index-candles', 'GET']  # 获取指数K线数据
    get_history_index_candles = ['/api/v5/market/history-index-candles', 'GET']  # 获取指数历史K线数据
    get_mark_price_candles = ['/api/v5/market/mark-price-candles', 'GET']  # 获取标记价格K线数据
    get_history_mark_price_candles = ['/api/v5/market/history-mark-price-candles', 'GET']  # 获取标记价格历史K线数据
    get_trades = ['/api/v5/market/trades', 'GET']  # 获取交易产品公共成交数据
    get_history_trades = ['/api/v5/market/history-trades', 'GET']  # 获取交易产品公共历史成交数据
    get_instrument_family_trades = ['/api/v5/market/option/instrument-family-trades', 'GET']  # 获取期权品种公共成交数据
    get_platform_24_volume = ['/api/v5/market/platform-24-volume', 'GET']  # 获取平台24小时总成交量
    get_open_oracle = ['/api/v5/market/open-oracle', 'GET']  # Oracle  上链交易数据
    get_exchange_rate = ['/api/v5/market/exchange-rate', 'GET']  # 获取法币汇率
    get_index_components = ['/api/v5/market/index-components', 'GET']  # 获取指数成分数据
    get_block_tickers = ['/api/v5/market/block-tickers', 'GET']  # 获取大宗交易所有产品行情信息
    get_block_ticker = ['/api/v5/market/block-ticker', 'GET']  # 获取大宗交易单个产品行情信息
    get_block_trades = ['/api/v5/market/block-trades', 'GET']  # 获取大宗交易公共成交数据


class Market(Client):
    # 获取所有产品行情信息
    def get_tickers(self, instType: str, uly: str = '', instFamily: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-tickers

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数适用于交割/永续/期权，如BTC-USD
        instFamily        	String  	否       	交易品种适用于交割/永续/期权，如BTC-USD
        '''
        return self.send_request(*_MarketEndpoints.get_tickers, **to_local(locals()))

    # 获取单个产品行情信息
    def get_ticker(self, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-ticker

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如 BTC-USD-SWAP
        '''
        return self.send_request(*_MarketEndpoints.get_ticker, **to_local(locals()))

    # 获取指数行情
    def get_index_tickers(self, quoteCcy: str = '', instId: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-index-tickers

        请求参数：
        Parameter         	Type    	Required	Description
        quoteCcy          	String  	可选      	指数计价单位， 目前只有USD/USDT/BTC为计价单位的指数，quoteCcy和instId必须填写一个
        instId            	String  	可选      	指数，如BTC-USD
        '''
        return self.send_request(*_MarketEndpoints.get_index_tickers, **to_local(locals()))

    # 获取产品深度
    def get_books(self, instId: str, sz: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-order-book

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT
        sz                	String  	否       	深度档位数量，最大值可传400，即买卖深度共800条不填写此参数，默认返回1档深度数据
        '''
        return self.send_request(*_MarketEndpoints.get_books, **to_local(locals()))

    # 获取产品轻量深度
    def get_books_lite(self, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-order-lite-book

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT
        '''
        return self.send_request(*_MarketEndpoints.get_books_lite, **to_local(locals()))

    # 获取交易产品K线数据
    def get_candles(self, instId: str, bar: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-candlesticks

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-190927-5000-C
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        limit             	String  	否       	分页返回的结果集数量，最大为300，不填默认返回100条
        '''
        return self.send_request(*_MarketEndpoints.get_candles, **to_local(locals()))

    # 获取交易产品历史K线数据
    def get_history_candles(self, instId: str, after: str = '', before: str = '', bar: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-candlesticks-history

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-200927
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_MarketEndpoints.get_history_candles, **to_local(locals()))

    # 获取指数K线数据
    def get_index_candles(self, instId: str, after: str = '', before: str = '', bar: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-index-candlesticks

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	现货指数，如BTC-USD
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M/3M]UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/1Wutc/1Mutc/3Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_MarketEndpoints.get_index_candles, **to_local(locals()))

    # 获取指数历史K线数据
    def get_history_index_candles(self, instId: str, after: str = '', before: str = '', bar: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-index-candlesticks-history

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	现货指数，如BTC-USD
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M]UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/1Wutc/1Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_MarketEndpoints.get_history_index_candles, **to_local(locals()))

    # 获取标记价格K线数据
    def get_mark_price_candles(self, instId: str, after: str = '', before: str = '', bar: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-mark-price-candlesticks

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-SWAP
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M/3M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/1Wutc/1Mutc/3Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_MarketEndpoints.get_mark_price_candles, **to_local(locals()))

    # 获取标记价格历史K线数据
    def get_history_mark_price_candles(self, instId: str, after: str = '', before: str = '', bar: str = '',
                                       limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-mark-price-candlesticks-history

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USD-SWAP
        after             	String  	否       	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
        before            	String  	否       	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
        bar               	String  	否       	时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/1Wutc/1Mutc]
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_MarketEndpoints.get_history_mark_price_candles, **to_local(locals()))

    # 获取交易产品公共成交数据
    def get_trades(self, instId: str, limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-trades

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT
        limit             	String  	否       	分页返回的结果集数量，最大为500，不填默认返回100条
        '''
        return self.send_request(*_MarketEndpoints.get_trades, **to_local(locals()))

    # 获取交易产品公共历史成交数据
    def get_history_trades(self, instId: str, type: str = '', after: str = '', before: str = '', limit: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-trades-history

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT
        type              	String  	否       	分页类型1：tradeId 分页2：时间戳分页默认为1：tradeId 分页
        after             	String  	否       	请求此 ID 或 ts 之前的分页内容，传的值为对应接口的 tradeId 或 ts
        before            	String  	否       	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的 tradeId。不支持时间戳分页。
        limit             	String  	否       	分页返回的结果集数量，最大为100，不填默认返回100条
        '''
        return self.send_request(*_MarketEndpoints.get_history_trades, **to_local(locals()))

    # 获取期权品种公共成交数据
    def get_instrument_family_trades(self, instFamily: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-option-trades

        请求参数：
        Parameter         	Type    	Required	Description
        instFamily        	String  	是       	交易品种，如 BTC-USD，适用于期权
        '''
        return self.send_request(*_MarketEndpoints.get_instrument_family_trades, **to_local(locals()))

    # 获取平台24小时总成交量
    def get_platform_24_volume(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-24h-total-volume
        '''
        return self.send_request(*_MarketEndpoints.get_platform_24_volume, **to_local(locals()))

    # Oracle  上链交易数据
    def get_open_oracle(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-oracle
        '''
        return self.send_request(*_MarketEndpoints.get_open_oracle, **to_local(locals()))

    # 获取法币汇率
    def get_exchange_rate(self, ):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-exchange-rate
        '''
        return self.send_request(*_MarketEndpoints.get_exchange_rate, **to_local(locals()))

    # 获取指数成分数据
    def get_index_components(self, index: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-index-components

        请求参数：
        Parameter         	Type    	Required	Description
        index             	String  	是       	指数，如BTC-USDT
        '''
        return self.send_request(*_MarketEndpoints.get_index_components, **to_local(locals()))

    # 获取大宗交易所有产品行情信息
    def get_block_tickers(self, instType: str, uly: str = '', instFamily: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-block-tickers

        请求参数：
        Parameter         	Type    	Required	Description
        instType          	String  	是       	产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约OPTION：期权
        uly               	String  	否       	标的指数适用于交割/永续/期权，如BTC-USD
        instFamily        	String  	否       	交易品种适用于交割/永续/期权，如BTC-USD
        '''
        return self.send_request(*_MarketEndpoints.get_block_tickers, **to_local(locals()))

    # 获取大宗交易单个产品行情信息
    def get_block_ticker(self, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-block-ticker

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如 BTC-USD-SWAP
        '''
        return self.send_request(*_MarketEndpoints.get_block_ticker, **to_local(locals()))

    # 获取大宗交易公共成交数据
    def get_block_trades(self, instId: str):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-block-trades

        请求参数：
        Parameter         	Type    	Required	Description
        instId            	String  	是       	产品ID，如BTC-USDT
        '''
        return self.send_request(*_MarketEndpoints.get_block_trades, **to_local(locals()))

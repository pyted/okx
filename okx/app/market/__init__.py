from okx.app.market.exchange_info import ExchangeInfo
from okx.app.market.ticker import Ticker
from okx.app.market.history_candle import HistoryCandle


class Market(ExchangeInfo, Ticker, HistoryCandle):
    pass


class MarketSPOT(Market):
    def __init__(
            self,
            key: str = '',
            secret: str = '',
            passphrase: str = '',
            timezone='Asia/Shanghai',
            proxies={},
            proxy_host: str = None,
    ):
        instType = 'SPOT'
        super(MarketSPOT, self).__init__(
            instType=instType,
            key=key,
            secret=secret,
            passphrase=passphrase,
            timezone=timezone,
            proxies=proxies,
            proxy_host=proxy_host,

        )


class MarketSWAP(Market):
    def __init__(
            self,
            key: str = '',
            secret: str = '',
            passphrase: str = '',
            timezone='Asia/Shanghai',
            proxies={},
            proxy_host: str = None,
    ):
        instType = 'SWAP'
        super(MarketSWAP, self).__init__(
            instType=instType,
            key=key,
            secret=secret,
            passphrase=passphrase,
            timezone=timezone,
            proxies=proxies,
            proxy_host=proxy_host,
        )

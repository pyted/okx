from okx.api.market import Market
from okx.api.public import Public


class MarketBase():
    def __init__(
            self,
            instType: str,
            key: str = '',
            secret: str = '',
            passphrase: str = '',
            flag: str = '0',
            timezone='Asia/Shanghai',
            proxies={},
            proxy_host: str = None,
    ):
        self.instType = instType.upper()

        self.marketAPI = Market(
            key=key,
            secret=secret,
            passphrase=passphrase,
            flag=flag,
            proxies=proxies,
            proxy_host=proxy_host,
        )
        self.publicAPI = Public(
            key=key,
            secret=secret,
            passphrase=passphrase,
            flag=flag,
            proxies=proxies,
            proxy_host=proxy_host,
        )
        self.timezone = timezone

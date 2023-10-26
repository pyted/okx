from okx.app.account import AccountSPOT
from okx.app.market import MarketSPOT
from okx.api import Trade as TradeAPI


class TradeBase():
    def __init__(
            self,
            key: str,
            secret: str,
            passphrase: str,
            timezone: str = 'Asia/Shanghai',
            account=None,
            market=None,
            proxies={},
            proxy_host: str = None,
    ):
        # SWAP账户
        if not account:
            self._account = AccountSPOT(key=key, secret=secret, passphrase=passphrase, proxies=proxies,
                                        proxy_host=proxy_host)
        else:
            self._account = account

        # SWAP行情
        if not market:
            self._market = MarketSPOT(key=key, secret=secret, passphrase=passphrase, timezone=timezone, proxies=proxies,
                                      proxy_host=proxy_host)
        else:
            self._market = market

        # 时区
        self.timezone = timezone
        # TRADE API
        FLAG = '0'
        self.api = TradeAPI(key=key, secret=secret, passphrase=passphrase, flag=FLAG, proxies=proxies,
                            proxy_host=proxy_host)

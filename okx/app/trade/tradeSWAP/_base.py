from okx.app.account import AccountSWAP
from okx.app.market import MarketSWAP
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
            self._account = AccountSWAP(key=key, secret=secret, passphrase=passphrase, proxies=proxies,
                                        proxy_host=proxy_host)
        else:
            self._account = account

        # SWAP行情
        if not market:
            self._market = MarketSWAP(key=key, secret=secret, passphrase=passphrase, timezone=timezone, proxies=proxies,
                                      proxy_host=proxy_host)
        else:
            self._market = market

        # 设置持仓方向
        set_position_mode_result = self._account.set_position_mode(
            posMode='long_short_mode'
        )
        if set_position_mode_result['code'] == '0':
            print('[SUCCESS] 设置持仓方式为双向持仓成功，posMode="long_short_mode"')
        else:
            print('[FAILURE] 设置持仓方式为双向持仓失败，请手动设置：posMode="long_short_mode"')

        # 时区
        self.timezone = timezone
        # TRADE API
        FLAG = '0'
        self.api = TradeAPI(key=key, secret=secret, passphrase=passphrase, flag=FLAG, proxies=proxies,
                            proxy_host=proxy_host)

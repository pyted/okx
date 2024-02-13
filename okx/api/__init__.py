from okx.api.account import Account  # 交易账户

# 撮合交易--------------------------------------------
from okx.api.trade import Trade  # 交易
from okx.api.algotrade import AlgoTrade  # 策略交易
from okx.api.gridtrade import GridTrade  # 网格交易
from okx.api.signalbottrade import SignalBotTrade  # 信号交易
from okx.api.recurringbuy import RecurringBuy  # 定投
from okx.api.copytrade import CopyTrade  # 跟单
from okx.api.market import Market  # 行情数据
# ---------------------------------------------------

from okx.api.blocktrade import BlockTrade  # 大宗交易
from okx.api.spreadtrade import SpreadTrade  # 价差交易
from okx.api.public import Public  # 公共数据
from okx.api.tradingstatistics import TradingStatistics  # 交易大数据
from okx.api.fundingaccount import FundingAccount  # 资金账户
from okx.api.subaccount import SubAccount  # 子账户

# 金融产品--------------------------------------------
from okx.api.earn import Earn  # 赚币
from okx.api.savings import Savings  # 余币宝
# ---------------------------------------------------

from okx.api.status import Status  # Status


class API():
    def __init__(
            self,
            key='',
            secret='',
            passphrase='',
            flag='0',
            proxies={},
            proxy_host: str = None,
            retry_num=50,
            retry_delay=0.1,
    ):
        self.account = Account(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 交易账户
        self.trade = Trade(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 交易
        self.algoTrade = AlgoTrade(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 策略交易
        self.gridTrade = GridTrade(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 网格交易
        self.signalBotTrade = SignalBotTrade(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 信号交易
        self.recurringBuy = RecurringBuy(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 定投
        self.copyTrade = CopyTrade(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 跟单
        self.market = Market(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 行情数据
        self.blockTrade = BlockTrade(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 大宗交易
        self.spreadTrade = SpreadTrade(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 价差交易
        self.public = Public(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # # 公共数据
        self.tradingStatistics = TradingStatistics(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 交易大数据
        self.fundingAccount = FundingAccount(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 资金账户
        self.subAccount = SubAccount(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 子账户
        self.earn = Earn(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 赚币
        self.savings = Savings(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # 余币宝
        self.status = Status(key=key,secret=secret,passphrase=passphrase,flag=flag,proxies=proxies,proxy_host=proxy_host,retry_num=retry_num,retry_delay=retry_delay,)  # Status


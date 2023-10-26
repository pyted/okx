import random
import datetime
import time
import numpy as np
import pendulum
from typing import Union
from paux import filter as _filter
from paux import log as _log
from paux import date as _date
from paux import thread as _thread
from candlelite.calculate import interval as _interval
from candlelite.crypto.okx_lite import OkxLite
from okx.app import code
from okx.app.market import Market
from okx.app import exception
from okx.app.candle_server.rule import CandleRule


class CandleServer():
    def __init__(self, instType: str, rule=CandleRule, proxies={}, proxy_host: str = None):
        # 规则
        self.rule = rule
        # 产品类型
        self.instType = instType.upper()
        # 行情客户端
        self.market = Market(
            instType=self.instType,
            key=self.rule.KEY,
            secret=self.rule.SECRET,
            passphrase=self.rule.PASSPHRASE,
            timezone=self.rule.TIMEZONE,
            proxies=proxies,
            proxy_host=proxy_host,
        )
        # 产品过滤器 用于candle_map的更新
        self.filter = _filter.Filter()
        # BinanceLite
        self.okxLite = OkxLite()
        self.okxLite.CANDLE_DATE_BASE_DIR = self.rule.CANDLE_DIR
        self.okxLite.CANDLE_FILE_BASE_DIR = self.rule.CACHE_DIR
        self.okxLite.TIMEZONE = self.rule.TIMEZONE
        # 日志
        self.log = _log.Log(
            log_dirpath=self.rule.LOG_DIRPATH,
            file_level=self.rule.LOG_FILE_LEVEL,
            console_level=self.rule.LOG_CONSOLE_LEVEL,
        )
        self.lite = self.okxLite
        self._run_candle_map_thread = None
        self.__close_run_candle_map_signal = False
        self._download_daily_thread = None
        self.__close_download_daily_thread = False

    # 获取过滤后的产品名称
    def get_instIds_filtered(self) -> dict:
        '''
        过滤内容：
            1. rule.INSTIDS_FILTER
            2. rule.INSTIDS_CONTAINS
            3. rule.INSTID_ENDSWITH
            4. CandleServer.filter
        '''
        # 验证self.instIds
        if not (
                self.rule.INSTIDS == 'all' or
                isinstance(self.rule.INSTIDS, list)
        ):
            msg = 'rule.INSTIDS must be "all" or list type'
            raise exception.RuleException(msg)
        # 产品为全部 self.rule.INSTIDS = 'all'
        if isinstance(self.rule.INSTIDS, str) and self.rule.INSTIDS.lower() == 'all':
            instIds_trading_result = self.market.get_instIds_trading_on(
                expire_seconds=60 * 60,  # 使用的缓存过期时间
            )
            if instIds_trading_result['code'] != '0':
                return instIds_trading_result
            instIds = instIds_trading_result['data']
        # 产品类型为列表
        else:
            instIds = self.rule.INSTIDS
        # 第一次过滤 使用rule中的条件 -> instIds_filtered1
        # INSTIDS_FILTER
        # INSTID_CONTAINS
        # INSTID_ENDSWITH
        instIds_filtered1 = []
        for instId in instIds:
            instId: str
            if self.rule.INSTIDS_FILTER and instId in self.rule.INSTIDS_FILTER:
                continue
            if self.rule.INSTID_CONTAINS and not self.rule.INSTID_CONTAINS in instId:
                continue
            if self.rule.INSTID_ENDSWITH and not instId.endswith(self.rule.INSTID_ENDSWITH):
                continue
            instIds_filtered1.append(instId)
        # 第二次过滤 self.filter 过滤数据不足，请求错误的instId -> instIds_filtered2
        instIds_filtered2 = []
        for instId in instIds_filtered1:
            instId: str
            if self.filter.check(instId):  # True 不过滤
                instIds_filtered2.append(instId)
        result = {'code': '0', 'data': instIds_filtered2, 'msg': ''}
        return result

    # 按照日期下载历史K线
    def download_candles_by_date(
            self,
            start: Union[str, int, float, datetime.date],
            end: Union[str, int, float, datetime.date, None] = None,
            replace=False,
    ):
        '''
        :param start: 起始日期
        :param end: 终止日期
            None 使用昨日日期
        :param replace: 是否替换本地文件
        '''
        # 执行下载使用的临时过滤器，过滤数据异常的产品
        self._download_filter = _filter.Filter()
        # 日期终点
        if not end:
            end = pendulum.yesterday(tz=self.rule.TIMEZONE)
        # 需要下载的日期序列
        date_range = _date.get_range_dates(start=start, end=end, timezone=self.rule.TIMEZONE)
        # 反转日期序列，用于加速
        date_range = sorted(date_range, reverse=True)
        # 按照日期下载
        for date in date_range:
            self.__download_candles_by_date(
                date=date,
                replace=replace,
            )
        # 删除临时过滤器
        del self._download_filter

    # 下载某一天多产品历史K线数据
    def __download_candles_by_date(
            self,
            date: Union[str, int, float, datetime.date],
            replace=False,
    ):
        '''
        :param date: 日期
        :param replace: 是否替换本地文件
        '''
        # 日期字符串，用于控制台打印
        if self.rule.TIMEZONE == 'America/New_York':
            date_str = _date.to_fmt(date, self.rule.TIMEZONE, '%d/%m/%Y')
        else:
            date_str = _date.to_fmt(date, self.rule.TIMEZONE, '%Y-%m-%d')
        # 获取产品列表
        get_instIds_filtered_result = self.get_instIds_filtered()
        # **[ERROR RAISE]** 产品列表有误
        if get_instIds_filtered_result['code'] != '0':
            msg = '[get_instIds_filtered] code={code} msg={msg}'.format(
                msg=get_instIds_filtered_result['msg'],
                code=get_instIds_filtered_result['code'],
            )
            self.log.error(msg)
            raise exception.CodeException(msg)
        instIds = get_instIds_filtered_result['data']
        # 过滤下载异常的产品
        instIds = [instId for instId in instIds if self._download_filter.check(instId)]
        # 产品逐个下载
        download_detail = {
            'all': len(instIds),  # 总数
            'skip': 0,  # 跳过的个数
            'suc': 0,  # 成功的个数
            'warn': 0,  # 警告的个数
            'error': 0,  # 失败的个数
        }
        for instId in instIds:
            # 不替换且存在数据
            if not replace and self.lite.check_candle_date_path(
                    instType=self.instType,
                    symbol=instId,
                    start=date,
                    end=date,
                    bar=self.rule.BAR,
            )['code']:
                download_detail['skip'] += 1
                continue
            # 按照日期下载数据
            get_history_candle_by_date_result = self.market.get_history_candle_by_date(
                instId=instId,
                date=date,
                bar=self.rule.BAR,
                valid_interval=True,
                valid_start=True,
                valid_end=True
            )
            # 下载状态码 this_code
            this_code = get_history_candle_by_date_result['code']
            # 下载异常
            if this_code != '0':
                msg = '[get_history_candle_by_date] code={code} instId={instId} date={date} bar={bar} msg={msg}'.format(
                    code=this_code,
                    instId=instId,
                    date=date_str,
                    bar=self.rule.BAR,
                    msg=get_history_candle_by_date_result['msg']
                )
                # info 长度问题与起始错误，数据不足，过滤
                if this_code in [code.CANDLE_LENGTH_ERROR[0], code.CANDLE_START_ERROR[0]]:
                    self._download_filter.set(name=instId, filter_minute=1440)
                    self.log.warn(msg)
                    download_detail['warn'] += 1
                # error 数据间隔错误 或者 终止时间 过滤
                elif this_code in [code.CANDLE_INTERVAL_ERROR[0], code.CANDLE_END_ERROR[0]]:
                    self._download_filter.set(name=instId, filter_minute=1440)
                    self.log.error(msg)
                    download_detail['error'] += 1
                # error 其他状态码错误 不过滤
                else:
                    self.log.error(msg)
            # 历史K线数据合规 保存
            else:
                candle = get_history_candle_by_date_result['data']
                self.lite.save_candle_by_date(
                    candle=candle,
                    instType=self.instType,
                    symbol=instId,
                    start=date,
                    end=date,
                    bar=self.rule.BAR,
                )
                msg = 'DOWNLOAD {instId:<10} {bar:<3} {date}'.format(
                    instId=instId,
                    bar=self.rule.BAR,
                    date=date_str,
                )
                self.log.info(msg)
                download_detail['suc'] += 1
            # pass
        msg = 'COMPLETE DOWNLOAD {date} (ALL:{all} SKIP:{skip} SUC:{suc} WARN:{warn} ERROR:{error})'.format(
            date=date_str,
            **download_detail,
        )
        self.log.info(msg)

    def prepare_candle_map(self):
        # 历史K线最新毫秒时间戳 -> latest_ts
        latest_ts_result = self.market.get_history_candle_latest_ts(bar=self.rule.BAR)
        # **[ERROR RAISE]** 获取失败
        if latest_ts_result['code'] != '0':
            msg = '[get_history_candle_latest] code={code} msg={msg}'.format(
                code=latest_ts_result['code'],
                msg=latest_ts_result['msg'],
            )
            raise exception.CodeException(msg)
        latest_ts = latest_ts_result['data']
        # start_ts
        start_ts = float(latest_ts - _interval.get_interval(bar=self.rule.BAR) * (self.rule.LENGTH - 1))
        # 本地date数据的起始日期start_date与终止日期end_date
        start_date = _date.to_datetime(date=start_ts, timezone=self.rule.TIMEZONE).date()
        end_date = pendulum.yesterday(tz=self.rule.TIMEZONE).date()
        # 产品 -> instIds
        get_instIds_filtered_result = self.get_instIds_filtered()
        # **[ERROR RAISE]** 获取失败
        if get_instIds_filtered_result['code'] != '0':
            msg = '[get_instIds_filtered] code={code} msg={msg}'.format(
                msg=get_instIds_filtered_result['msg'],
                code=get_instIds_filtered_result['code'],
            )
            self.log.error(msg)
            raise exception.CodeException(msg)
        instIds = get_instIds_filtered_result['data']
        # candle_map
        candle_map = {}
        # 逐个产品遍历
        for instId in instIds:
            # 是否有缓存
            if self.lite.check_candle_file_path(
                    instType=self.instType,
                    symbol=instId,
                    bar=self.rule.BAR,
            )['code']:
                # 尝试读取缓存
                try:
                    # 缓存数据
                    candle_cache = self.lite.load_candle_by_file(
                        instType=self.instType,
                        symbol=instId,
                        path=None,
                        bar=self.rule.BAR,
                        valid_interval=True,
                    )
                    # 按照时间截取
                    candle_cache_transformed = candle_cache[
                        (candle_cache[:, 0] >= start_ts) & (candle_cache[:, 0] <= latest_ts)
                        ]
                    # 如果截取后数据不为空，使用缓存
                    if candle_cache_transformed.shape[0] > 0:
                        candle_map[instId] = candle_cache_transformed
                        continue
                # 有缓存但读取失败 -> 继续尝试从date数据中读取
                except:
                    msg = f'[load_candle_by_file] instId={instId}'
                    self.log.error(msg)
            # 无缓存或者缓存文件读取失败
            # 是否有date数据
            if self.lite.check_candle_date_path(
                    instType=self.instType,
                    symbol=instId,
                    start=start_date,
                    end=end_date,
                    bar=self.rule.BAR,
            )['code']:
                # 尝试读取date数据
                try:
                    # date数据
                    candle_date = self.lite.load_candle_by_date(
                        instType=self.instType,
                        symbol=instId,
                        start=start_date,
                        end=end_date,
                        bar=self.rule.BAR,
                        valid_interval=True,
                        valid_start=True,
                        valid_end=True,
                    )
                    # 时间截取
                    candle_date_transformed = candle_date[
                        (candle_date[:, 0] >= start_ts) & (candle_date[:, 0] <= latest_ts)
                        ]
                    # 如果截取后数据不为空，使用此数据
                    if candle_date_transformed.shape[0] > 0:
                        candle_map[instId] = candle_date_transformed
                        continue
                # 有date数据但是读取失败
                except:
                    msg = '[load_candle_by_date] instId={instId} start_date={start_date} end_date={end_date}'.format(
                        instId=instId,
                        start_date=str(start_date),
                        end_date=str(end_date),
                    )
                    self.log.error(msg)
        # 连续两次将candle_map更新到最新
        for i in range(2):
            candle_map = self.update_candle(candle_map)
        return candle_map

    def update_candle(self, candle_map=None):
        # 优先级 candle_map >> self.candle_map
        if candle_map == None:
            if hasattr(self, 'candle_map'):
                candle_map = self.candle_map
            # [ERROR RAISE] 没有candle_map和self.candle_map
            else:
                msg = 'candle_map and self.candle_map can not be empty together'
                raise exception.ParamException(msg)
        # 历史K线最新毫秒时间戳 -> latest_ts
        latest_ts_result = self.market.get_history_candle_latest_ts(bar=self.rule.BAR)
        if latest_ts_result['code'] != '0':
            msg = '[get_history_candle_latest_ts] code={code} msg={msg}'.format(
                code=latest_ts_result['code'],
                msg=latest_ts_result['msg'],
            )
            raise exception.CodeException(msg)
        latest_ts = latest_ts_result['data']
        # 获取过滤后的产品 -> instIds
        get_instIds_filtered_result = self.get_instIds_filtered()
        if get_instIds_filtered_result['code'] != '0':
            msg = '[get_instIds_filtered] code={code} msg={msg}'.format(
                msg=get_instIds_filtered_result['msg'],
                code=get_instIds_filtered_result['code'],
            )
            self.log.error(msg)
            raise exception.CodeException(msg)
        instIds = get_instIds_filtered_result['data']
        # 逐个产品遍历
        for instId in instIds:
            candle = candle_map[instId] if instId in candle_map.keys() else None
            if isinstance(candle, np.ndarray) and candle.shape[0] > 0 and candle[-1, 0] == latest_ts:
                continue
            update_history_candle_result = self.market.update_history_candle(
                instId=instId,
                length=self.rule.LENGTH,
                candle=candle,
                end=latest_ts,
                bar=self.rule.BAR,
                valid_interval=True,
            )
            this_code = update_history_candle_result['code']
            if this_code != '0':
                msg = '[update_history_candle] code={code} instId={instId} msg={msg}'.format(
                    instId=instId,
                    code=this_code,
                    msg=update_history_candle_result['msg']
                )
                if this_code == code.CANDLE_LENGTH_ERROR[0]:
                    self.filter.set(name=instId, filter_minute=60 + random.randint(1, 10))
                    self.log.warn(msg)
                elif this_code == code.CANDLE_INTERVAL_ERROR[0]:
                    self.filter.set(name=instId, filter_minute=1440 + random.randint(1, 10))
                    self.log.error(msg)
                else:
                    self.log.error(msg)
                if instId in candle_map.keys():
                    del candle_map[instId]
            else:
                candle_map[instId] = update_history_candle_result['data']
        return candle_map

    # 多线程更新candle_map
    @_thread.thread_wrapper
    def thread_update_candle_map(self):
        while True:
            # 退出条件
            if self.__close_run_candle_map_signal == True:
                break
            # 更新数据
            try:
                if not hasattr(self, 'candle_map'):
                    self.candle_map = {}
                candle_map = self.update_candle(candle_map=self.candle_map)
                self.candle_map = candle_map
            except:
                msg = '[thread: update_candle]'
                self.log.error(msg)
            else:
                # 如果需要保存缓存
                if self.rule.CACHE_DELAY_SECONDS:
                    # 按时保存缓存
                    try:
                        # 没有上次缓存时间或者超过CACHE_DELAY_SECONDS
                        if (
                                (not hasattr(self, '__last_cache_candle_time'))
                                or
                                (time.time() - getattr(self,
                                                       '__last_cache_candle_time') >= self.rule.CACHE_DELAY_SECONDS)
                        ):
                            self.lite.save_candle_map_by_file(
                                candle_map=self.candle_map,
                                instType=self.instType,
                                symbols=[],
                                replace=True,
                                bar=self.rule.BAR,
                            )
                            setattr(self, '__last_cache_candle_time', time.time())
                            msg = 'DOWNLOAD CANDLE CACHE'
                            self.log.info(msg)
                    except:
                        msg = '[thread: save_candle_map_by_file]'
                        self.log.error(msg)
                # 如果需要每天下载date数据
                if self.rule.DOWNLOAD_TIME and pendulum.now(self.rule.TIMEZONE).time().strftime(
                        '%H:%M:%S') >= self.rule.DOWNLOAD_TIME:
                    try:
                        # 没有上次下载日期或者距离上次下载日期超过1天
                        if (
                                (not hasattr(self, '__last_download_candle_date'))
                                or
                                ((pendulum.now(tz=self.rule.TIMEZONE).date() - getattr(self,
                                                                                       '__last_download_candle_date')).days >= 1)
                        ):
                            self.lite.save_candle_map_by_date(
                                candle_map=self.candle_map,
                                instType=self.instType,
                                symbols=[],
                                replace=False,
                                start=pendulum.yesterday(tz=self.rule.TIMEZONE),
                                end=pendulum.yesterday(tz=self.rule.TIMEZONE),
                                bar=self.rule.BAR,
                            )
                            setattr(self, '__last_download_candle_date', pendulum.now(tz=self.rule.TIMEZONE).date())
                            msg = 'DOWNLOAD CANDLE BY DATE'
                            self.log.info(msg)
                    except:
                        msg = '[thread: save_candle_map_by_date]'
                        self.log.error(msg)
            finally:
                time.sleep(self.rule.UPDATE_INTERVAL_SECONDS)
        self.__close_run_candle_map_signal = False

    # 运行服务
    def run_candle_map(self):
        # 有正在运行的run线程
        if self._run_candle_map_thread and self._run_candle_map_thread.isAlive():
            msg = 'Server run thread is running. Cannot run repeatedly.'
            print(msg)
            return None
        # 补充date数据
        if self.rule.LOCAL_CANDLE_DAYS:
            self.download_candles_by_date(
                start=pendulum.now(tz=self.rule.TIMEZONE) - datetime.timedelta(days=self.rule.LOCAL_CANDLE_DAYS),
                end=pendulum.yesterday(tz=self.rule.TIMEZONE),
            )
        # 准备candle_map
        self.candle_map = self.prepare_candle_map()
        msg = 'COMPLETE PREPARE candle_map'
        self.log.info(msg)
        # 多线程更新candle_map
        t = self.thread_update_candle_map()
        self._run_candle_map_thread = t
        time.sleep(1)

    def close_run_candle_map(self):
        if self._run_candle_map_thread:
            self.__close_run_candle_map_signal = True
        else:
            msg = 'run_candle_map is not running'
            print(msg)

    def close_download_daily(self):
        if self._download_daily_thread:
            self.__close_download_daily_thread = True
        else:
            msg = 'download_daily is not running'
            print(msg)

    # 每天定时下载以天为单位的历史数据
    @_thread.thread_wrapper
    def _download_daily(
            self,
            start: Union[str, int, float, datetime.date, None] = None,
            replace: bool = False
    ):
        # 下载补充数据
        yesterday = pendulum.yesterday(tz=self.rule.TIMEZONE)
        last_day = yesterday
        # 如果有start 下载start ~ yesterday的数据
        if start == None:
            start = yesterday
        self.download_candles_by_date(start=start, end=yesterday, replace=replace)
        while True:
            if self.__close_download_daily_thread == True:
                break
            time.sleep(0.5)
            # 下载的时间条件
            if not pendulum.now(tz=self.rule.TIMEZONE).time().strftime('%H:%M:%S') >= self.rule.DOWNLOAD_TIME:
                continue
            # 下载的日期条件
            yesterday = pendulum.yesterday(tz=self.rule.TIMEZONE)
            if (yesterday - last_day).days > 0:
                self.download_candles_by_date(
                    start=yesterday,
                    end=yesterday,
                )
                last_day = yesterday
        self.__close_download_daily_thread = False

    def download_daily(self,
                       start: Union[str, int, float, datetime.date, None] = None,
                       replace: bool = False
                       ):
        '''
        :param start: 起始日期
            start != None 补充下载start ~ yesterday 的历史K线数据
        :param replace: 是否替换本地数据
        '''
        if self._download_daily_thread and self._download_daily_thread.isAlive():
            msg = 'Server download daily thread is running. Cannot run repeatedly.'
            print(msg)
            return None
        t = self._download_daily(start=start, replace=replace)
        self._download_daily_thread = t
        time.sleep(1)

    # 获得candle的最新时间与当前时间查小于security_seconds的k线数据
    def get_candle_security(self, instId: str, security_seconds=60 * 3) -> np.ndarray:
        '''
        :param instId: 产品
        :param security_seconds: 与当前时间戳相差多少以内判定为安全
        '''
        # 不存在
        if instId not in self.candle_map.keys():
            return np.array([])
        candle = self.candle_map[instId]
        # 是否与此时时间相差超过了security_seconds
        if (time.time() * 1000 - candle[-1, 0]) >= security_seconds * 1000:
            return np.array([])
        return candle

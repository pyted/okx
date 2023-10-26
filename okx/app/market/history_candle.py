import time
import datetime
import pendulum
import pandas as pd
import numpy as np
import paux.date as _date
from typing import Union
from okx.app import code
from okx.app.market._base import MarketBase
from okx.app.market import utils
from candlelite.calculate import valid as _valid
from candlelite.calculate import transform as _transform
from candlelite.calculate import interval as _interval

__all__ = ['HistoryCandle']


# 历史K线
class HistoryCandle(MarketBase):
    # 将API返回的原始历史K线数据列表转换为np.array类型
    def __candle_list_to_candle(
            self,
            instId: str,
            candle_list: list,
            start: Union[int, float, str, datetime.date, datetime.datetime, None],
            end: Union[int, float, str, datetime.date, datetime.datetime, None],
            bar: str = '1m',
            valid_interval: bool = True,
            valid_start: bool = True,
            valid_end: bool = True
    ) -> dict:
        '''
        :param instId: 产品
        :param candle_list: API返回的K线数据列表
        :param start: 起始时间
        :param end: 终止时间
            start和end可以为None，如果存在数据，会截取[start,end]的数据
            例如：
                start == None end != None
                    -> ts <= end
                start != None end == None
                    -> ts >= start
                start != None end != None
                    -> start <= ts <= end
        :param bar: 时间粒度
        :param valid_interval: 是否验证时间间隔
        :param valid_start: 是否验证时间起点 start必须存在
        :param valid_end: 是否验证时间终点 end必须存在
        '''
        # 转换DataFrame
        df = pd.DataFrame(candle_list).astype(float)
        # [ERROR RETURN] 数据为空
        if not df.shape[0]:
            result = {
                'code': code.CANDLE_LENGTH_ERROR[0],
                'data': np.array([]),
                'msg': 'Candle empty {instId} {start} ~ {end}'.format(
                    instId=str(instId),
                    start=_date.to_fmt(date=start, timezone=self.timezone) if start else 'None',
                    end=_date.to_fmt(date=end, timezone=self.timezone) if end else 'None',
                ),
            }
            return result
        # 按照时间戳去重
        ts_column = df.columns.tolist()[0]
        df[ts_column] = df[ts_column].astype(int)
        df = df.drop_duplicates(subset=ts_column)
        # 按照start和end截取数据
        if start and end:
            df = df[
                (df[ts_column] <= _date.to_ts(end, timezone=self.timezone)) &
                (df[ts_column] >= _date.to_ts(start, timezone=self.timezone))
                ]
        elif start and not end:
            df = df[df[ts_column] >= _date.to_ts(start, timezone=self.timezone)]
        elif end and not start:
            df = df[df[ts_column] <= _date.to_ts(end, timezone=self.timezone)]
        # 排序
        df = df.sort_values(by=ts_column)
        # 转化为array
        candle = df.to_numpy()
        # 验证时间起点
        if valid_start:
            valid_start_result = _valid.valid_start(candle=candle, start=start, timezone=self.timezone)
            # [ERROR RETURN] 时间起点错误
            if not valid_start_result['code']:
                return {
                    'code': code.CANDLE_START_ERROR[0],
                    'data': candle,
                    'msg': str(instId) + valid_start_result['msg']
                }
        # 验证时间终点
        if valid_end:
            valid_end_result = _valid.valid_end(candle=candle, end=end, timezone=self.timezone)
            # [ERROR RETURN] 时间终点错误
            if not valid_end_result['code']:
                return {
                    'code': code.CANDLE_END_ERROR[0],
                    'data': candle,
                    'msg': str(instId) + valid_end_result['msg'],
                }

        # 验证时间间隔
        if valid_interval:
            valid_interval_result = _valid.valid_interval(candle=candle, interval=_interval.get_interval(bar))
            # [ERROR RETURN] 时间间隔错误
            if not valid_interval_result['code']:
                return {
                    'code': code.CANDLE_INTERVAL_ERROR[0],
                    'data': candle,
                    'msg': str(instId) + valid_interval_result['msg'],
                }
        # [RETURN]
        result = {'code': '0', 'data': candle, 'msg': ''}
        return result

    # 获取产品的历史K线数据
    # Weight >= 1 (智能节约权重)
    def get_history_candle(
            self,
            instId: str,
            start: Union[str, int, float, datetime.datetime, datetime.date],
            end: Union[str, int, float, datetime.datetime, datetime.date],
            bar: str = '1m',
            valid_interval: bool = True,
            valid_start: bool = True,
            valid_end: bool = True
    ) -> dict:
        '''
        :param instId: 产品
        :param start: 起始日期时间
        :param end: 起始日期时间
        :param bar: 时间粒度
        :param valid_interval: 是否验证时间间隔
        :param valid_start: 是否验证起始时间
        :param valid_end: 是否验证终止时间

        okx 底层API不会包含before（start）和after（end）时刻的数据
        '''
        # 起始与终止时间戳
        start_ts = _date.to_ts(date=start, timezone=self.timezone)
        end_ts = _date.to_ts(date=end, timezone=self.timezone)
        # 时间间隔
        bar_interval = _interval.get_interval(bar=bar)
        # 初始化起始时间和candle列表
        before_ts = start_ts
        candle_list = []
        while True:
            # 计算limit
            limit = self._get_limit(num=(end_ts - before_ts) / bar_interval + 1)
            # 获取K线数据
            result = self.marketAPI.get_history_candles(
                instId=instId,
                before=before_ts - 1,
                after=before_ts + (limit - 1) * bar_interval + 1,
                bar=bar,
                limit=limit,
            )
            # [ERROR RETURN] K线数据错误
            if result['code'] != '0':
                return result
            # [BREAK] 数据为空
            if not result['data']:
                break
            # 保存candle
            candle_list += result['data']
            # 跳过上一次的endTime，上一次的endTime=before_ts + (limit - 1) * bar_interval
            before_ts = before_ts + limit * bar_interval
            # [BREAK] 完成
            if before_ts > end_ts:
                break
        # 转换为candle
        result = self.__candle_list_to_candle(
            instId=instId,
            candle_list=candle_list,
            start=start,
            end=end,
            bar=bar,
            valid_interval=valid_interval,
            valid_start=valid_start,
            valid_end=valid_end,
        )
        # [RETURN]
        return result

    # 获取产品指定数量的最新历史K线数据
    # Weight > 1 (智能节约权重)
    def get_history_candle_latest(
            self,
            instId: str,
            length: int,
            end: Union[str, int, float, datetime.date, datetime.datetime, None] = None,
            bar: str = '1m',
            valid_interval: bool = True,
    ) -> dict:
        '''
        :param instId: 合约产品
        :param length: K线长度
        :param end: 终止日期时间
            支持: 毫秒时间戳、日期格式的字符串、日期时间对象与日期对象 -> 自动验证数据终点
            None: 取当前时间 -> 不验证时间终点
        :param bar: 时间粒度
        :param valid_interval: 是否验证时间间隔
        '''
        # 时间终止
        if not end:
            end_ts = int(time.time() * 1000)
        else:
            end_ts = _date.to_ts(date=end, timezone=self.timezone)
        # 时间间隔
        bar_interval = _interval.get_interval(bar)
        # 从后向前获取candle
        after_ts = end_ts
        candle_list = []
        while True:
            # 计算limit
            limit = self._get_limit(num=length - len(candle_list))
            # 获取K线数据
            result = self.marketAPI.get_history_candles(
                instId=instId,
                before=after_ts - (limit - 1) * bar_interval - 1,
                after=after_ts + 1,
                bar=bar,
                limit=limit,
            )
            # [ERROR RETURN] 数据错误
            if result['code'] != '0':
                return result
            # [BREAK] 数据为空
            if not result['data']:
                break
            # 添加
            candle_list += result['data']
            # [BREAK] 完成
            if len(candle_list) >= length:
                break
            # 计算下一个的终止时间
            after_ts = int(candle_list[-1][0]) - bar_interval
        # 转换为np.array
        result = self.__candle_list_to_candle(
            instId=instId,
            candle_list=candle_list,
            start=None,
            end=end,
            bar=bar,
            valid_interval=valid_interval,
            valid_start=False,
            valid_end=True if end != None else False,  # 是否验证终止时间
        )
        # [ERROR RETURN] 转换失败
        if result['code'] != '0':
            return result
        # 取后length行数据
        candle = result['data'][-length:]
        # 验证数据长度
        valid_length_result = _valid.valid_length(candle=candle, length=length)
        # [ERROR RETURN] 数据长度错误
        if not valid_length_result['code']:
            return {
                'code': code.CANDLE_LENGTH_ERROR[0],
                'data': candle,
                'msg': str(instId) + valid_length_result['msg']
            }
        # [RETURN]
        result['data'] = candle
        return result

    # 获取产品指定日期的历史K线数据
    # Weight: 1 ~ 10 (智能节约权重)
    def get_history_candle_by_date(
            self,
            instId: str,
            date: Union[str, int, float, datetime.date],
            bar: str = '1m',
            valid_interval: bool = True,
            valid_start: bool = True,
            valid_end: bool = True
    ) -> dict:
        '''
        :param instId: 产品
        :param date: 日期
        :param bar: 时间粒度
        :param valid_interval: 是否验证时间间隔
        :param valid_start: 是否验证起始时间
        :param valid_end: 是否验证终止时间
        '''
        # 日期时间对象，其中小时分钟秒均为0
        date = _date.to_datetime(date=date, timezone=self.timezone)
        # 起始毫秒时间戳
        start = int(date.timestamp() * 1000)
        bar_interval = _interval.get_interval(bar)
        # 终止毫秒时间戳
        end_date = datetime.date(year=date.year, month=date.month, day=date.day) + datetime.timedelta(days=1)
        end_date = pendulum.datetime(
            year=end_date.year,
            month=end_date.month,
            day=end_date.day,
            hour=0,
            minute=0,
            second=0,
            tz=self.timezone,
        )
        end = int(end_date.timestamp() * 1000 - 1 * bar_interval)
        # [RETURN]
        return self.get_history_candle(
            instId=instId,
            start=start,
            bar=bar,
            end=end,
            valid_interval=valid_interval,
            valid_start=valid_start,
            valid_end=valid_end,
        )

    # 获取历史K线数据中最新的毫秒时间戳
    # Weight: 1
    def get_history_candle_latest_ts(
            self,
            bar: str = '1m',
    ) -> dict:
        '''
        :param bar: 时间粒度
        '''
        instId = 'BTC-USDT'
        # 获取长度为1的最新历史K数据
        result = self.get_history_candle_latest(
            instId=instId,
            bar=bar,
            length=99,
        )
        # [ERROR RETURN] 历史K线有误
        if result['code'] != '0':
            return result
        # 最新的毫秒时间戳，以浮点数保存
        latest_ts = float(result['data'][-1, 0])
        result['data'] = latest_ts
        # [RETURN]
        return result

    # 更新产品历史K线数据到指定时间
    # Weight: >= 1 (Intelligent saving weight)
    def update_history_candle(
            self,
            instId: str,
            length: int,
            candle: np.array = None,
            end: [int, float, datetime.date, datetime.datetime, str] = None,
            bar: str = '1m',
            valid_interval=True,
    ) -> dict:
        '''
        :param instId: 合约产品
        :param length: 更新后的有效长度
        :param candle: 历史K线数据 None: 重新下载candle数据
        :param end: 更新后的终点时间
            None: 使用最新的历史K线数据毫秒时间戳
        :param bar: 时间粒度
        :param valid_interval: 是否验证时间间隔

        如论end是有有值，都会验证数据的时间终点与长度
        '''
        # 终止时间戳end_ts
        if end:
            # end有值
            end_ts = _date.to_ts(date=end, timezone=self.timezone)
        else:
            # 获取最新的历史K线时间戳
            result = self.get_history_candle_latest_ts(
                bar=bar,
            )
            # [ERROR RETURN] 获取时间戳异常
            if result['code'] != '0':
                return result
            end_ts = result['data']
        # 时间间隔
        bar_interval = _interval.get_interval(bar)
        # 计算剩余需要更新的长度 length_left
        # 存在candle
        if isinstance(candle, np.ndarray) and candle.shape[0] > 0:
            # 数据间隔异常 更新全部
            if not (np.diff(candle[:, 0]) == bar_interval).all():
                length_left = length
            else:
                # 数据过早 更新全部
                if end_ts - (length - 1) * bar_interval < candle[:, 0].min():
                    length_left = length
                # 更新剩余部分
                else:
                    candle_end_ts = candle[:, 0].max()
                    length_left = int(min((end_ts - candle_end_ts) / bar_interval, length))
        # 不存在candle，更新全部
        else:
            length_left = length
        # [RETURN] 无需更新
        if length_left == 0:
            return {'code': '0', 'data': candle, 'msg': ''}
        # 获取最新数据
        result = self.get_history_candle_latest(
            instId=instId,
            length=length_left,
            end=end_ts,
            bar=bar,
            valid_interval=valid_interval,
        )
        # [ERROR RETURN] 最新历史K线数据异常
        if result['code'] != '0':
            return result
        # 如果candle存在，二者拼接 candle_union
        candle_add = result['data']
        if isinstance(candle, np.ndarray) and candle.shape[0] > 0:
            candle_union = _transform.concat_candle(
                candles=[candle, candle_add],
                drop_duplicate=True,
                sort=True
            )
        else:
            candle_union = candle_add
        # 取末尾length长度
        candle_union = candle_union[-length:]
        # 验证时间间隔
        if valid_interval:
            valid_interval_result = _valid.valid_interval(candle=candle_union, interval=_interval.get_interval(bar))
            # [ERROR RETURN] 时间间隔错误
            if not valid_interval_result['code']:
                return {
                    'code': code.CANDLE_INTERVAL_ERROR[0],
                    'data': candle_union,
                    'msg': str(instId) + valid_interval_result['msg']
                }
        # 验证数据长度
        valid_length_result = _valid.valid_length(candle=candle_union, length=length)
        # 【ERROR RETURN】数据长度错误
        if not valid_length_result['code']:
            return {
                'code': code.CANDLE_LENGTH_ERROR[0],
                'data': candle_union,
                'msg': str(instId) + valid_length_result['msg'],
            }

        # [RETURN]
        result = {'code': '0', 'data': candle_union, 'msg': ''}
        return result

    # 历史K线 根据num获取最佳的limit
    def _get_limit(self, num: int) -> int:
        return int(np.clip(num, 1, 100))

    # 将Okx的历史K线数据从array转换成DataFrame类型
    def candle_to_df(self, candle: np.ndarray, convert_ts: bool = True) -> pd.DataFrame:
        return utils.candle_to_df(candle=candle, convert_ts=convert_ts, timezone=self.timezone)

    # 将Okx的历史K线数据从DataFrame转换成array类型
    def df_to_candle(self, df: pd.DataFrame, convert_ts: bool = True) -> np.ndarray:
        return utils.df_to_candle(df=df, convert_ts=convert_ts, timezone=self.timezone)

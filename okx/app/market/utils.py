from typing import Union
from copy import deepcopy
import numpy as np
import pandas as pd
from candlelite.crypto.okx_lite import OKX_TIMEZONE
from candlelite.calculate.transform import to_candle as _to_candle
from paux import date as _date


# 将Okx的历史K线数据从array转换成DataFrame类型
def candle_to_df(
        candle: np.ndarray,
        convert_ts: bool = True,
        timezone: Union[str, None] = OKX_TIMEZONE,
) -> pd.DataFrame:
    '''
    :param candle: array类型的历史K线数据
    :param convert_ts: 是否将时间戳转化为日期字符串
    :param timezone: 时区
        默认使用candlelite中Binance的时区
        None 使用本机默认时区
    '''
    df = pd.DataFrame(candle)
    df.columns = [
        'ts',  # 开盘时间 Open time
        'o',  # 开盘价 Open
        'h',  # 最高价 High
        'l',  # 最低价 Low
        'c',  # 收盘价 close
        'vol',  # 交易量，以张为单位；如果是衍生品合约，数值为合约的张数。如果是币币/币币杠杆，数值为交易货币的数量。
        'volCcy',  # 交易量，以币为单位；如果是衍生品合约，数值为交易货币的数量。如果是币币 / 币币杠杆，数值为计价货币的数量。
        'volCcyQuote',  # 交易量，以计价货币为单位；如：BTC-USDT 和 BTC-USDT-SWAP, 单位均是 USDT；BTC-USD-SWAP 单位是 USD
        'confirm',  # K线状态；0代表K线未完结，1代表K线已完结。
    ]
    # 是否转换时间戳为日期字符串
    if convert_ts:
        # 美国时间
        if timezone == 'America/New_York':
            fmt = '%m/%d/%Y %H:%M:%S'
        # 中国时间
        else:
            fmt = '%Y-%m-%d %H:%M:%S'
        df['ts'] = df['ts'].apply(
            lambda ts: _date.to_fmt(date=ts, timezone=timezone, fmt=fmt)
        )
    df['confirm'] = df['confirm'].astype(int)
    return df


# 将Okx的历史K线数据从DataFrame转换成array类型
def df_to_candle(
        df: pd.DataFrame,
        convert_ts: bool = True,
        timezone: Union[str, None] = OKX_TIMEZONE
):
    '''
    :param df: DataFrame类型的历史K线数据
    :param timezone: 时区
        默认使用candlelite中Binance的时区
        None 使用本机默认时区
    '''
    df = deepcopy(df)
    if convert_ts:
        df['ts'] = df['ts'].apply(
            lambda openTs: _date.to_ts(date=openTs, timezone=timezone)
        )
    candle = _to_candle(df)
    return candle

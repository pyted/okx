# okx-api 说明文档 v1.0.8

**项目更名 okx_api -> okx**

**在Python中的下载方式变成了pip install okx**

## 1 okx-api设计目的

- 目前没有交易所承认的官方Rest Api Python Sdk，只有推荐的第三方项目，虽然也很好但是对于官方接口更新的维护较慢，我需要最新的底层接口支持。
- 关于Okx，我开发了比较多的功能框架，例如获取实时行情数据的okx_candle，实盘现货交易框架：okx_spot，实盘永续合约交易框架：okx_swap，所以公用的稳定底层十分重要。
- okx-api是对交易所接口的底层封装，并非高级封装，对于熟悉Okx量化交易者来说仅需很少的学习成本。

## 2 下载okx-api

GITHUB：https://github.com/pyted/okx

```cmd
pip3 install okx
```

## 3 使用okx-api的例子

```python
from okx import Market  # 导入行情数据
from pprint import pprint

if __name__ == '__main__':
  # 行情数据无需添加key、secret与passphrase
  key = ''
  secret = ''
  passphrase = ''
  flag = '0'  # flag = '0' 实盘 flag = '1' 模拟盘

  market = Market()
  # 获取现货交易BTC-USDT的行情信息
  result = market.get_ticker(instId='BTC-USDT')
  pprint(result)
```

输出：

```text
>> {'code': '0',
>>  'data': [{'askPx': '23352.5',
>>            'askSz': '1.26608653',
>>            'bidPx': '23352.4',
>>            'bidSz': '0.46033212',
>>            'high24h': '23722.5',
>>            'instId': 'BTC-USDT',
>>            'instType': 'SPOT',
>>            'last': '23352.5',
>>            'lastSz': '0.01734077',
>>            'low24h': '23211',
>>            'open24h': '23463.6',
>>            'sodUtc0': '23431.3',
>>            'sodUtc8': '23603.6',
>>            'ts': '1675510037012',
>>            'vol24h': '5108.83404369',
>>            'volCcy24h': '119705529.10438071'}],
>>  'msg': ''}
```


## 4 okx-api的说明


okx-api是对REST API接口的封装，不包含WebSocket API。

okx-api的请求参数和返回结果与官方一致

okx-api服务器网络问题时，会尝试重新请求，重新请求的状态码有：                

- 50001 服务暂时不可用，请稍后重试
- 50004 接口请求超时（不代表请求成功或者失败，请检查请求结果）
- 50011 用户请求频率过快，超过该接口允许的限额。请参考 API 文档并限制请求
- 50013 当前系统繁忙，请稍后重试
- 50026 系统错误，请稍后重试

    
okx-api包含功能：

|接口种类|类名称|是否需要秘钥|
|:---|:---|:---|
|交易|okx.Trade|是|
|资金|okx.Funding|是|
|闪兑|okx.Convert|是|
|账户|okx.Account|是|
|子账户|okx.SubAccount|是|
|网格交易|okx.Grid|是|
|赚币|okx.Staking|是|
|跟单接口|okx.CopyTrading|是|
|行情数据|okx.Market|否|
|公共数据|okx.Public|否|
|交易大数据|okx.Rubik|否|
|Status（系统状态）|okx.System|否|

全部功能类的实例化都包含4个参数：

- key，默认值：''
- secret，默认值：''
- passphrase，默认值：''
- flag，默认值：'0' 
    - '0' 实盘
    - '1' 模拟盘

**个人测试发现模拟盘的数据接口功能并不完善，对于待上线项目，建议直接采用小金额实盘接口测试。**

## 6. 交易模块 Trade

### 6.1 交易接口总览

|接口名称|函数名称|
|:---|:---|
|下单|set_order|
|批量下单|set_batch_orders|
|撤单|set_cancel_order|
|批量撤单|set_cancel_batch_orders|
|修改订单|set_amend_order|
|批量修改订单|set_amend_batch_orders|
|市价仓位全平|set_close_position|
|获取订单信息|get_order|
|获取未成交订单列表|get_orders_pending|
|获取历史订单记录（近七天）|get_orders_history|
|获取历史订单记录（近三个月）|get_orders_history_archive|
|获取成交明细（近三天）|get_fills|
|获取成交明细（近三个月）|get_fills_history|
|策略委托下单|set_order_algo|
|撤销策略委托订单|set_cancel_algos|
|撤销高级策略委托订单|set_cancel_advance_algos|
|获取未完成策略委托单列表|get_orders_algo_pending|
|获取历史策略委托单列表|get_orders_algo_history|
|获取一键兑换主流币币种列表|get_easy_convert_currency_list|
|一键兑换主流币交易|set_easy_convert|
|获取一键兑换主流币历史记录|get_easy_convert_history|
|获取一键还债币种列表|get_one_click_repay_currency_list|
|一键还债交易|set_one_click_repay|
|获取一键还债历史记录|get_one_click_repay_history|

### 6.2 交易接口介绍

#### 6.2.1 下单 set_order

请求路径：/api/v5/trade/order 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USD-190927-5000-C|
|tdMode|String|是|交易模式保证金模式：isolated：逐仓 ；cross：全仓非保证金模式：cash：非保证金|
|side|String|是|订单方向buy：买，sell：卖|
|ordType|String|是|订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）|
|sz|String|是|委托数量|
|ccy|String|否|保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单|
|clOrdId|String|否|客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|tag|String|否|订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。|
|posSide|String|可选|持仓方向在双向持仓模式下必填，且仅可选择long或short。 仅适用交割、永续。|
|px|String|可选|委托价格，仅适用于limit、post_only、fok、ioc类型的订单|
|reduceOnly|Boolean|否|是否只减仓，true或false，默认false仅适用于币币杠杆，以及买卖模式下的交割/永续仅适用于单币种保证金模式和跨币种保证金模式|
|tgtCcy|String|否|市价单委托数量sz的单位，仅适用于币币市价订单base_ccy: 交易货币 ；quote_ccy：计价货币买单默认quote_ccy， 卖单默认base_ccy|
|banAmend|Boolean|否|是否禁止币币市价改单，true 或 false，默认false为true时，余额不足时，系统不会改单，下单会失败，仅适用于币币市价单|
|tpTriggerPx|String|否|止盈触发价，如果填写此参数，必须填写 止盈委托价|
|tpOrdPx|String|否|止盈委托价，如果填写此参数，必须填写 止盈触发价委托价格为-1时，执行市价止盈|
|slTriggerPx|String|否|止损触发价，如果填写此参数，必须填写 止损委托价|
|slOrdPx|String|否|止损委托价，如果填写此参数，必须填写 止损触发价委托价格为-1时，执行市价止损|
|tpTriggerPxType|String|否|止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last|
|slTriggerPxType|String|否|止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last|
|quickMgnType|String|否|一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动|



#### 6.2.2 批量下单 set_batch_orders

请求路径：/api/v5/trade/batch-orders 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USD-190927-5000-C|
|tdMode|String|是|交易模式保证金模式：isolated：逐仓 ；cross：全仓非保证金模式：cash：非保证金|
|side|String|是|订单方向buy：买，sell：卖|
|ordType|String|是|订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）|
|sz|String|是|委托数量|
|ccy|String|否|保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单|
|clOrdId|String|否|客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|tag|String|否|订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-16位之间。|
|posSide|String|可选|持仓方向在双向持仓模式下必填，且仅可选择long或short。 仅适用交割、永续。|
|px|String|否|委托价格，仅适用于limit、post_only、fok、ioc类型的订单|
|reduceOnly|Boolean|否|是否只减仓，true或false，默认false仅适用于币币杠杆，以及买卖模式下的交割/永续仅适用于单币种保证金模式和跨币种保证金模式|
|tgtCcy|String|否|市价单委托数量sz的单位，仅适用于币币市价订单base_ccy: 交易货币 ；quote_ccy：计价货币买单默认quote_ccy， 卖单默认base_ccy|
|banAmend|Boolean|否|是否禁止币币市价改单，true 或 false，默认false为true时，余额不足时，系统不会改单，下单会失败，仅适用于币币市价单|
|tpTriggerPx|String|否|止盈触发价，如果填写此参数，必须填写 止盈委托价|
|tpOrdPx|String|否|止盈委托价，如果填写此参数，必须填写 止盈触发价委托价格为-1时，执行市价止盈|
|slTriggerPx|String|否|止损触发价，如果填写此参数，必须填写 止损委托价|
|slOrdPx|String|否|止损委托价，如果填写此参数，必须填写 止损触发价委托价格为-1时，执行市价止损|
|tpTriggerPxType|String|否|止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last|
|slTriggerPxType|String|否|止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last|
|quickMgnType|String|否|一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动|



#### 6.2.3 撤单 set_cancel_order

请求路径：/api/v5/trade/cancel-order 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USD-190927|
|ordId|String|可选|订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主|
|clOrdId|String|可选|用户自定义ID|



#### 6.2.4 批量撤单 set_cancel_batch_orders

请求路径：/api/v5/trade/cancel-batch-orders 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USD-190927|
|ordId|String|可选|订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主|
|clOrdId|String|可选|用户自定义ID|



#### 6.2.5 修改订单 set_amend_order

请求路径：/api/v5/trade/amend-order 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID|
|cxlOnFail|Boolean|否|false：不自动撤单true：自动撤单 当订单修改失败时，该订单是否需要自动撤销。默认为false|
|ordId|String|可选|订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主|
|clOrdId|String|可选|用户自定义order ID|
|reqId|String|否|用户自定义修改事件ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|newSz|String|可选|修改的新数量，newSz和newPx不可同时为空。对于部分成交订单，该数量应包含已成交数量。|
|newPx|String|可选|修改的新价格|



#### 6.2.6 批量修改订单 set_amend_batch_orders

请求路径：/api/v5/trade/amend-batch-orders 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID|
|cxlOnFail|Boolean|否|false：不自动撤单true：自动撤单 当订单修改失败时，该订单是否需要自动撤销，默认为false|
|ordId|String|可选|订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主|
|clOrdId|String|可选|用户自定义order ID|
|reqId|String|否|用户自定义修改事件ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|newSz|String|可选|修改的新数量，newSz和newPx不可同时为空。对于部分成交订单，该数量应包含已成交数量。|
|newPx|String|可选|修改的新价格|



#### 6.2.7 市价仓位全平 set_close_position

请求路径：/api/v5/trade/close-position 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID|
|mgnMode|String|是|保证金模式cross：全仓 ；isolated：逐仓|
|posSide|String|可选|持仓方向单向持仓模式下：可不填写此参数，默认值net，如果填写，仅可以填写net双向持仓模式下： 必须填写此参数，且仅可以填写long：平多 ，short：平空|
|ccy|String|可选|保证金币种，单币种保证金模式的全仓币币杠杆平仓必填|
|autoCxl|Boolean|否|当市价全平时，平仓单是否需要自动撤销,默认为false.false：不自动撤单true：自动撤单|
|clOrdId|String|否|客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|tag|String|否|订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。|



#### 6.2.8 获取订单信息 get_order

请求路径：/api/v5/trade/order 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID ，如BTC-USD-190927|
|ordId|String|可选|订单ID ，ordId和clOrdId必须传一个，若传两个，以ordId为主|
|clOrdId|String|可选|用户自定义ID|



#### 6.2.9 获取未成交订单列表 get_orders_pending

请求路径：/api/v5/trade/orders-pending 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|否|产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|否|标的指数|
|instFamily|String|否|交易品种适用于交割/永续/期权|
|instId|String|否|产品ID，如BTC-USD-200927|
|ordType|String|否|订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）|
|state|String|否|订单状态live：等待成交partially_filled：部分成交|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 6.2.10 获取历史订单记录（近七天） get_orders_history

请求路径：/api/v5/trade/orders-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|否|标的指数|
|instFamily|String|否|交易品种适用于交割/永续/期权|
|instId|String|否|产品ID，如BTC-USD-190927|
|ordType|String|否|订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）|
|state|String|否|订单状态canceled：撤单成功filled：完全成交|
|category|String|否|订单种类twap：TWAP自动换币adl：ADL自动减仓full_liquidation：强制平仓partial_liquidation：强制减仓delivery：交割ddh：对冲减仓类型订单|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId|
|begin|String|否|筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085|
|end|String|否|筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 6.2.11 获取历史订单记录（近三个月） get_orders_history_archive

请求路径：/api/v5/trade/orders-history-archive 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|否|标的指数|
|instFamily|String|否|交易品种适用于交割/永续/期权|
|instId|String|否|产品ID，如BTC-USD-200927|
|ordType|String|否|订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）|
|state|String|否|订单状态canceled：撤单成功filled：完全成交|
|category|String|否|订单种类twap：TWAP自动换币adl：ADL自动减仓full_liquidation：强制平仓partial_liquidation：强制减仓delivery：交割ddh：对冲减仓类型订单|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId|
|begin|String|否|筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085|
|end|String|否|筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 6.2.12 获取成交明细（近三天） get_fills

请求路径：/api/v5/trade/fills 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|否|产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|否|标的指数|
|instFamily|String|否|交易品种适用于交割/永续/期权|
|instId|String|否|产品 ID，如BTC-USD-190927|
|ordId|String|否|订单 ID|
|after|String|否|请求此 ID 之前（更旧的数据）的分页内容，传的值为对应接口的billId|
|before|String|否|请求此 ID 之后（更新的数据）的分页内容，传的值为对应接口的billId|
|begin|String|否|筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085|
|end|String|否|筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 6.2.13 获取成交明细（近三个月） get_fills_history

请求路径：/api/v5/trade/fills-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|否|标的指数|
|instFamily|String|否|交易品种适用于交割/永续/期权|
|instId|String|否|产品 ID，如BTC-USD-190927|
|ordId|String|否|订单 ID|
|after|String|否|请求此 ID 之前（更旧的数据）的分页内容，传的值为对应接口的billId|
|before|String|否|请求此 ID 之后（更新的数据）的分页内容，传的值为对应接口的billId|
|begin|String|否|筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085|
|end|String|否|筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 6.2.14 策略委托下单 set_order_algo

请求路径：/api/v5/trade/order-algo 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USD-190927-5000-C|
|tdMode|String|是|交易模式保证金模式isolated：逐仓，cross：全仓非保证金模式cash：非保证金|
|side|String|是|订单方向buy：买sell：卖|
|ordType|String|是|订单类型conditional：单向止盈止损oco：双向止盈止损trigger：计划委托move_order_stop：移动止盈止损iceberg：冰山委托twap：时间加权委托|
|ccy|String|否|保证金币种仅适用于单币种保证金模式下的全仓杠杆订单|
|posSide|String|可选|持仓方向在双向持仓模式下必填，且仅可选择long或short|
|sz|String|可选|委托数量sz和closeFraction必填且只能填其一|
|tag|String|否|订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间|
|tgtCcy|String|否|委托数量的类型base_ccy: 交易货币 ；quote_ccy：计价货币仅适用于币币单向止盈止损市价买单默认买为计价货币，卖为交易货币|
|reduceOnly|Boolean|否|是否只减仓，true或false，默认false仅适用于币币杠杆，以及买卖模式下的交割/永续仅适用于单币种保证金模式和跨币种保证金模式|
|clOrdId|String|否|客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间|
|closeFraction|String|可选|策略委托触发时，平仓的百分比。1 代表100%现在系统只支持全部平仓，唯一接受参数为1仅适用于交割或永续仅适用于买卖模式posSide=net仅适用于减仓订单reduceOnly=true仅适用于止盈止损ordType=conditional或oco仅适用于止盈止损市价订单sz和closeFraction必填且只能填其一|
|quickMgnType|String|否|一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动|



#### 6.2.15 撤销策略委托订单 set_cancel_algos

请求路径：/api/v5/trade/cancel-algos 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoId|String|是|策略委托单ID|
|instId|String|是|产品ID 如BTC-USDT|



#### 6.2.16 撤销高级策略委托订单 set_cancel_advance_algos

请求路径：/api/v5/trade/cancel-advance-algos 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoId|String|是|策略委托单ID|
|instId|String|是|产品ID 如BTC-USDT|



#### 6.2.17 获取未完成策略委托单列表 get_orders_algo_pending

请求路径：/api/v5/trade/orders-algo-pending 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ordType|String|是|订单类型conditional：单向止盈止损oco：双向止盈止损trigger：计划委托move_order_stop：移动止盈止损iceberg：冰山委托twap：时间加权委托|
|algoId|String|否|策略委托单ID|
|instType|String|否|产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约MARGIN：杠杆|
|instId|String|否|产品ID，BTC-USD-190927|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId|
|limit|String|否|返回结果的数量，最大为100，默认100条|
|clOrdId|String|否|客户自定义订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|



#### 6.2.18 获取历史策略委托单列表 get_orders_algo_history

请求路径：/api/v5/trade/orders-algo-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ordType|String|是|订单类型conditional：单向止盈止损oco：双向止盈止损trigger：计划委托move_order_stop：移动止盈止损iceberg：冰山委托twap：时间加权委托|
|state|String|可选|订单状态effective：已生效canceled：已经撤销order_failed：委托失败【state和algoId必填且只能填其一】|
|algoId|String|可选|策略委托单ID 【state和algoId必填且只能填其一】|
|instType|String|否|产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约MARGIN：杠杆|
|instId|String|否|产品ID，BTC-USD-190927|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 6.2.19 获取一键兑换主流币币种列表 get_easy_convert_currency_list

请求路径：/api/v5/trade/easy-convert-currency-list 请求方法：GET

请求参数：无


#### 6.2.20 一键兑换主流币交易 set_easy_convert

请求路径：/api/v5/trade/easy-convert 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|fromCcy|Array|是|小币支付币种单次最多同时选择5个币种，如有多个币种则用逗号隔开|
|toCcy|String|是|兑换的主流币只选择一个币种，且不能和小币支付币种重复|



#### 6.2.21 获取一键兑换主流币历史记录 get_easy_convert_history

请求路径：/api/v5/trade/easy-convert-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|after|String|否|查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085|
|before|String|否|查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085|
|limit|String|否|返回的结果集数量，默认为100，最大为100|



#### 6.2.22 获取一键还债币种列表 get_one_click_repay_currency_list

请求路径：/api/v5/trade/one-click-repay-currency-list 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|debtType|String|否|负债类型cross: 全仓负债isolated: 逐仓负债|



#### 6.2.23 一键还债交易 set_one_click_repay

请求路径：/api/v5/trade/one-click-repay 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|debtCcy|Array|是|负债币种单次最多同时选择5个币种，如有多个币种则用逗号隔开|
|repayCcy|String|是|偿还币种只选择一个币种，且不能和负债币种重复|



#### 6.2.24 获取一键还债历史记录 get_one_click_repay_history

请求路径：/api/v5/trade/one-click-repay-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|after|String|否|查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085|
|before|String|否|查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085|
|limit|String|否|返回的结果集数量，默认为100，最大为100|


### 6.3 例子

交易模块必须填写秘钥

```python
from okx import Trade
from pprint import pprint

if __name__ == '__main__':
  # 交易模块需要秘钥
  key = '****'
  secret = '****'
  passphrase = '****'
  flag = '0'

  trade = Trade(key, secret, passphrase, flag)

  # 限价单购买BTC-USDT现货，数量2，价格1
  result = trade.set_order(
    instId='BTC-USDT',
    tdMode='cash',
    side='buy',
    ordType='limit',
    px='1',
    sz='2',

  )
  pprint(result)
```

输出：

```text
>> {'code': '0',
>>  'data': [{'clOrdId': '',
>>            'ordId': '542313757641707520',
>>            'sCode': '0',
>>            'sMsg': 'Order placed',
>>            'tag': ''}],
>>  'msg': ''}
```

## 7 资金 Funding 

### 7.1  资金接口总览

|接口名称|函数名称|
|:---|:---|
|获取币种列表|get_currencies|
|获取资金账户余额|get_balances|
|获取不可交易资产|get_non_tradable_assets|
|获取账户资产估值|get_asset_valuation|
|资金划转|set_transfer|
|获取资金划转状态|get_transfer_state|
|获取资金流水|get_bills|
|闪电网络充币|get_deposit_lightning|
|获取充值地址信息|get_deposit_address|
|获取充值记录|get_deposit_history|
|提币|set_withdrawal|
|闪电网络提币|set_withdrawal_lightning|
|撤销提币|set_cancel_withdrawal|
|获取提币记录|get_withdrawal_history|
|获取充值/提现的详细状态|get_deposit_withdraw_status|
|小额资产兑换|set_convert_dust_assets|
|获取余币宝余额|get_saving_balance|
|余币宝申购/赎回|set_purchase_redempt|
|设置余币宝借贷利率|set_lending_rate|
|获取余币宝出借明细|get_lending_history|
|获取市场借贷信息（公共）|get_lending_rate_summary|
|获取市场借贷历史（公共）|get_lending_rate_history|

### 7.2  资金接口介绍

#### 7.2.1 获取币种列表 get_currencies

请求路径：/api/v5/asset/currencies 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔|



#### 7.2.2 获取资金账户余额 get_balances

请求路径：/api/v5/asset/balances 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔|



#### 7.2.3 获取不可交易资产 get_non_tradable_assets

请求路径：/api/v5/asset/non-tradable-assets 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔|



#### 7.2.4 获取账户资产估值 get_asset_valuation

请求路径：/api/v5/asset/asset-valuation 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|资产估值对应的单位BTC 、USDTUSD 、CNY 、JPY、KRW、RUB、EURVND 、IDR 、INR、PHP、THB、TRYAUD 、SGD 、ARS、SAR、AED、IQD默认为  BTC 为单位的估值|



#### 7.2.5 资金划转 set_transfer

请求路径：/api/v5/asset/transfer 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种，如USDT|
|amt|String|是|划转数量|
|from|String|是|转出账户6：资金账户18：交易账户|
|to|String|是|转入账户6：资金账户18：交易账户|
|subAcct|String|可选|子账户名称，type 为1，2或4：subAcct 为必填项|
|type|String|否|划转类型0：账户内划转1：母账户转子账户(仅适用于母账户APIKey)2：子账户转母账户(仅适用于母账户APIKey)3：子账户转母账户(仅适用于子账户APIKey)4：子账户转子账户(仅适用于子账户APIKey，且目标账户需要是同一母账户下的其他子账户)默认是0|
|loanTrans|Boolean|否|是否支持跨币种保证金模式或组合保证金模式下的借币转入/转出true 或 false，默认false|
|clientId|String|否|客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|omitPosRisk|String|否|是否忽略仓位风险默认为false仅适用于组合保证金模式|



#### 7.2.6 获取资金划转状态 get_transfer_state

请求路径：/api/v5/asset/transfer-state 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|transId|String|可选|划转IDtransId和clientId必须传一个，若传两个，以transId为主|
|clientId|String|可选|客户自定义ID|
|type|String|否|划转类型0：账户内划转1：母账户转子账户(仅适用于母账户APIKey)2：子账户转母账户(仅适用于母账户APIKey)3：子账户转母账户(仅适用于子账户APIKey)4：子账户转子账户(仅适用于子账户APIKey，且目标账户需要是同一母账户下的其他子账户)默认是0|



#### 7.2.7 获取资金流水 get_bills

请求路径：/api/v5/asset/bills 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种|
|type|String|否|账单类型1：充值2：提现13：撤销提现20：转出至子账户（主体是母账户）21：从子账户转入（主体是母账户）22：转出到母账户（主体是子账户）23：母账户转入（主体是子账户）28：领取47：系统冲正48：活动得到49：活动送出50：预约得到51：预约扣除52：发红包53：抢红包54：红包退还61：兑换68：领取卡券权益69：发送卡券权益72：收币73：送币74：送币退还75：申购余币宝76：赎回余币宝77：派发78：锁定79：节点投票80：锁仓挖矿81：投票赎回82：锁仓赎回83：锁仓挖矿收益84：违约金85：算力挖矿收益86：云算力支付87：云算力收益88：补贴收益89：存币收益90：挖矿申购91：挖矿赎回92：补充质押物93：赎回质押物94：投资95：借款人借款96：投资本金转入97：借款人借款转出98：借款人借款利息转出99：投资人投资利息转入102：提前还款违约金转入103：提前还款违约金转出104：抵押借贷手续费转入105：抵押借贷手续费转出106：逾期手续费转入107：逾期手续费转出108：逾期利息转出109：借款还款逾期利息转入110：平仓质押物转入到系统账号111：平仓质押物转出到系统账号112：爆仓质押物转入到系统账号113：爆仓质押物转出到系统账号114：风险准备金转入115：风险准备金转出116：创建订单117：完成订单118：取消订单119：商家解冻保证金120：商家添加保证金121：FiatGateway 创建订单122：FiatGateway 取消订单123：FiatGateway 完成订单124：Jumpstart 解锁125：手动注入126：利息注入127：投资手续费转入128：投资手续费转出129：奖励转入130：从交易账户转入131：转出至交易账户132：客服冻结133：客服解冻134：客服转交135：跨链兑换136：兑换137：ETH2.0申购138：ETH2.0兑换139：ETH2.0收益143：系统退款145：系统回收146：客户回馈147：sushi 增发收益150：节点返佣151：邀请奖励152：经纪商返佣153：新手奖励154：拆盲盒奖励155：福利中心提现156：返佣卡返佣157：红包160：双币赢申购161：双币赢回款162：双币赢收益163：双币赢退款169：2022春节红包172：助力人返佣173：手续费返现174：支付175：锁定质押物176：借款转入177：添加质押物178：减少质押物179：还款180：释放质押物181：偿还空投糖果182：反馈奖励183：邀请好友奖励184：瓜分奖池奖励185：经纪商闪兑返佣186：0元领ETH187：闪兑划转188：插槽竞拍兑换189：盲盒奖励193：卡支付购买195：不可交易资产提币196：不可交易资产提币撤销197：不可交易资产充值198：无效资产减少199：有效资产增加200：买入202：价格锁定申购203：价格锁定回款204：价格锁定收益205：价格锁定退款207：双币赢精简版申购208：双币赢精简版回款209：双币赢精简版收益210：双币赢精简版退款211：投聪夺币中奖212：多币种借贷锁定质押物213：多币种质押物转出用户帐户214：多币种质押物返还用户215：多币种借贷释放质押物216：多币种借贷划转到用户帐户217：多币种借贷借款转入218：多币种借贷还款219：多币种还款由用户帐户转入220：已下架数字货币221：提币手续费支出222：提币手续费退款223：带单分润224：服务费225：鲨鱼鳍申购226：鲨鱼鳍回款227：鲨鱼鳍收益228：鲨鱼鳍退款229：空投发放230：换币完成232：利息补贴已入账233：经纪商佣金补偿|
|clientId|String|否|转账或提币的客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|after|String|否|查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085|
|before|String|否|查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085|
|limit|String|否|分页返回的结果集数量，最大为 100，不填默认返回 100 条|



#### 7.2.8 闪电网络充币 get_deposit_lightning

请求路径：/api/v5/asset/deposit-lightning 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种，仅支持BTC|
|amt|String|是|充值数量，推荐在0.000001〜0.1之间|
|to|String|否|资金充值到账账户6: 资金账户18: 交易账户不填写此参数，默认到账资金账户|



#### 7.2.9 获取充值地址信息 get_deposit_address

请求路径：/api/v5/asset/deposit-address 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种，如BTC|



#### 7.2.10 获取充值记录 get_deposit_history

请求路径：/api/v5/asset/deposit-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种名称，如BTC|
|depId|String|否|充值记录 ID|
|fromWdId|String|否|内部转账发起者提币申请 ID如果该笔充值来自于内部转账，则该字段展示内部转账发起者的提币ID|
|txId|String|否|区块转账哈希记录|
|type|String|否|充值方式3：内部转账4：链上充值|
|state|String|否|充值状态0：等待确认1：确认到账2：充值成功8：因该币种暂停充值而未到账，恢复充值后自动到账11：命中地址黑名单12：账户或充值被冻结13：子账户充值拦截|
|after|String|否|查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1654041600000|
|before|String|否|查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1656633600000|
|limit|string|否|返回的结果集数量，默认为100，最大为100，不填默认返回100条|



#### 7.2.11 提币 set_withdrawal

请求路径：/api/v5/asset/withdrawal 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种，如USDT|
|amt|String|是|数量|
|dest|String|是|提币方式3：内部转账4：链上提币|
|toAddr|String|是|如果选择链上提币，toAddr必须是认证过的数字货币地址。某些数字货币地址格式为地址:标签，如ARDOR-7JF3-8F2E-QUWZ-CAN7F:123456如果选择内部转账，toAddr必须是接收方地址，可以是邮箱、手机或者账户名。|
|fee|String|是|网络手续费≥0，提币到数字货币地址所需网络手续费可通过获取币种列表接口查询|
|chain|String|可选|币种链信息如USDT下有USDT-ERC20，USDT-TRC20，USDT-Omni多个链如果没有不填此参数，则默认为主链|
|areaCode|String|可选|手机区号当toAddr为手机号时，该参数必填|
|clientId|String|否|客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|



#### 7.2.12 闪电网络提币 set_withdrawal_lightning

请求路径：/api/v5/asset/withdrawal-lightning 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种，如BTC|
|invoice|String|是|invoice 号码|
|memo|String|否|闪电网络提币的备注|



#### 7.2.13 撤销提币 set_cancel_withdrawal

请求路径：/api/v5/asset/cancel-withdrawal 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|wdId|String|是|提币申请ID|



#### 7.2.14 获取提币记录 get_withdrawal_history

请求路径：/api/v5/asset/withdrawal-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种名称，如BTC|
|wdId|String|否|提币申请ID|
|clientId|String|否|客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|txId|String|否|区块转账哈希记录|
|type|String|否|提币方式3：内部转账4：链上提币|
|state|String|否|提币状态-3：撤销中-2：已撤销-1：失败0：等待提币1：提币中2：提币成功7: 审核通过10: 等待划转4,5,6,8,9,12: 等待客服审核|
|after|String|否|查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1654041600000|
|before|String|否|查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1656633600000|
|limit|string|否|返回的结果集数量，默认为100，最大为100，不填默认返回100条|



#### 7.2.15 获取充值/提现的详细状态 get_deposit_withdraw_status

请求路径：/api/v5/asset/deposit-withdraw-status 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|wdId|String|可选|提币申请ID，用于查询资金提现wdId与txId必传其一也仅可传其一|
|txId|String|可选|区块转账哈希记录ID，用于查询资金充值wdId与txId必传其一也仅可传其一|
|ccy|String|可选|币种，如USDT查询充值时必填，需要与txId一并提供|
|to|String|可选|资金充值到账账户地址查询充值时必填，需要与txId一并提供|
|chain|String|可选|币种链信息，例如 USDT-ERC20查询充值时必填，需要与txId一并提供|



#### 7.2.16 小额资产兑换 set_convert_dust_assets

请求路径：/api/v5/asset/convert-dust-assets 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|Array|是|需要转换的币种资产|



#### 7.2.17 获取余币宝余额 get_saving_balance

请求路径：/api/v5/asset/saving-balance 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC|



#### 7.2.18 余币宝申购/赎回 set_purchase_redempt

请求路径：/api/v5/asset/purchase_redempt 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种名称，如BTC|
|amt|String|是|申购/赎回 数量|
|side|String|是|操作类型purchase：申购redempt：赎回|
|rate|String|是|申购年利率仅适用于申购，新申购的利率会覆盖上次申购的利率参数取值范围在1%到365%之间|



#### 7.2.19 设置余币宝借贷利率 set_lending_rate

请求路径：/api/v5/asset/set-lending-rate 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种名称，如BTC|
|rate|String|是|贷出利率参数取值范围在1%到365%之间|



#### 7.2.20 获取余币宝出借明细 get_lending_history

请求路径：/api/v5/asset/lending-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC|
|after|String|否|查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085|
|before|String|否|查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085|
|limit|String|否|分页返回的结果集数量，最大为 100，不填默认返回 100 条|



#### 7.2.21 获取市场借贷信息（公共） get_lending_rate_summary

请求路径：/api/v5/asset/lending-rate-summary 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC|



#### 7.2.22 获取市场借贷历史（公共） get_lending_rate_history

请求路径：/api/v5/asset/lending-rate-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC|
|after|String|否|查询在此之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085|
|before|String|否|查询在此之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|


### 7.3 例子  

资金模块需要秘钥

```python
from okx import Funding
from pprint import pprint

if __name__ == '__main__':
  # 资金模块需要秘钥
  key = '****'
  secret = '****'
  passphrase = '****'
  flag = '0'

  funding = Funding(key, secret, passphrase, flag)

  # 获取资金账户余额
  result = funding.get_balances(ccy='USDT')
  pprint(result)
```

输出：

```text
>> {'code': '0',
>>  'data': [{'availBal': '124812.0771248455630674',
>>            'bal': '124812.0771248455630674',
>>            'ccy': 'USDT',
>>            'frozenBal': '0'}],
>>  'msg': ''}
```

## 8 Convert 闪兑

### 8.1 闪兑接口总览

|接口名称|函数名称|
|:---|:---|
|获取闪兑币种列表|get_currencies|
|获取闪兑币对信息|get_currency_pair|
|闪兑预估询价|set_estimate_quote|
|闪兑交易|set_trade|
|获取闪兑交易历史|get_history|

### 8.2 闪兑接口介绍

#### 8.2.1 获取闪兑币种列表 get_currencies

请求路径：/api/v5/asset/convert/currencies 请求方法：GET

请求参数：无


#### 8.2.2 获取闪兑币对信息 get_currency_pair

请求路径：/api/v5/asset/convert/currency-pair 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|fromCcy|String|是|消耗币种，如USDT|
|toCcy|String|是|获取币种，如BTC|



#### 8.2.3 闪兑预估询价 set_estimate_quote

请求路径：/api/v5/asset/convert/estimate-quote 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|baseCcy|String|是|交易货币币种，如BTC-USDT中的BTC|
|quoteCcy|String|是|计价货币币种，如BTC-USDT中的USDT|
|side|String|是|交易方向买：buy卖：sell描述的是对于baseCcy的交易方向|
|rfqSz|String|是|询价数量|
|rfqSzCcy|String|是|询价币种|
|clQReqId|String|否|客户端自定义的订单标识字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|tag|String|否|订单标签适用于broker用户|



#### 8.2.4 闪兑交易 set_trade

请求路径：/api/v5/asset/convert/trade 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|quoteId|String|是|报价ID|
|baseCcy|String|是|交易货币币种，如BTC-USDT中的BTC|
|quoteCcy|String|是|计价货币币种，如BTC-USDT中的USDT|
|side|String|是|交易方向买：buy卖：sell描述的是对于baseCcy的交易方向|
|sz|String|是|用户报价数量报价数量应不大于预估询价中的询价数量|
|szCcy|String|是|用户报价币种|
|clTReqId|String|否|用户自定义的订单标识字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。|
|tag|String|否|订单标签适用于broker用户|



#### 8.2.5 获取闪兑交易历史 get_history

请求路径：/api/v5/asset/convert/history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|after|String|否|查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085|
|before|String|否|查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085|
|limit|String|否|返回的结果集数量，默认为100，最大为100|
|tag|String|否|订单标签适用于broker用户|

### 8.3 例子

闪兑模块需要秘钥

```python
from okx import Convert
from pprint import pprint

if __name__ == '__main__':
  # 闪兑模块需要秘钥
  key = '****'
  secret = '****'
  passphrase = '****'
  flag = '0'

  convert = Convert(key, secret, passphrase, flag)

  # 获取闪兑币种列表
  result = convert.get_currencies()
  pprint(result)
```

输出：

```text
>> {'code': '0',
>>  'data': [{'ccy': 'BTC', 'max': '', 'min': ''},
>>           {'ccy': 'ETH', 'max': '', 'min': ''},
>>           ... ...
>>  'msg': ''}
```

## 9 Account 账户

### 9.1 账户接口总览

|接口名称|函数名称|
|:---|:---|
|查看账户余额|get_balance|
|查看持仓信息|get_positions|
|查看历史持仓信息|get_positions_history|
|查看账户持仓风险|get_account_position_risk|
|账单流水查询（近七天）|get_bills|
|账单流水查询（近三月）|get_bills_archive|
|查看账户配置|get_config|
|设置持仓模式|set_position_mode|
|设置杠杆倍数|set_leverage|
|获取最大可买卖/开仓数量|get_max_size|
|获取最大可用数量|get_max_avail_size|
|调整保证金|set_margin_balance|
|获取杠杆倍数|get_leverage_info|
|获取交易产品最大可借|get_max_loan|
|获取当前账户交易手续费费率|get_trade_fee|
|获取计息记录|get_interest_accrued|
|获取用户当前杠杆借币利率|get_interest_rate|
|期权greeks的PA/BS切换|set_greeks|
|逐仓交易设置|set_isolated_mode|
|查看账户最大可转余额|get_max_withdrawal|
|查看账户特定风险状态|get_risk_state|
|一键借币模式手动借币还币|set_quick_margin_borrow_repay|
|获取一键借币还币历史|get_quick_margin_borrow_repay_history|
|尊享借币还币|set_borrow_repay|
|获取尊享借币还币历史|get_borrow_repay_history|
|获取尊享借币计息记录|get_vip_interest_accrued|
|获取尊享借币扣息记录|get_vip_interest_deducted|
|尊享借币订单列表|get_vip_loan_order_list|
|尊享借币订单详情|get_vip_loan_order_detail|
|获取借币利率与限额|get_interest_limits|
|组合保证金的虚拟持仓保证金计算|set_simulated_margin|
|查看账户Greeks|get_greeks|
|获取组合保证金模式全仓限制|get_position_tiers|
|设置组合保证金账户风险对冲模式|set_riskOffset_type|
|开通期权交易|set_activate_option|


### 9.2 账户接口介绍

#### 9.2.1 查看账户余额 get_balance

请求路径：/api/v5/account/balance 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔|



#### 9.2.2 查看持仓信息 get_positions

请求路径：/api/v5/account/positions 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|否|产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权instType和instId同时传入的时候会校验instId与instType是否一致。|
|instId|String|否|交易产品ID，如：BTC-USD-190927-5000-C支持多个instId查询（不超过10个），半角逗号分隔|
|posId|String|否|持仓ID支持多个posId查询（不超过20个），半角逗号分割|



#### 9.2.3 查看历史持仓信息 get_positions_history

请求路径：/api/v5/account/positions-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|否|产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|instId|String|否|交易产品ID，如：BTC-USD-SWAP|
|mgnMode|String|否|保证金模式cross：全仓，isolated：逐仓|
|type|String|否|平仓类型1：部分平仓;2：完全平仓;3：强平;4：强减;5：ADL自动减仓;状态叠加时，以最新的平仓类型为准状态为准。|
|posId|String|否|持仓ID|
|after|String|否|查询仓位更新 (uTime) 之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085|
|before|String|否|查询仓位更新 (uTime) 之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085|
|limit|String|否|分页返回结果的数量，最大为100，默认100条|



#### 9.2.4 查看账户持仓风险 get_account_position_risk

请求路径：/api/v5/account/account-position-risk 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|否|产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|



#### 9.2.5 账单流水查询（近七天） get_bills

请求路径：/api/v5/account/bills 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|否|产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|ccy|String|否|账单币种|
|mgnMode|String|否|仓位类型isolated：逐仓cross：全仓|
|ctType|String|否|linear： 正向合约inverse： 反向合约仅交割/永续有效|
|type|String|否|账单类型1：划转2：交易3：交割4：自动换币5：强平6：保证金划转7：扣息8：资金费9：自动减仓10：穿仓补偿11：系统换币12：策略划拨13：对冲减仓14: 大宗交易15: 一键借币18: 分润22: 一键还债|
|subType|String|否|账单子类型1：买入2：卖出3：开多4：开空5：平多6：平空9：市场借币扣息11：转入12：转出14：尊享借币扣息160：手动追加保证金161：手动减少保证金162：自动追加保证金114：自动换币买入115：自动换币卖出118：系统换币转入119：系统换币转出100：强减平多101：强减平空102：强减买入103：强减卖出104：强平平多105：强平平空106：强平买入107：强平卖出110：强平换币转入111：强平换币转出125：自动减仓平多126：自动减仓平空127：自动减仓买入128：自动减仓卖出131：对冲买入132：对冲卖出170：到期行权171：到期被行权172：到期作废112：交割平多113：交割平空117：交割/期权穿仓补偿173：资金费支出174：资金费收入200:系统转入201:手动转入202:系统转出203:手动转出204: 大宗交易买205: 大宗交易卖206: 大宗交易开多207: 大宗交易开空208: 大宗交易平多209: 大宗交易平空210: 手动借币211: 手动还币212: 自动借币213：自动还币"16：强制还币17：强制借币还息224: 还债转入225: 还债转出250: 分润支出;251: 分润退还;252: 分润收入;|
|after|String|否|请求此id之前（更旧的数据）的分页内容，传的值为对应接口的billId|
|before|String|否|请求此id之后（更新的数据）的分页内容，传的值为对应接口的billId|
|begin|String|否|筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085|
|end|String|否|筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 9.2.6 账单流水查询（近三月） get_bills_archive

请求路径：/api/v5/account/bills-archive 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|否|产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|ccy|String|否|账单币种|
|mgnMode|String|否|仓位类型isolated：逐仓cross：全仓|
|ctType|String|否|linear： 正向合约inverse： 反向合约仅交割/永续有效|
|type|String|否|账单类型1：划转2：交易3：交割4：自动换币5：强平6：保证金划转7：扣息8：资金费9：自动减仓10：穿仓补偿11：系统换币12：策略划拨13：对冲减仓14: 大宗交易15: 一键借币22: 一键还债18: 分润|
|subType|String|否|账单子类型1：买入2：卖出3：开多4：开空5：平多6：平空9：市场借币扣息11：转入12：转出14：尊享借币扣息160：手动追加保证金161：手动减少保证金162：自动追加保证金114：自动换币买入115：自动换币卖出118：系统换币转入119：系统换币转出100：强减平多101：强减平空102：强减买入103：强减卖出104：强平平多105：强平平空106：强平买入107：强平卖出110：强平换币转入111：强平换币转出125：自动减仓平多126：自动减仓平空127：自动减仓买入128：自动减仓卖出131：对冲买入132：对冲卖出170：到期行权171：到期被行权172：到期作废112：交割平多113：交割平空117：交割/期权穿仓补偿173：资金费支出174：资金费收入200:系统转入201:手动转入202:系统转出203:手动转出204: 大宗交易买205: 大宗交易卖206: 大宗交易开多207: 大宗交易开空208: 大宗交易平多209: 大宗交易平空210: 手动借币211: 手动还币212: 自动借币213：自动还币"16：强制还币17：强制借币还息224: 还债转入225: 还债转出250: 分润支出;251: 分润退还;252: 分润收入;|
|after|String|否|请求此id之前（更旧的数据）的分页内容，传的值为对应接口的billId|
|before|String|否|请求此id之后（更新的数据）的分页内容，传的值为对应接口的billId|
|begin|String|否|筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085|
|end|String|否|筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 9.2.7 查看账户配置 get_config

请求路径：/api/v5/account/config 请求方法：GET

请求参数：无


#### 9.2.8 设置持仓模式 set_position_mode

请求路径：/api/v5/account/set-position-mode 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|posMode|String|是|持仓方式long_short_mode：双向持仓net_mode：单向持仓仅适用交割/永续|



#### 9.2.9 设置杠杆倍数 set_leverage

请求路径：/api/v5/account/set-leverage 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|lever|String|是|杠杆倍数|
|mgnMode|String|是|保证金模式isolated：逐仓cross：全仓如果ccy有效传值，该参数值只能为cross。|
|instId|String|可选|产品ID：币对、合约instId和ccy至少要传一个；如果两个都传，默认使用instId|
|ccy|String|可选|保证金币种仅适用于跨币种保证金模式的全仓币币杠杆。设置自动借币的杠杆倍数时必填|
|posSide|String|可选|持仓方向long：双向持仓多头short：双向持仓空头仅适用于逐仓交割/永续在双向持仓且保证金模式为逐仓条件下必填|



#### 9.2.10 获取最大可买卖/开仓数量 get_max_size

请求路径：/api/v5/account/max-size 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔|
|tdMode|String|是|交易模式cross：全仓isolated：逐仓cash：非保证金|
|ccy|String|可选|保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单|
|px|String|否|委托价格当不填委托价时会按当前最新成交价计算当指定多个产品ID查询时，忽略该参数，按当前最新成交价计算|
|leverage|String|否|开仓杠杆倍数默认为当前杠杆倍数仅适用于币币杠杆/交割/永续|
|unSpotOffset|Boolean|否|true：禁止现货对冲，false：允许现货对冲默认为false仅适用于组合保证金模式开启现货对冲模式下有效，否则忽略此参数。|



#### 9.2.11 获取最大可用数量 get_max_avail_size

请求路径：/api/v5/account/max-avail-size 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔|
|tdMode|String|是|交易模式cross：全仓isolated：逐仓cash：非保证金|
|ccy|String|可选|保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单|
|reduceOnly|Boolean|否|是否为只减仓模式，仅适用于币币杠杆|
|unSpotOffset|Boolean|否|true：禁止现货对冲，false：允许现货对冲默认为false仅适用于组合保证金模式开启现货对冲模式下有效，否则忽略此参数。|
|quickMgnType|String|否|一键借币类型，仅适用于杠杆逐仓的一键借币模式：manual：手动，auto_borrow： 自动借币，auto_repay： 自动还币默认是manual：手动|



#### 9.2.12 调整保证金 set_margin_balance

请求路径：/api/v5/account/position/margin-balance 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID|
|posSide|String|是|持仓方向，默认值是netlong：双向持仓多头short：双向持仓空头net：单向持仓|
|type|String|是|增加/减少保证金add：增加，或者转入质押资产(一键借币)reduce：减少，或者转出质押资产（一键借币）|
|amt|String|是|增加或减少的保证金数量|
|ccy|String|否|增加或减少的保证金的币种，仅适用于逐仓自主划转和一键借币模式下的币币杠杆|
|auto|Boolean|否|是否自动借币转 true 或 false，默认false仅适用于逐仓自主划转保证金模式下的币币杠杆|
|loanTrans|Boolean|否|是否支持跨币种保证金模式或组合保证金模式下的借币转入/转出true 或 false，默认false|



#### 9.2.13 获取杠杆倍数 get_leverage_info

请求路径：/api/v5/account/leverage-info 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID支持多个instId查询，半角逗号分隔。instId个数不超过20个|
|mgnMode|String|是|保证金模式isolated：逐仓cross：全仓|



#### 9.2.14 获取交易产品最大可借 get_max_loan

请求路径：/api/v5/account/max-loan 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品 ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔|
|mgnMode|String|是|仓位类型isolated：逐仓cross：全仓|
|mgnCcy|String|可选|保证金币种，如BTC币币杠杆单币种全仓情况下必须指定保证金币种|



#### 9.2.15 获取当前账户交易手续费费率 get_trade_fee

请求路径：/api/v5/account/trade-fee 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|instId|String|否|产品ID，如BTC-USDT仅适用于instType为币币/币币杠杆|
|uly|String|否|标的指数适用于交割/永续/期权，如BTC-USD|
|instFamily|String|否|交易品种适用于交割/永续/期权，如BTC-USD|



#### 9.2.16 获取计息记录 get_interest_accrued

请求路径：/api/v5/account/interest-accrued 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|type|String|否|借币类型1：尊享借币2：市场借币默认为市场借币|
|ccy|String|否|借贷币种，如BTC仅适用于市场借币仅适用于币币杠杆|
|instId|String|否|产品ID，如BTC-USDT仅适用于市场借币|
|mgnMode|String|否|保证金模式cross：全仓isolated：逐仓仅适用于市场借币|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 9.2.17 获取用户当前杠杆借币利率 get_interest_rate

请求路径：/api/v5/account/interest-rate 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种|



#### 9.2.18 期权greeks的PA/BS切换 set_greeks

请求路径：/api/v5/account/set-greeks 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|greeksType|String|是|希腊字母展示方式PA：币本位，BS：美元本位|



#### 9.2.19 逐仓交易设置 set_isolated_mode

请求路径：/api/v5/account/set-isolated-mode 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|isoMode|String|是|逐仓保证金划转模式automatic:开仓自动划转autonomy:自主划转quick_margin:一键借币|
|type|String|是|业务线类型MARGIN:币币杠杆CONTRACTS:合约|



#### 9.2.20 查看账户最大可转余额 get_max_withdrawal

请求路径：/api/v5/account/max-withdrawal 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔|



#### 9.2.21 查看账户特定风险状态 get_risk_state

请求路径：/api/v5/account/risk-state 请求方法：GET

请求参数：无


#### 9.2.22 一键借币模式手动借币还币 set_quick_margin_borrow_repay

请求路径：/api/v5/account/quick-margin-borrow-repay 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT|
|ccy|String|是|借贷币种，如BTC|
|side|String|是|borrow：借币，repay：还币|
|amt|String|是|借/还币的数量|



#### 9.2.23 获取一键借币还币历史 get_quick_margin_borrow_repay_history

请求路径：/api/v5/account/quick-margin-borrow-repay-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|否|产品ID，如 BTC-USDT|
|ccy|String|否|借贷币种，如BTC|
|side|String|否|borrow：借币，repay：还币|
|after|String|否|请求此 ID 之前（更旧的数据）的分页内容，传的值为对应接口的refId|
|before|String|否|请求此 ID 之后（更新的数据）的分页内容，传的值为对应接口的refId|
|begin|String|否|筛选的开始时间戳，Unix 时间戳为毫秒数格式，如 1597026383085|
|end|String|否|筛选的结束时间戳，Unix 时间戳为毫秒数格式，如 1597027383085|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 9.2.24 尊享借币还币 set_borrow_repay

请求路径：/api/v5/account/borrow-repay 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|借贷币种，如BTC|
|side|String|是|borrow：借币，repay：还币|
|amt|String|是|借/还币的数量|
|ordId|String|可选|借币订单ID，还币时，该字段必填|



#### 9.2.25 获取尊享借币还币历史 get_borrow_repay_history

请求路径：/api/v5/account/borrow-repay-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|借贷币种，如BTC|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 9.2.26 获取尊享借币计息记录 get_vip_interest_accrued

请求路径：/api/v5/account/vip-interest-accrued 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|借贷币种，如BTC，仅适用于币币杠杆|
|ordId|String|否|借币订单ID|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 9.2.27 获取尊享借币扣息记录 get_vip_interest_deducted

请求路径：/api/v5/account/vip-interest-deducted 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ordId|String|否|借币订单ID|
|ccy|String|否|借贷币种，如BTC，仅适用于币币杠杆|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 9.2.28 尊享借币订单列表 get_vip_loan_order_list

请求路径：/api/v5/account/vip-loan-order-list 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ordId|String|否|借币订单ID|
|state|String|否|订单状态1:借币申请中2:借币中3:还币申请中4:已还币5:借币失败|
|ccy|String|否|借贷币种，如 BTC|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 9.2.29 尊享借币订单详情 get_vip_loan_order_detail

请求路径：/api/v5/account/vip-loan-order-detail 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ordId|String|是|借币订单ID|
|ccy|String|否|借贷币种，如 BTC|
|after|String|否|请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|before|String|否|请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 9.2.30 获取借币利率与限额 get_interest_limits

请求路径：/api/v5/account/interest-limits 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|type|String|否|借币类型1：尊享借币2：市场借币默认为市场借币|
|ccy|String|否|借贷币种，如BTC|



#### 9.2.31 组合保证金的虚拟持仓保证金计算 set_simulated_margin

请求路径：/api/v5/account/simulated_margin 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|否|产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权|
|inclRealPos|Boolean|否|是否代入已有仓位true：调整被代入的已有仓位信息false：不代入已有仓位，仅使用simPos里新增的模拟仓位进行计算,默认为True|
|spotOffsetType|String|否|现货对冲模式1：现货对冲模式U模式 2：现货对冲模式币模式 3：衍生品模式默认是 3|
|simPos|Array|否|调整持仓列表|
|> instId|String|否|交易产品ID|
|> pos|String|否|持仓量|



#### 9.2.32 查看账户Greeks get_greeks

请求路径：/api/v5/account/greeks 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC|



#### 9.2.33 获取组合保证金模式全仓限制 get_position_tiers

请求路径：/api/v5/account/position-tiers 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|可选|标的指数，如BTC-USDT，支持多个查询（不超过3个），uly之间半角逗号分隔适用于交割/永续/期权uly与instFamily必须传一个,若传两个，以instFamily为主|
|instFamily|String|可选|交易品种，如BTC-USDT，支持多个查询（不超过5个），instFamily之间半角逗号分隔适用于交割/永续/期权uly与instFamily必须传一个,若传两个，以instFamily为主|



#### 9.2.34 设置组合保证金账户风险对冲模式 set_riskOffset_type

请求路径：/api/v5/account/set-riskOffset-type 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|type|String|是|风险对冲模式1：现货对冲(USDT)2:现货对冲(币)3:衍生品对冲|



#### 9.2.35 开通期权交易 set_activate_option

请求路径：/api/v5/account/activate-option 请求方法：POST

请求参数：无

### 9.3 例子

账户模块需要秘钥

```python
from okx import Account
from pprint import pprint

if __name__ == '__main__':
  # 账户模块需要秘钥
  key = '****'
  secret = '****'
  passphrase = '****'
  flag = '0'

  account = Account(key, secret, passphrase, flag)

  # 查看账户USDT余额
  result = account.get_balance('USDT')
  pprint(result)
```

输出：

```text
>> {'code': '0',
>>  'data': [{'adjEq': '',
>>            'details': [{'availBal': '498.00000000169007',
>>                         'availEq': '498.00000000169007',
>>                         'cashBal': '500.00000000169007',
>>                         'ccy': 'USDT',
>>                         'crossLiab': '',
>>                         'disEq': '500.00000000169007',
>>                         'eq': '500.00000000169007',
>>                         'eqUsd': '500.00000000169007',
>>                         'fixedBal': '0',
>>                         'frozenBal': '2',
>>                         'interest': '',
>>                         'isoEq': '0',
>>                         'isoLiab': '',
>>                         'isoUpl': '0',
>>                         'liab': '',
>>                         'maxLoan': '',
>>                         'mgnRatio': '',
>>                         'notionalLever': '0',
>>                         'ordFrozen': '2',
>>                         'spotInUseAmt': '',
>>                         'stgyEq': '0',
>>                         'twap': '0',
>>                         'uTime': '1672592968994',
>>                         'upl': '0',
>>                         'uplLiab': ''}],
>>            'imr': '',
>>            'isoEq': '0',
>>            'mgnRatio': '',
>>            'mmr': '',
>>            'notionalUsd': '',
>>            'ordFroz': '',
>>            'totalEq': '500.22421655441127',
>>            'uTime': '1675570865890'}],
>>  'msg': ''}
```

## 10 子账户 SubAccount 

### 10.1 子账户接口总览

|接口名称|函数名称|
|:---|:---|
|查看子账户列表|get_list|
|重置子账户的APIKey|set_modify_apikey|
|获取子账户交易账户余额|get_account_balances|
|获取子账户资金账户余额|get_asset_balances|
|查询子账户转账记录|get_bills|
|子账户间资金划转|set_transfer|
|设置子账户主动转出权限|set_transfer_out|
|查看被托管的子账户列表|get_entrust_subaccount_list|
|获取用户的节点返佣信息|get_if_rebate|

### 10.2 子账户接口介绍

#### 10.2.1 查看子账户列表 get_list

请求路径：/api/v5/users/subaccount/list 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|enable|String|否|子账户状态，true：正常使用false：冻结|
|subAcct|String|否|子账户名称|
|after|String|否|查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式|
|before|String|否|查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 10.2.2 重置子账户的APIKey set_modify_apikey

请求路径：/api/v5/users/subaccount/modify-apikey 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|subAcct|String|是|子账户名称|
|apiKey|String|是|子账户API的公钥|
|label|String|否|子账户APIKey的备注，如果填写该字段，则该字段会被重置|
|perm|String|否|子账户APIKey权限read_only：只读 ；trade：交易多个权限用半角逗号隔开。如果填写该字段，则该字段会被重置|
|ip|String|否|子账户APIKey绑定ip地址，多个ip用半角逗号隔开，最多支持20个ip。如果填写该字段，那该字段会被重置如果ip传""，则表示解除IP绑定|



#### 10.2.3 获取子账户交易账户余额 get_account_balances

请求路径：/api/v5/account/subaccount/balances 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|subAcct|String|是|子账户名称|



#### 10.2.4 获取子账户资金账户余额 get_asset_balances

请求路径：/api/v5/asset/subaccount/balances 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔|



#### 10.2.5 查询子账户转账记录 get_bills

请求路径：/api/v5/asset/subaccount/bills 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种，如 BTC|
|type|String|否|0: 母账户转子账户  ；1: 子账户转母账户|
|subAcct|String|否|子账户名称|
|after|String|否|查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式|
|before|String|否|查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 10.2.6 子账户间资金划转 set_transfer

请求路径：/api/v5/asset/subaccount/transfer 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|amt|String|是|划转数量|
|from|String|是|6：资金账户18：交易账户|
|to|String|是|6：资金账户18：交易账户|
|fromSubAccount|String|是|转出子账户的子账户名称|
|toSubAccount|String|是|转入子账户的子账户名称|
|loanTrans|Boolean|否|是否支持跨币种保证金模式或组合保证金模式下的借币转入/转出true 或 false，默认false|
|omitPosRisk|String|否|是否忽略仓位风险默认为false仅适用于组合保证金模式|



#### 10.2.7 设置子账户主动转出权限 set_transfer_out

请求路径：/api/v5/users/subaccount/set-transfer-out 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|subAcct|String|是|子账户名称，支持设置多个（不超过20个），子账户名称之间半角逗号分隔|
|canTransOut|Boolean|否|是否可以主动转出，默认为truefalse：不可转出true：可以转出|



#### 10.2.8 查看被托管的子账户列表 get_entrust_subaccount_list

请求路径：/api/v5/users/entrust-subaccount-list 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|subAcct|String|否|子账户名称|



#### 10.2.9 获取用户的节点返佣信息 get_if_rebate

请求路径：/api/v5/users/partner/if-rebate 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|apiKey|String|是|用户的 API key|

### 10.3 例子

子账户模块需要秘钥

```python
from okx import SubAccount
from pprint import pprint

if __name__ == '__main__':
  # 子账户模块需要秘钥
  key = '****'
  secret = '****'
  passphrase = '****'
  flag = '0'

  subAccount = SubAccount(key, secret, passphrase, flag)

  # 查看子账户列表
  result = subAccount.get_list()
  pprint(result)
```

输出：

```text
>> {'code': '0', 'data': [], 'msg': ''}
```

## 11 网格交易 Grid

### 11.1 网格交易接口总览


|接口名称|函数名称|
|:---|:---|
|网格策略委托下单|set_order_algo|
|修改网格策略订单|set_amend_order_algo|
|网格策略停止|set_stop_order_algo|
|获取未完成网格策略委托单列表|get_orders_algo_pending|
|获取历史网格策略委托单列表|get_orders_algo_history|
|获取网格策略委托订单详情|get_orders_algo_details|
|获取网格策略委托子订单信息|get_sub_orders|
|获取网格策略委托持仓|get_positions|
|现货/天地网格提取利润|set_withdraw_income|
|调整保证金计算|set_compute_margin_balance|
|调整保证金|set_margin_balance|
|网格策略智能回测（公共）|get_ai_param|

### 11.2 网格交易接口介绍

#### 11.2.1 网格策略委托下单 set_order_algo

请求路径：/api/v5/tradingBot/grid/order-algo 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT|
|algoOrdType|String|是|策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托|
|maxPx|String|是|区间最高价格|
|minPx|String|是|区间最低价格|
|gridNum|String|是|网格数量|
|runType|String|否|网格类型1：等差，2：等比默认为等差天地网格只支持2|
|tpTriggerPx|String|否|止盈触发价适用于现货网格/合约网格|
|slTriggerPx|String|否|止损触发价适用于现货网格/合约网格|
|tag|String|否|订单标签|



#### 11.2.2 修改网格策略订单 set_amend_order_algo

请求路径：/api/v5/tradingBot/grid/amend-order-algo 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoId|String|是|策略订单ID|
|instId|String|是|产品ID，如BTC-USDT-SWAP|
|slTriggerPx|String|可选|新的止损触发价当值为""则代表取消止损触发价slTriggerPx、tpTriggerPx至少要传一个值|
|tpTriggerPx|String|可选|新的止盈触发价当值为""则代表取消止盈触发价|



#### 11.2.3 网格策略停止 set_stop_order_algo

请求路径：/api/v5/tradingBot/grid/stop-order-algo 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoId|String|是|策略订单ID|
|instId|String|是|产品ID，如BTC-USDT|
|algoOrdType|String|是|策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托|
|stopType|String|是|网格策略停止类型现货网格/天地网格1：卖出交易币，2：不卖出交易币合约网格1：市价全平|



#### 11.2.4 获取未完成网格策略委托单列表 get_orders_algo_pending

请求路径：/api/v5/tradingBot/grid/orders-algo-pending 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoOrdType|String|是|策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托|
|algoId|String|否|策略订单ID|
|instId|String|否|产品ID，如BTC-USDT|
|instType|String|否|产品类型SPOT：币币MARGIN：杠杆FUTURES：交割合约SWAP：永续合约|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 11.2.5 获取历史网格策略委托单列表 get_orders_algo_history

请求路径：/api/v5/tradingBot/grid/orders-algo-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoOrdType|String|是|策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托|
|algoId|String|否|策略订单ID|
|instId|String|否|产品ID，如BTC-USDT|
|instType|String|否|产品类型SPOT：币币MARGIN：杠杆FUTURES：交割合约SWAP：永续合约|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的algoId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的algoId|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 11.2.6 获取网格策略委托订单详情 get_orders_algo_details

请求路径：/api/v5/tradingBot/grid/orders-algo-details 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoOrdType|String|是|策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托|
|algoId|String|是|策略订单ID|



#### 11.2.7 获取网格策略委托子订单信息 get_sub_orders

请求路径：/api/v5/tradingBot/grid/sub-orders 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoId|String|是|策略订单ID|
|algoOrdType|String|是|策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托|
|type|String|是|子订单状态live：未成交，filled：已成交|
|groupId|String|否|组ID|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId|
|limit|String|否|返回结果的数量，最大为100，默认100条|



#### 11.2.8 获取网格策略委托持仓 get_positions

请求路径：/api/v5/tradingBot/grid/positions 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoOrdType|String|是|订单类型contract_grid：合约网格委托|
|algoId|String|是|策略订单ID|



#### 11.2.9 现货/天地网格提取利润 set_withdraw_income

请求路径：/api/v5/tradingBot/grid/withdraw-income 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoId|String|是|策略订单ID|



#### 11.2.10 调整保证金计算 set_compute_margin_balance

请求路径：/api/v5/tradingBot/grid/compute-margin-balance 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoId|String|是|策略订单ID|
|type|String|是|调整保证金类型add：增加，reduce：减少|
|amt|String|否|调整保证金数量|



#### 11.2.11 调整保证金 set_margin_balance

请求路径：/api/v5/tradingBot/grid/margin-balance 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoId|String|是|策略订单ID|
|type|String|是|调整保证金类型add：增加，reduce：减少|
|amt|String|可选|调整保证金数量amt和percent必须传一个|
|percent|String|可选|调整保证金百分比|



#### 11.2.12 网格策略智能回测（公共） get_ai_param

请求路径：/api/v5/tradingBot/grid/ai-param 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|algoOrdType|String|是|策略订单类型grid：现货网格委托contract_grid：合约网格委托moon_grid：天地网格委托|
|instId|String|是|产品ID，如BTC-USDT|
|direction|String|可选|合约网格类型long：做多，short：做空，neutral：中性合约网格必填|
|duration|String|否|回测周期7D：7天，30D：30天，180D：180天默认现货网格为7D，天地网格为180D|

## 12 赚币 Staking 

### 12.1 赚币接口总览

|接口名称|函数名称|
|:---|:---|
|查看项目|get_offers|
|申购项目|set_purchase|
|赎回项目|set_redeem|
|撤销项目申购/赎回|set_cancel|
|查看活跃订单|get_orders_active|
|查看历史订单|get_orders_history|

### 12.2 赚币接口介绍

#### 12.2.1 查看项目 get_offers

请求路径：/api/v5/finance/staking-defi/offers 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|productId|String|否|项目ID|
|protocolType|String|否|项目类型staking：锁仓挖矿defi：DEFI|
|ccy|String|否|投资币种，如BTC|



#### 12.2.2 申购项目 set_purchase

请求路径：/api/v5/finance/staking-defi/purchase 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|productId|String|是|项目ID|
|investData|Array|是|投资信息|
|> ccy|String|是|投资币种，如BTC|
|> amt|String|是|投资数量|
|term|String|可选|投资期限定期项目必须指定投资期限|
|tag|String|否|订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间|



#### 12.2.3 赎回项目 set_redeem

请求路径：/api/v5/finance/staking-defi/redeem 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ordId|String|是|订单ID|
|protocolType|String|是|项目类型staking：锁仓挖矿defi：DEFI|
|allowEarlyRedeem|Boolean|否|是否提前赎回默认为false|



#### 12.2.4 撤销项目申购/赎回 set_cancel

请求路径：/api/v5/finance/staking-defi/cancel 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ordId|String|是|订单ID|
|protocolType|String|是|项目类型staking：锁仓挖矿defi：DEFI|



#### 12.2.5 查看活跃订单 get_orders_active

请求路径：/api/v5/finance/staking-defi/orders-active 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|productId|String|否|项目ID|
|protocolType|String|否|项目类型staking：锁仓挖矿defi：DEFI|
|ccy|String|否|投资币种，如BTC|
|state|String|否|订单状态8: 待上车（预约中）13: 订单取消中9: 上链中1: 收益中2: 赎回中|



#### 12.2.6 查看历史订单 get_orders_history

请求路径：/api/v5/finance/staking-defi/orders-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|productId|String|否|项目ID|
|protocolType|String|否|项目类型staking：锁仓挖矿defi：DEFI|
|ccy|String|否|投资币种，如BTC|
|after|String|否|请求此ID之前（更旧的数据）的分页内容，传的值为对应接口的ordId|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的ordId|
|limit|String|否|返回结果的数量，默认100条,最大值为100条|

### 12.3 例子

赚币模块需要秘钥

```python
from okx import Staking
from pprint import pprint

if __name__ == '__main__':
  # 赚币模块需要秘钥
  key = '****'
  secret = '****'
  passphrase = '****'
  flag = '0'

  staking = Staking(key, secret, passphrase, flag)

  # 查看项目
  result = staking.get_offers()
  pprint(result)
```

输出：

```text
>> {'code': '0',
>>  'data': [{'apy': '0.0673',
>>            'ccy': 'USDT',
>>            'earlyRedeem': False,
>>            'earningData': [{'ccy': 'SUSHI', 'earningType': '1'}],
>>            'investData': [{'bal': '1248.07712484',
>>                            'ccy': 'USDT',
>>                            'maxAmt': '0',
>>                            'minAmt': '100'},
>>                           {'bal': '0',
>>                            'ccy': 'ETH',
>>                            'maxAmt': '0',
>>                            'minAmt': '0.06017661'}],
>>            'productId': '1507',
>>            'protocol': 'Sushiswap',
>>            'protocolType': 'defi',
>>            'state': 'purchasable',
>>            'term': '0'},
>>            ... ...
>>         ]
>>  'msg': ''}
```

## 13 跟单接口CopyTrading 

**跟单接口权限需要单独申请**

### 13.1 跟单接口总览

|接口名称|函数名称|
|:---|:---|
|交易员获取当前带单|get_current_subpositions|
|交易员获取历史带单|get_subpositions_history|
|交易员止盈止损|set_algo_order|
|交易员平仓|set_close_subposition|
|交易员获取带单合约|get_instruments|
|交易员修改带单合约|set_instruments|
|交易员历史分润明细|get_profit_sharing_details|
|交易员历史分润汇总|get_total_profit_sharing|
|交易员待分润明细|get_unrealized_profit_sharing_details|

### 13.2 跟单接口介绍

#### 13.2.1 交易员获取当前带单 get_current_subpositions

请求路径：/api/v5/copytrading/current-subpositions 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|否|产品ID ，如BTC-USDT-SWAP|



#### 13.2.2 交易员获取历史带单 get_subpositions_history

请求路径：/api/v5/copytrading/subpositions-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|否|产品ID ，如BTC-USDT-SWAP|
|after|String|否|请求此id之前（更旧的数据）的分页内容，传的值为对应接口的subPosId|
|before|String|否|请求此id之后（更新的数据）的分页内容，传的值为对应接口的subPosId|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 13.2.3 交易员止盈止损 set_algo_order

请求路径：/api/v5/copytrading/algo-order 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|subPosId|String|是|带单仓位ID|
|tpTriggerPx|String|可选|止盈触发价，触发后以市价进行委托，tpTriggerPx 和 slTriggerPx 至少需要填写一个|
|slTriggerPx|String|可选|止损触发价，触发后以市价进行委托|
|tpTriggerPxType|String|否|止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last|
|slTriggerPxType|String|否|止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last|



#### 13.2.4 交易员平仓 set_close_subposition

请求路径：/api/v5/copytrading/close-subposition 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|subPosId|String|是|带单仓位ID|



#### 13.2.5 交易员获取带单合约 get_instruments

请求路径：/api/v5/copytrading/instruments 请求方法：GET

请求参数：无


#### 13.2.6 交易员修改带单合约 set_instruments

请求路径：/api/v5/copytrading/set-instruments 请求方法：POST

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如 BTC-USDT-SWAP，多个产品用半角逗号隔开，最多支持10个产品ID|



#### 13.2.7 交易员历史分润明细 get_profit_sharing_details

请求路径：/api/v5/copytrading/profit-sharing-details 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|after|String|否|请求此id之前（更旧的数据）的分页内容，传的值为对应接口的profitSharingId|
|before|String|否|请求此id之后（更新的数据）的分页内容，传的值为对应接口的profitSharingId|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 13.2.8 交易员历史分润汇总 get_total_profit_sharing

请求路径：/api/v5/copytrading/total-profit-sharing 请求方法：GET

请求参数：无


#### 13.2.9 交易员待分润明细 get_unrealized_profit_sharing_details

请求路径：/api/v5/copytrading/unrealized-profit-sharing-details 请求方法：GET

请求参数：无



## 14 行情数据 Market 

### 14.1 行情数据接口总览

|接口名称|函数名称|
|:---|:---|
|获取所有产品行情信息|get_tickers|
|获取单个产品行情信息|get_ticker|
|获取指数行情|get_index_tickers|
|获取产品深度|get_books|
|获取产品轻量深度|get_books_lite|
|获取交易产品K线数据|get_candles|
|获取交易产品历史K线数据|get_history_candles|
|获取指数K线数据|get_index_candles|
|获取指数历史K线数据|get_history_index_candles|
|获取标记价格K线数据|get_mark_price_candles|
|获取标记价格历史K线数据|get_history_mark_price_candles|
|获取交易产品公共成交数据|get_trades|
|获取交易产品公共历史成交数据|get_history_trades|
|获取期权品种公共成交数据|get_instrument_family_trades|
|获取平台24小时总成交量|get_platform_24_volume|
|Oracle  上链交易数据|get_open_oracle|
|获取法币汇率|get_exchange_rate|
|获取指数成分数据|get_index_components|
|获取大宗交易所有产品行情信息|get_block_tickers|
|获取大宗交易单个产品行情信息|get_block_ticker|
|获取大宗交易公共成交数据|get_block_trades|

### 14.2 行情数据接口介绍

#### 14.2.1 获取所有产品行情信息 get_tickers

请求路径：/api/v5/market/tickers 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|否|标的指数适用于交割/永续/期权，如BTC-USD|
|instFamily|String|否|交易品种适用于交割/永续/期权，如BTC-USD|



#### 14.2.2 获取单个产品行情信息 get_ticker

请求路径：/api/v5/market/ticker 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如 BTC-USD-SWAP|


#### 14.2.3 获取指数行情 get_index_tickers

请求路径：/api/v5/market/index-tickers 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|quoteCcy|String|可选|指数计价单位， 目前只有USD/USDT/BTC为计价单位的指数，quoteCcy和instId必须填写一个|
|instId|String|可选|指数，如BTC-USD|



#### 14.2.4 获取产品深度 get_books

请求路径：/api/v5/market/books 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT|
|sz|String|否|深度档位数量，最大值可传400，即买卖深度共800条不填写此参数，默认返回1档深度数据|



#### 14.2.5 获取产品轻量深度 get_books_lite

请求路径：/api/v5/market/books-lite 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT|



#### 14.2.6 获取交易产品K线数据 get_candles

请求路径：/api/v5/market/candles 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USD-190927-5000-C|
|bar|String|否|时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts|
|limit|String|否|分页返回的结果集数量，最大为300，不填默认返回100条|



#### 14.2.7 获取交易产品历史K线数据 get_history_candles

请求路径：/api/v5/market/history-candles 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USD-200927|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts|
|bar|String|否|时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 14.2.8 获取指数K线数据 get_index_candles

请求路径：/api/v5/market/index-candles 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|现货指数，如BTC-USD|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts|
|bar|String|否|时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M/3M]UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/1Wutc/1Mutc/3Mutc]|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 14.2.9 获取指数历史K线数据 get_history_index_candles

请求路径：/api/v5/market/history-index-candles 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|现货指数，如BTC-USD|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts|
|bar|String|否|时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M]UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/1Wutc/1Mutc]|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 14.2.10 获取标记价格K线数据 get_mark_price_candles

请求路径：/api/v5/market/mark-price-candles 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USD-SWAP|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts|
|bar|String|否|时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M/3M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/1Wutc/1Mutc/3Mutc]|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 14.2.11 获取标记价格历史K线数据 get_history_mark_price_candles

请求路径：/api/v5/market/history-mark-price-candles 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USD-SWAP|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts|
|bar|String|否|时间粒度，默认值1m如 [1m/3m/5m/15m/30m/1H/2H/4H]香港时间开盘价k线：[6H/12H/1D/1W/1M]UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/1Wutc/1Mutc]|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 14.2.12 获取交易产品公共成交数据 get_trades

请求路径：/api/v5/market/trades 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT|
|limit|String|否|分页返回的结果集数量，最大为500，不填默认返回100条|



#### 14.2.13 获取交易产品公共历史成交数据 get_history_trades

请求路径：/api/v5/market/history-trades 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT|
|type|String|否|分页类型1：tradeId 分页2：时间戳分页默认为1：tradeId 分页|
|after|String|否|请求此 ID 或 ts 之前的分页内容，传的值为对应接口的 tradeId 或 ts|
|before|String|否|请求此ID之后（更新的数据）的分页内容，传的值为对应接口的 tradeId。不支持时间戳分页。|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 14.2.14 获取期权品种公共成交数据 get_instrument_family_trades

请求路径：/api/v5/market/option/instrument-family-trades 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instFamily|String|是|交易品种，如 BTC-USD，适用于期权|



#### 14.2.15 获取平台24小时总成交量 get_platform_24_volume

请求路径：/api/v5/market/platform-24-volume 请求方法：GET

请求参数：无


#### 14.2.16 Oracle  上链交易数据 get_open_oracle

请求路径：/api/v5/market/open-oracle 请求方法：GET

请求参数：无


#### 14.2.17 获取法币汇率 get_exchange_rate

请求路径：/api/v5/market/exchange-rate 请求方法：GET

请求参数：无


#### 14.2.18 获取指数成分数据 get_index_components

请求路径：/api/v5/market/index-components 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|index|String|是|指数，如BTC-USDT|



#### 14.2.19 获取大宗交易所有产品行情信息 get_block_tickers

请求路径：/api/v5/market/block-tickers 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SPOT：币币SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|否|标的指数适用于交割/永续/期权，如BTC-USD|
|instFamily|String|否|交易品种适用于交割/永续/期权，如BTC-USD|



#### 14.2.20 获取大宗交易单个产品行情信息 get_block_ticker

请求路径：/api/v5/market/block-ticker 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如 BTC-USD-SWAP|


#### 14.2.21 获取大宗交易公共成交数据 get_block_trades

请求路径：/api/v5/market/block-trades 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT|

### 14.3 例子

**行情数据模块无需秘钥**

```python
from okx import Market
from pprint import pprint

if __name__ == '__main__':
  # 行情数据模块无需秘钥
  key = ''
  secret = ''
  passphrase = ''
  flag = '0'

  market = Market(key, secret, passphrase, flag)
  # 获取所有产品行情信息
  result = market.get_tickers(instType='SPOT')  # SPOT币币
  pprint(result)
```

输出：

```text
>> {'code': '0',
>>  'data': [{'askPx': '0.00000666',
>>            'askSz': '38.2674',
>>            'bidPx': '0.00000657',
>>            'bidSz': '280.5009',
>>            'high24h': '0.00000685',
>>            'instId': 'BCD-BTC',
>>            'instType': 'SPOT',
>>            'last': '0.00000664',
>>            'lastSz': '12.2992',
>>            'low24h': '0.00000644',
>>            'open24h': '0.00000656',
>>            'sodUtc0': '0.00000658',
>>            'sodUtc8': '0.00000674',
>>            'ts': '1675572360017',
>>            'vol24h': '40196.8587',
>>            'volCcy24h': '0.2515'},
>>            ... ...
>>         ],
>>  'msg': ''}
```


## 15 公共数据 Public 

### 15.1 公共数据接口总览

|接口名称|函数名称|
|:---|:---|
|获取交易产品基础信息|get_instruments|
|获取交割和行权记录|get_delivery_exercise_history|
|获取持仓总量|get_open_interest|
|获取永续合约当前资金费率|get_funding_rate|
|获取永续合约历史资金费率|get_funding_rate_history|
|获取限价|get_price_limit|
|获取期权定价|get_opt_summary|
|获取预估交割/行权价格|get_estimated_price|
|获取免息额度和币种折算率等级|get_discount_rate_interest_free_quota|
|获取系统时间|get_time|
|获取平台公共爆仓单信息|get_liquidation_orders|
|获取标记价格|get_mark_price|
|获取衍生品仓位档位|get_position_tiers|
|获取市场借币杠杆利率和借币限额|get_interest_rate_loan_quota|
|获取尊享借币杠杆利率和借币限额|get_vip_interest_rate_loan_quota|
|获取衍生品标的指数|get_underlying|
|获取风险准备金余额|get_insurance_fund|
|张币转换|get_convert_contract_coin|
|获取期权公共成交数据|get_option_trades|

### 15.2 公共数据接口介绍

#### 15.2.1 获取交易产品基础信息 get_instruments

请求路径：/api/v5/public/instruments 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|可选|标的指数，仅适用于交割/永续/期权，期权必填|
|instFamily|String|否|交易品种，仅适用于交割/永续/期权|
|instId|String|否|产品ID|



#### 15.2.2 获取交割和行权记录 get_delivery_exercise_history

请求路径：/api/v5/public/delivery-exercise-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型FUTURES：交割合约OPTION：期权|
|uly|String|可选|标的指数uly与instFamily必须传一个,若传两个，以instFamily为主|
|instFamily|String|可选|交易品种uly与instFamily必须传一个,若传两个，以instFamily为主|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 15.2.3 获取持仓总量 get_open_interest

请求路径：/api/v5/public/open-interest 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|可选|标的指数适用于交割/永续/期权期权情况下，uly和instFamily必须传一个|
|instFamily|String|可选|交易品种适用于交割/永续/期权期权情况下，uly和instFamily必须传一个|
|instId|String|否|产品ID，如BTC-USD-180216仅适用于交割/永续/期权|



#### 15.2.4 获取永续合约当前资金费率 get_funding_rate

请求路径：/api/v5/public/funding-rate 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID ，如BTC-USD-SWAP仅适用于永续|



#### 15.2.5 获取永续合约历史资金费率 get_funding_rate_history

请求路径：/api/v5/public/funding-rate-history 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID ，如BTC-USD-SWAP仅适用于永续|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的fundingTime|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的fundingTime|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 15.2.6 获取限价 get_price_limit

请求路径：/api/v5/public/price-limit 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，如BTC-USDT-SWAP仅适用于交割/永续/期权|



#### 15.2.7 获取期权定价 get_opt_summary

请求路径：/api/v5/public/opt-summary 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|uly|String|可选|标的指数，仅适用于期权uly与instFamily必须传一个,若传两个，以instFamily为主|
|instFamily|String|可选|交易品种，仅适用于期权uly与instFamily必须传一个,若传两个，以instFamily为主|
|expTime|String|否|合约到期日，格式为"YYMMDD"，如 "200527"|



#### 15.2.8 获取预估交割/行权价格 get_estimated_price

请求路径：/api/v5/public/estimated-price 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID， 如BTC-USD-200214仅适用于交割/期权|



#### 15.2.9 获取免息额度和币种折算率等级 get_discount_rate_interest_free_quota

请求路径：/api/v5/public/discount-rate-interest-free-quota 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|否|币种|
|discountLv|String|否|折算率等级1:第一档2:第二档3:第三档4:第四档5:第五档|



#### 15.2.10 获取系统时间 get_time

请求路径：/api/v5/public/time 请求方法：GET

请求参数：无


#### 15.2.11 获取平台公共爆仓单信息 get_liquidation_orders

请求路径：/api/v5/public/liquidation-orders 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|mgnMode|String|否|保证金模式cross：全仓isolated：逐仓|
|instId|String|否|产品ID，仅适用于币币杠杆|
|ccy|String|否|币种 ，仅适用于币币杠杆（全仓）|
|uly|String|可选|标的指数交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主|
|instFamily|String|可选|交易品种交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主|
|alias|String|可选|this_week：本周next_week：次周quarter：季度next_quarter：次季度交割合约情况下，该参数必填|
|state|String|否|状态unfilled：未成交filled：已成交默认为unfilled交割/永续合约情况下，该参数必填|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 15.2.12 获取标记价格 get_mark_price

请求路径：/api/v5/public/mark-price 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|uly|String|否|标的指数适用于交割/永续/期权|
|instFamily|String|否|交易品种适用于交割/永续/期权|
|instId|String|否|产品ID，如BTC-USD-SWAP|



#### 15.2.13 获取衍生品仓位档位 get_position_tiers

请求路径：/api/v5/public/position-tiers 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|tdMode|String|是|保证金模式isolated：逐仓 ；cross：全仓|
|uly|String|可选|标的指数，支持多uly，半角逗号分隔，最大不超过3个当产品类型是永续、交割、期权之一时，uly与instFamily必须传一个，若传两个，以instFamily为主当产品类型是MARGIN时忽略|
|instFamily|String|可选|交易品种，支持多instFamily，半角逗号分隔，最大不超过5个当产品类型是永续、交割、期权之一时，uly与instFamily必须传一个，若传两个，以instFamily为主|
|instId|String|可选|产品ID，支持多instId，半角逗号分隔，最大不超过5个仅适用币币杠杆，instId和ccy必须传一个，若传两个，以instId为主|
|ccy|String|可选|保证金币种仅适用杠杆全仓，该值生效时，返回的是跨币种保证金模式和组合保证金模式下的借币量|
|tier|String|否|查指定档位|



#### 15.2.14 获取市场借币杠杆利率和借币限额 get_interest_rate_loan_quota

请求路径：/api/v5/public/interest-rate-loan-quota 请求方法：GET

请求参数：无


#### 15.2.15 获取尊享借币杠杆利率和借币限额 get_vip_interest_rate_loan_quota

请求路径：/api/v5/public/vip-interest-rate-loan-quota 请求方法：GET

请求参数：无


#### 15.2.16 获取衍生品标的指数 get_underlying

请求路径：/api/v5/public/underlying 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权|



#### 15.2.17 获取风险准备金余额 get_insurance_fund

请求路径：/api/v5/public/insurance-fund 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instType|String|是|产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权|
|type|String|否|风险准备金类型liquidation_balance_deposit：强平注入 ；bankruptcy_loss：穿仓亏损 ；platform_revenue：平台收入注入默认返回全部类型|
|uly|String|可选|标的指数交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主|
|instFamily|String|可选|交易品种交割/永续/期权情况下，uly与instFamily必须传一个，若传两个，以instFamily为主|
|ccy|String|可选|币种， 仅适用币币杠杆，且必填写|
|before|String|否|请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts|
|after|String|否|请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts|
|limit|String|否|分页返回的结果集数量，最大为100，不填默认返回100条|



#### 15.2.18 张币转换 get_convert_contract_coin

请求路径：/api/v5/public/convert-contract-coin 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|是|产品ID，仅适用于交割/永续/期权|
|sz|String|是|数量，币转张时，为币的数量，张转币时，为张的数量。张的数量，只能是正整数|
|type|String|否|转换类型1: 币转张，当张为小数时，会进一取整2: 张转币默认为 1|
|px|String|可选|委托价格币本位合约的张币转换时必填；U本位合约，usdt 与张的转换时，必填；coin 与张的转换时，可不填；期权的张币转换时，可不填。|
|unit|String|否|币的单位，coin: 币，usds: usdt 或者 usdc仅适用于交割和永续合约的U本位合约|



#### 15.2.19 获取期权公共成交数据 get_option_trades

请求路径：/api/v5/public/option-trades 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|instId|String|可选|产品ID，如 BTC-USD-221230-4000-C，instId和instFamily必须传一个，若传两个，以instId为主|
|instFamily|String|可选|交易品种，如 BTC-USD|
|optType|String|否|期权类型，C：看涨期权P：看跌期权|

### 15.3 例子

公共数据模块无需秘钥

```python
from okx import Public
from pprint import pprint

if __name__ == '__main__':
  # 公共数据模块无需秘钥
  key = ''
  secret = ''
  passphrase = ''
  flag = '0'

  public = Public(key, secret, passphrase, flag)
  # 获取交易产品基础信息
  result = public.get_instruments(instType='SWAP', instId='BTC-USDT-SWAP')
  pprint(result)
```

输出：

```text
>> {'code': '0',
>>  'data': [{'alias': '',
>>            'baseCcy': '',
>>            'category': '1',
>>            'ctMult': '1',
>>            'ctType': 'linear',
>>            'ctVal': '0.01',
>>            'ctValCcy': 'BTC',
>>            'expTime': '',
>>            'instFamily': 'BTC-USDT',
>>            'instId': 'BTC-USDT-SWAP',
>>            'instType': 'SWAP',
>>            'lever': '125',
>>            'listTime': '1611916828000',
>>            'lotSz': '1',
>>            'maxIcebergSz': '100000000',
>>            'maxLmtSz': '100000000',
>>            'maxMktSz': '10000',
>>            'maxStopSz': '10000',
>>            'maxTriggerSz': '100000000',
>>            'maxTwapSz': '100000000',
>>            'minSz': '1',
>>            'optType': '',
>>            'quoteCcy': '',
>>            'settleCcy': 'USDT',
>>            'state': 'live',
>>            'stk': '',
>>            'tickSz': '0.1',
>>            'uly': 'BTC-USDT'}],
>>  'msg': ''}
```

## 16 交易大数据 Rubik 

### 16.1 交易大数据接口总览

|接口名称|函数名称|
|:---|:---|
|获取交易大数据支持币种|get_support_coin|
|获取主动买入/卖出情况|get_taker_volume|
|获取杠杆多空比|get_loan_ratio|
|获取合约多空持仓人数比|get_long_short_account_ratio|
|获取合约持仓量及交易量|get_contracts_open_interest_volume|
|获取期权持仓量及交易量|get_option_open_interest_volume|
|看涨/看跌期权合约 持仓总量比/交易总量比|get_open_interest_volume_ratio|
|看涨看跌持仓总量及交易总量（按到期日分）|get_open_interest_volume_expiry|
|看涨看跌持仓总量及交易总量（按执行价格分）|get_open_interest_volume_strike|
|看跌/看涨期权合约 主动买入/卖出量|get_taker_block_volume|

### 16.2 交易大数据接口介绍

#### 16.2.1 获取交易大数据支持币种 get_support_coin

请求路径：/api/v5/rubik/stat/trading-data/support-coin 请求方法：GET

请求参数：无


#### 16.2.2 获取主动买入/卖出情况 get_taker_volume

请求路径：/api/v5/rubik/stat/taker-volume 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|instType|String|是|产品类型，币币："SPOT" , 衍生品："CONTRACTS"|
|begin|String|否|开始时间，例如：1597026383085|
|end|String|否|结束时间，例如：1597026383011|
|period|String|否|时间粒度，默认值5m。支持[5m/1H/1D]5m粒度最多只能查询两天之内的数据1H粒度最多只能查询30天之内的数据1D粒度最多只能查询180天之内的数据|



#### 16.2.3 获取杠杆多空比 get_loan_ratio

请求路径：/api/v5/rubik/stat/margin/loan-ratio 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|begin|String|否|开始时间，例如：1597026383085|
|end|String|否|结束时间，例如：1597026383011|
|period|String|否|时间粒度，默认值5m。支持[5m/1H/1D]5m粒度最多只能查询两天之内的数据1H粒度最多只能查询30天之内的数据1D粒度最多只能查询180天之内的数据|



#### 16.2.4 获取合约多空持仓人数比 get_long_short_account_ratio

请求路径：/api/v5/rubik/stat/contracts/long-short-account-ratio 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|begin|String|否|开始时间，例如：1597026383085|
|end|String|否|结束时间，例如：1597026383011|
|period|String|否|时间粒度，默认值5m。支持[5m/1H/1D]5m粒度最多只能查询两天之内的数据1H粒度最多只能查询30天之内的数据1D粒度最多只能查询180天之内的数据|



#### 16.2.5 获取合约持仓量及交易量 get_contracts_open_interest_volume

请求路径：/api/v5/rubik/stat/contracts/open-interest-volume 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|begin|String|否|开始时间，例如：1597026383085|
|end|String|否|结束时间，例如：1597026383011|
|period|String|否|时间粒度，默认值5m。支持[5m/1H/1D]5m粒度最多只能查询两天之内的数据1H粒度最多只能查询30天之内的数据1D粒度最多只能查询180天之内的数据|



#### 16.2.6 获取期权持仓量及交易量 get_option_open_interest_volume

请求路径：/api/v5/rubik/stat/option/open-interest-volume 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|period|String|否|时间粒度，默认值8H。支持[8H/1D]每个粒度最多只能查询72条数据|



#### 16.2.7 看涨/看跌期权合约 持仓总量比/交易总量比 get_open_interest_volume_ratio

请求路径：/api/v5/rubik/stat/option/open-interest-volume-ratio 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|period|String|否|时间粒度，默认值8H。支持[8H/1D]每个粒度最多只能查询72条数据|



#### 16.2.8 看涨看跌持仓总量及交易总量（按到期日分） get_open_interest_volume_expiry

请求路径：/api/v5/rubik/stat/option/open-interest-volume-expiry 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|period|String|否|时间粒度，默认值8H。支持[8H/1D]每个粒度最多只能查询72条数据|



#### 16.2.9 看涨看跌持仓总量及交易总量（按执行价格分） get_open_interest_volume_strike

请求路径：/api/v5/rubik/stat/option/open-interest-volume-strike 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|expTime|String|是|到期日（格式: YYYYMMdd，例如："20210623"）|
|period|String|否|时间粒度，默认值8H。支持[8H/1D]每个粒度最多只能查询72条数据|



#### 16.2.10 看跌/看涨期权合约 主动买入/卖出量 get_taker_block_volume

请求路径：/api/v5/rubik/stat/option/taker-block-volume 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|ccy|String|是|币种|
|period|String|否|时间粒度，默认值8H。支持[8H/1D]每个粒度最多只能查询72条数据|


### 16.3 例子

交易大数据模块无需秘钥

```python
from okx import Rubik
from pprint import pprint

if __name__ == '__main__':
  # 交易大数据模块无需秘钥
  key = ''
  secret = ''
  passphrase = ''
  flag = '0'

  rubik = Rubik(key, secret, passphrase, flag)
  # 获取主动买入/卖出情况
  result = rubik.get_taker_volume(instType='SPOT', ccy='BTC')
  pprint(result)

```

输出：

```text
>> {'code': '0',
>>  'data': [['1675572600000', '4.8369', '0.391'],
>>           ['1675572300000', '0.3481', '8.8288'],
>>           ['1675572000000', '0.7026', '1.421'],
>>           ['1675571700000', '1.3064', '0.9826'],
>>           ... ...
>>           ],
>>  'msg': ''}
```

## 17 Status（系统状态）System

### 17.1 Status接口总览

|接口名称|函数名称|
|:---|:---|
|获取系统升级事件的状态。|get_status|

### 17.2 Status接口介绍

#### 17.2.1 获取系统升级事件的状态 get_status


请求路径：/api/v5/system/status 请求方法：GET

请求参数：

|参数名|类型|是否必须|描述|
|:---|:---|:---|:---|
|state|String|No|系统的状态，scheduled:等待中 ; ongoing:进行中 ; pre_open:预开放；completed:已完成 canceled: 已取消 当维护时间过长，会存在预开放时间，一般持续10分钟左右。 不填写此参数，默认返回 等待中、进行中和预开放 的数据|


### 17.3 例子

System模块无需秘钥

```python
from okx import System
from pprint import pprint

if __name__ == '__main__':
  # System模块无需秘钥
  key = ''
  secret = ''
  passphrase = ''
  flag = '0'

  system = System(key, secret, passphrase, flag)
  # 获取系统升级事件的状态
  result = system.get_status()
  pprint(result)

```

输出：

```text
>> {'code': '0', 'data': [], 'msg': ''}
```
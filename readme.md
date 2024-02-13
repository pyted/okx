## OKX 2.1.0

安装：

```cmd
pip3 install okx==2.1.1
```

- 更新日期：2024-02-13
- 同步官方文档全部Rest接口 (2023年10月)
- 添加代理IP与代理服务器转发功能
- 部分模块名称有所改动
- **使用文档近期更新**

使用教程请参考examples

- 1.1 OKX（库）安装与介绍
- 1.2 API函数接口总览
- 1.3 API 行情接口.ipynb
- 1.4 API 交易账户.ipynb
- 1.5 API 基础交易接口.ipynb
- 1.6 API 公共数据.ipynb
- 2.1 APP 现货交易账户.ipynb
- 2.2 APP 现货行情-交易规则信息.ipynb
- 2.3 APP 现货行情-实时行情.ipynb
- 2.4 APP 现货行情-历史K线.ipynb
- 2.5 APP 现货交易-基础订单.ipynb
- 2.6 APP 现货交易-价格与数量.ipynb
- 2.7 APP 现货交易-限价单开仓.ipynb
- 2.8 APP 现货交易-市价单开仓.ipynb
- 2.9 APP 现货交易-限单价平仓.ipynb
- 2.10 APP 现货交易-市价单平仓.ipynb
- 3.1 APP 永续合约交易账户.ipynb
- 3.2 APP 永续合约行情-交易规则信息.ipynb
- 3.3 APP 永续合约行情-实时行情.ipynb
- 3.4 APP 永续合约行情-历史K线.ipynb
- 3.5 APP 永续合约交易-基础订单.ipynb
- 3.6 APP 永续合约交易-价格与数量.ipynb
- 3.7 APP 永续合约交易-限价单开仓.ipynb
- 3.8 APP 永续合约交易-市价单开仓.ipynb
- 3.9 APP 永续合约交易-限单价平仓.ipynb
- 3.10 APP 永续合约交易-市价单平仓.ipynb
- 4.1 APP K线服务 下载历史K线.ipynb
- 4.2 APP K线服务 每日定时下载昨日历史K线.ipynb
- 4.3 K线服务 维护实时历史K线.ipynb

v2.1.1 更新内容：

- 更新examples文档
- load模块支持columns字段，可以保留K线数据candle的指定列，以降低内存压力。
- APP模块中优化列表展示结果与字典展示结果
- setup安装中不在约束Numpy与Pandas的版本，提高安装兼容性

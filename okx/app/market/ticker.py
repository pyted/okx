from okx.app.market._base import MarketBase


class Ticker(MarketBase):

    # 获取所有产品的行情列表
    def get_tickers(self, instIds=[]) -> dict:
        api_tickers_result = self.marketAPI.get_tickers(instType=self.instType)
        if not instIds:
            return api_tickers_result
        if not api_tickers_result['code'] == '0':
            return api_tickers_result
        datas = []
        for _data in api_tickers_result['data']:
            if _data['instId'] in instIds:
                datas.append(_data)
        api_tickers_result['data'] = datas
        return api_tickers_result

    # 获取所有产品的行情字典
    def get_tickersMap(self, instIds=[]) -> dict:
        bookTickers_result = self.get_tickers(instIds=instIds)
        # [ERROR RETURN] 数据异常
        if bookTickers_result['code'] != '0':
            return bookTickers_result
        data_map = {}
        for ticker in bookTickers_result['data']:
            instId = ticker['instId']
            data_map[instId] = ticker

        bookTickers_result['data'] = data_map
        return bookTickers_result

    # 获取单个产品的行情
    def get_ticker(self, instId: str) -> dict:
        result = self.marketAPI.get_ticker(instId=instId)
        if result['code'] != '0':
            return result
        result['data'] = result['data'][0]
        return result

    # 产品深度
    def get_books(self, instId: str, sz: int = 1):
        result = self.marketAPI.get_books(instId=instId, sz=sz)
        if result['code'] != '0':
            return result
        result['data'] = result['data'][0]
        return result

    # 获取产品轻量深度
    def get_books_lite(self, instId: str):
        result = self.marketAPI.get_books_lite(instId=instId)
        if result['code'] != '0':
            return result
        result['data'] = result['data'][0]
        return result

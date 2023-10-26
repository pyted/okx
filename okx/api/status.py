'''
Status
https://www.okx.com/docs-v5/zh/#status
'''
from paux.param import to_local
from okx.api._client import Client


class _StatusEndpoints():
    get_status = ['/api/v5/system/status', 'GET']  # 获取系统升级事件的状态。


class Status(Client):
    # 获取系统升级事件的状态。
    def get_status(self, state: str = '', proxies={}, proxy_host: str = None):
        '''
        获取系统升级事件的状态。  由计划系统维护引起的短暂不可用（<5秒）和WebSocket闪断连接（用户可以立即重连）将不会公布。此类维护只会在市场波动性低的时期进行。
        https://www.okx.com/docs-v5/zh/#status-get-status

        限速：1次/5s

        请求参数：
        Parameter         	Type    	Required	Description
        state             	String  	No       	系统的状态，scheduled:等待中 ; ongoing:进行中 ; pre_open:预开放；completed:已完成 canceled: 已取消 当维护时间过长，会存在预开放时间，一般持续10分钟左右。 不填写此参数，默认返回 等待中、进行中和预开放 的数据

        返回参数请参考官方文档
        '''
        return self.send_request(*_StatusEndpoints.get_status, **to_local(locals()))

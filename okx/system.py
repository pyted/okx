from paux.param import to_local
from okx._client import Client


class _SystemEndpoints:
    get_status = ['/api/v5/system/status', 'GET']  # 获取系统升级事件的状态。


class System(Client):
    # 获取系统升级事件的状态。
    def get_status(self, state: str = ''):
        '''
        https://www.okx.com/docs-v5/zh/#rest-api-status
        请求参数：
        Parameter         	Type    	Required	Description
        state             	String  	No       	系统的状态，scheduled:等待中 ; ongoing:进行中 ; pre_open:预开放；completed:已完成 canceled: 已取消 当维护时间过长，会存在预开放时间，一般持续10分钟左右。 不填写此参数，默认返回 等待中、进行中和预开放 的数据
        '''
        return self.send_request(*_SystemEndpoints.get_status, **to_local(locals()))

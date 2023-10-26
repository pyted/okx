from okx.app.exception._base import AbstractEXP


# 请求方法错误
class RequestMethodError(AbstractEXP):
    pass


# 响应状态码错误
class ResponseStatusError(AbstractEXP):
    pass


# 响应Json数据中的code状态码异常
class CodeException(AbstractEXP):
    pass


# 请求异常
class RequestException(AbstractEXP):
    pass

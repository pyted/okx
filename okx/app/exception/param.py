from okx.app.exception._base import AbstractEXP


# 参数异常
class ParamException(AbstractEXP):
    pass


class ParamRoundPriceTypeException(AbstractEXP):
    def __init__(self, type, pmt='type must in ["CEIL","FLOOR"]'):
        self.error_msg = 'type = {type} \n{pmt}'.format(
            type=str(type),
            pmt=pmt,
        )


class ParamPositionSideException(AbstractEXP):
    def __init__(self, positionSide, pmt='positionSide must in ["LONG","SHORT"]'):
        self.error_msg = 'positionSide = {positionSide} \n{pmt}'.format(
            positionSide=str(positionSide),
            pmt=pmt,
        )

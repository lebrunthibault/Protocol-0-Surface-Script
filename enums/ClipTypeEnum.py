from a_protocol_0.enums.AbstractEnum import AbstractEnum


class ClipTypeEnum(AbstractEnum):
    NORMAL = ""
    ONE_SHOT = "one"

    @classmethod
    def default(cls):
        return ClipTypeEnum.NORMAL

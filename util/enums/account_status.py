from enum import Enum


class Status(Enum):
    ACTIVE = 0
    BLOCKED = 1
    CLOSED = 2

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

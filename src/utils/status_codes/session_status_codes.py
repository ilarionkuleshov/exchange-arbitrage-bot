from enum import IntEnum


class SessionStatusCodes(IntEnum):
    NOT_PROCESSED = 0
    IN_PROCESSING = 1
    SUCCESS = 2
    ERROR = 4

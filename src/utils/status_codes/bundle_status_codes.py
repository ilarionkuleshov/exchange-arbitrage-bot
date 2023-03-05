from enum import IntEnum


class BundleStatusCodes(IntEnum):
    NOT_PROCESSED = 0
    MESSAGE_SENT_SUCCESS = 2

    ERROR = 4
    BANNED = 44

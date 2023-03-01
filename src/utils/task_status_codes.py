from enum import IntEnum


class TaskStatusCodes(IntEnum):
    NOT_PROCESSED = 0
    IN_PROCESSING = 1

    SUCCESS = 2
    MESSAGE_SENT_SUCCESS = 22

    ERROR = 4
    BANNED = 44

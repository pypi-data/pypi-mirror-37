"""
definitions about status and events, shared by client and omnivore,
To make them using the same definitions, keep only one file is the
solution
"""

from enum import Enum

class CabinetMode(Enum):
    """
    all cabinet modes
    """
    DOING_TRANSACTION = 1
    COLLECTIING_IMAGE = 2
    # just for completeness
    FREE = 3


class TransactionStatus(Enum):
    """
    all transaction status
    """
    SCANNED = 1
    DOOR_OPENED = 2
    LOCK_OPENED = 8
    OPEN_DOOR_TIMEOUT = 3
    CACULATING = 4
    CACULATED = 5
    UNKNOWN_ERROR = 6
    # just for completeness
    FREE = 7


class EventTypes(Enum):
    # server -> cabinet events
    START_TRANSACTION = 999
    LOG_TRANSACTION = 1000
    TAKE_SNAPSHOT = 1001
    # used to enable or disable img_collect mode on cabinet
    ENTER_IMG_COLLECT = 201
    EXIT_IMG_COLLECT = 202

    # cabinet -> server events
    LOCK_OPENED = 2
    LOCK_OPEN_FAILED = 3
    OPEN_DOOR_TIMEOUT = 4
    DOOR_OPENED = 5
    PHOTOS_TAKEN_FAILED_START = 6
    PHOTOS_TAKEN_FAILED_END = 26
    PHOTOS_TAKEN_SUCCEED_START = 101
    PHOTOS_TAKEN_SUCCEED_END = 102
    DETECT_FAILED_START = 7
    DETECT_SUCCEED_START = 8
    DETECT_FAILED_END = 12
    DETECT_SUCCEED_END = 13
    DOOR_CLOSED = 9

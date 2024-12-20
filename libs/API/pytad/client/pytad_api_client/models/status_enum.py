from enum import Enum


class StatusEnum(str, Enum):
    ERROR = "ERROR"
    FAILED = "FAILED"
    INPROGRESS = "INPROGRESS"
    PASSED = "PASSED"
    SKIPPED = "SKIPPED"
    UNKNOWN = "UNKNOWN"
    XFAILED = "XFAILED"
    XPASSED = "XPASSED"

    def __str__(self) -> str:
        return str(self.value)

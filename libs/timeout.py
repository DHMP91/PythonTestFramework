from datetime import datetime
from exceptions import TimedOutException
class Timeout:
    def __init__(self, timeout: int, expire_exception=False):
        self.expired_exception = expire_exception
        self.start_datetime = int(datetime.now().timestamp())
        self.timeout = timeout

    @property
    def expired(self):
        now = int(datetime.now().timestamp())
        if (now - self.start_datetime) > self.timeout:
            if self.expired_exception:
                raise TimedOutException("Timeout has expired!")
            return True
        return False



from hamcrest.core.base_matcher import BaseMatcher

class __IsWithinRange(BaseMatcher):

    def __init__(self, min_value: int, max_value: int):
        self.min = min_value
        self.max = max_value

    def _matches(self, value: int):
        if self.min <= value <= self.max:
            return True
        return False

    def describe_to(self, description):
        description.append_text(f'Number is within the range {self.min} to {self.max}.')



def is_within_range(min_value: int, max_value: int):
    return __IsWithinRange(min_value, max_value)
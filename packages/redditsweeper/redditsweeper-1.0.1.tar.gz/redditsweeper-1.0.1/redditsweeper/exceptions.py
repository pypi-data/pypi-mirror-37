class SweeperError(Exception):
    def __init__(self, value=None):
        self.value = value or ""

    def __str__(self):
        return repr(self.value)

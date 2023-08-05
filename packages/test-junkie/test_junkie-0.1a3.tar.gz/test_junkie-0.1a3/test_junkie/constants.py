class TestCategory:

    SUCCESS = "success"
    FAIL = "fail"
    IGNORE = "ignore"
    ERROR = "error"
    SKIP = "skip"
    CANCEL = "cancel"
    ALL = [SUCCESS, FAIL, IGNORE, ERROR, SKIP, CANCEL]
    ALL_UN_SUCCESSFUL = [FAIL, IGNORE, ERROR]


class SuiteCategory:

    SUCCESS = "success"
    FAIL = "fail"
    SKIP = "skip"
    CANCEL = "cancel"
    ALL = [SUCCESS, FAIL, SKIP, CANCEL]
    ALL_UN_SUCCESSFUL = [FAIL]

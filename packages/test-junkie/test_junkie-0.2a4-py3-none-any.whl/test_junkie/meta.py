import threading

from test_junkie.debugger import LogJunkie
from test_junkie.decorators import synchronized


def meta(**kwargs):
    return kwargs


class Meta:

    def __init__(self):

        pass

    @staticmethod
    @synchronized(threading.Lock())
    def update(test, parameter=None, suite_parameter=None, **kwargs):
        from test_junkie.builder import SuiteBuilder
        suites = SuiteBuilder.get_execution_roster().values()
        for suite in suites:
            if suite.update_test_meta(test, parameter, suite_parameter, **kwargs) is True:
                LogJunkie.debug("Updated meta for test: {}".format(test))
                return
        raise Exception("Failed to update meta for test: {}. Test not found!")

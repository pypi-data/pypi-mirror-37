import threading


class ParallelProcessor:

    def __init__(self, **kwargs):

        multi_threaded_config = {"suites": kwargs.get("suite_multithreading", False),
                                 "tests": kwargs.get("test_multithreading", False)}

        multi_processing_config = {"suites": kwargs.get("suite_multiprocessing", False),
                                   "tests": kwargs.get("test_multiprocessing", False)}

        if True in multi_threaded_config.values():
            if True in multi_processing_config.values():
                raise Exception("Cannot use multi-threading and multi-processing at the same time!")
        elif True in multi_processing_config.values():
            if True in multi_threaded_config.values():
                raise Exception("Cannot use multi-processing and multi-threading at the same time!")

        self.__multi_processing_config = multi_processing_config
        self.__multi_threaded_config = multi_threaded_config
        self.__test_limit = None
        self.__suite_limit = None

    def suite_multithreading(self):

        return self.__multi_threaded_config.get("suites")

    def test_multithreading(self):

        return self.__multi_threaded_config.get("tests")

    def suite_multiprocessing(self):

        return self.__multi_processing_config.get("suites")

    def test_multiprocessing(self):

        return self.__multi_processing_config.get("tests")

    @staticmethod
    def run_suite_in_a_thread(func, suite):
        thread = threading.Thread(target=func, args=(suite,))
        thread.start()
        return thread

    @staticmethod
    def run_test_in_a_thread(func, suite, test, test_start_time, parameter, before_class_error):
        thread = threading.Thread(target=func, args=(suite, test, test_start_time, parameter, before_class_error))
        thread.start()
        return thread

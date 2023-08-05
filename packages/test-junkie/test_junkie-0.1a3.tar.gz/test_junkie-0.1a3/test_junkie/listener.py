import time
import traceback


class TestListener:

    def __init__(self, **kwargs):

        self.kwargs = kwargs

    def on_in_progress(self):

        print("===========Test In Progress===========")
        print("Args: ", self.kwargs)
        print("=================================")

    def on_cancel(self):

        print("===========Test Canceled===========")
        print("Args: ", self.kwargs)
        print("=================================")

    def on_success(self):

        print("===========Test passed===========")
        print("Args: ", self.kwargs)
        print("=================================")

    def on_failure(self, exception):
        print("===========Test failed===========")
        print("Args: ", self.kwargs)
        time.sleep(0.005)
        traceback.print_tb(exception.__traceback__)
        time.sleep(0.005)
        print("=================================")

    def on_skip(self):
        print("===========Test skipped==========")
        print("Args: ", self.kwargs)
        print("=================================")

    def on_error(self, exception):
        print("===========Test error===========")
        print("Args: ", self.kwargs)
        time.sleep(0.005)
        traceback.print_tb(exception.__traceback__)
        time.sleep(0.005)
        # print(exception.with_traceback(exception.__traceback__))
        print("=================================")

    def on_ignore(self, exception):
        print("===========Test ignored==========")
        print("Args: ", self.kwargs)
        time.sleep(0.005)
        traceback.print_tb(exception.__traceback__)
        time.sleep(0.005)
        print("=================================")

    def on_before_class_error(self, exception):
        print("===========Before Class Error===========")
        print("Args: ", self.kwargs)
        time.sleep(0.005)
        traceback.print_tb(exception.__traceback__)
        time.sleep(0.005)
        print("========================================")

    def on_before_class_failure(self, exception):
        print("===========Before Class Failed===========")
        print("Args: ", self.kwargs)
        time.sleep(0.005)
        traceback.print_tb(exception.__traceback__)
        time.sleep(0.005)
        print("=========================================")

    def on_after_class_error(self, exception):
        print("===========After Class Error===========")
        print("Args: ", self.kwargs)
        time.sleep(0.005)
        traceback.print_tb(exception.__traceback__)
        time.sleep(0.005)
        print("=======================================")

    def on_after_class_failure(self, exception):
        print("===========After Class Failed===========")
        print("Args: ", self.kwargs)
        time.sleep(0.005)
        traceback.print_tb(exception.__traceback__)
        time.sleep(0.005)
        print("========================================")

    def on_class_in_progress(self):
        print("===========Class In Progress===========")
        print("Args: ", self.kwargs)
        print("===================================")

    def on_class_skip(self):
        print("===========Class Skipped===========")
        print("Args: ", self.kwargs)
        print("===================================")

    def on_class_cancel(self):
        print("===========Class Canceled===========")
        print("Args: ", self.kwargs)
        print("===================================")

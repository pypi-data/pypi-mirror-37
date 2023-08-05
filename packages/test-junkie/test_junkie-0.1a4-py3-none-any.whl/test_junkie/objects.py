from test_junkie.decorators import DecoratorType
from test_junkie.constants import TestCategory
from test_junkie.metrics import ClassMetrics, TestMetrics


class SuiteObject:

    def __init__(self, suite_definition):

        self.__suite_definition = suite_definition
        self.__listener = suite_definition["test_listener"](class_meta=suite_definition["class_meta"])
        self.__rules = suite_definition["test_rules"](class_meta=suite_definition["test_rules"])
        self.__tests = []
        self.__absolute_test_count = 0
        self.__test_count = 0
        self.__has_parameterized_tests = False

        for test in suite_definition["suite_definition"].get(DecoratorType.TEST_CASE):
            params = test["decorator_kwargs"].get("parameters", [])
            self.__tests.append(TestObject(test))
            self.__absolute_test_count += len(params) if params else 1
            self.__test_count += 1
            self.__has_parameterized_tests = True if params else False

        self.metrics = ClassMetrics()

    def get_decorated_definition(self, decorator_type):

        return self.__suite_definition["suite_definition"].get(decorator_type)

    def get_test_count(self):

        return self.__test_count

    def get_absolute_test_count(self):

        return self.__absolute_test_count

    def has_parameterised_tests(self):

        return self.__has_parameterized_tests

    def get_class_name(self):

        return self.__suite_definition["class_name"]

    def get_class_object(self):

        return self.__suite_definition["class_object"]

    def get_class_module(self):

        return self.get_class_object().__module__

    def get_test_objects(self):

        return self.__tests

    def can_skip(self):

        return self.__suite_definition.get("class_skip", False)

    def get_retry_limit(self):

        return self.__suite_definition.get("class_retry", 1)

    def get_rules(self):

        return self.__rules

    def get_listener(self):

        return self.__listener

    def get_meta(self):

        return self.__suite_definition["class_meta"]

    def get_unsuccessful_tests(self):

        unsuccessful_tests = []
        tests = self.get_test_objects()
        for test in tests:
            for value in test.metrics.get_metrics().values():
                if value["status"] in TestCategory.ALL_UN_SUCCESSFUL:
                    unsuccessful_tests.append(test)
        return unsuccessful_tests

    def has_unsuccessful_tests(self):

        tests = self.get_test_objects()
        for test in tests:
            for value in test.metrics.get_metrics().values():
                if value["status"] in TestCategory.ALL_UN_SUCCESSFUL:
                    return True
        return False

    def get_status(self):

        return self.metrics.get_metrics()["status"]

    def get_parallel_restrictions(self):

        return self.__suite_definition["pr"]


class TestObject:

    def __init__(self, test_definition):

        self.__test_definition = test_definition

        self.metrics = TestMetrics()

    def can_skip(self):

        return self.get_kwargs().get("skip", False)

    def get_parameters(self):

        return self.get_kwargs().get("parameters", [None])

    def get_retry_limit(self):

        return self.get_kwargs().get("retry", 1)

    def get_function_name(self):

        return self.get_function_object().__name__

    def get_function_object(self):

        return self.__test_definition["decorated_function"]

    def get_tags(self):

        return self.get_kwargs().get("tags", [])

    def get_meta(self):

        return self.get_kwargs().get("meta", {})

    def get_kwargs(self):

        return self.__test_definition["decorator_kwargs"]

    def _is_qualified_for_retry(self, param=None):

        test = self.metrics.get_metrics()[str(param)]
        return test["status"] in TestCategory.ALL_UN_SUCCESSFUL

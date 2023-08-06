import numpy as np


class TestRunData:

    def __init__(self):
        self.test_passed = 0
        self.test_failed = 0
        self.test_not_run = 0
        self.total_steps = 0
        self.passed_steps = 0
        self.failed_steps = 0
        self.data_test = []

    def get_test_passed(self):
        return self.test_passed

    def get_test_failed(self):
        return self.test_failed

    def get_test_not_run(self):
        return self.test_not_run

    def get_number_of_test_case(self):
        return len(self.data_test)

    def add_test_case(self, name, order):
        test_case = TestCaseData(name, order)
        self.data_test.append(test_case)
        return test_case

    def get_test_case_by_order(self, order):
        """
        test: (TestCaseData)
        """
        for test in self.data_test:
            if test.get_order() == order:
                return test

    def get_test_data(self):
        return self.data_test

    def get_passed_test_case(self):
        self.test_passed = 0
        for test in self.data_test:
            if test.get_status() == "pass":
                self.test_passed += 1
        return self.test_passed

    def get_failed_test_case(self):
        self.test_failed = 0
        for test in self.data_test:
            if test.get_status() == "fail":
                self.test_failed += 1
        return self.test_failed

    def get_total_steps(self):
        self.total_steps = 0
        for test in self.data_test:
            self.total_steps += test.get_number_of_steps()
        return self.total_steps

    def get_total_passed_steps(self):
        self.passed_steps = 0
        for test in self.data_test:
            self.passed_steps += test.get_passed_steps()
        return self.passed_steps

    def get_total_failed_steps(self):
        self.failed_steps = 0
        for test in self.data_test:
            self.failed_steps += test.get_failed_steps()
        return self.failed_steps


class TestCaseData:

    def __init__(self, name, order):
        self._name = name
        self._order = order
        self._passed_steps = 0
        self._failed_steps = 0
        self._total_steps = 0
        self._status = None
        self._steps = []

    def get_steps(self):
        return self._steps

    def get_number_of_steps(self):
        return len(self._steps)

    def get_name(self):
        return self._name

    def get_order(self):
        return self._order

    def get_total_steps(self):
        return self._total_steps

    def get_passed_steps(self):
        return self._passed_steps

    def get_failed_steps(self):
        return self._failed_steps

    def get_status(self):
        return self._status

    def get_passed_percentage(self, decimals):
        return np.round((self._passed_steps / self._total_steps) * 100, decimals)

    def set_status(self, status):
        self._status = status

    def check_status(self):
        if self._failed_steps >= 1:
            self.set_status("fail")
        else:
            self.set_status("pass")

    def add_step(self, order,
                 description=None,
                 status=None,
                 time=None,
                 method=None,
                 error_message=None,
                 error_line=None,
                 error_line_module=None):

        step = StepData(order,
                        description=description,
                        status=status,
                        time=time,
                        func=method,
                        error_message=error_message,
                        error_line=error_line,
                        error_line_module=error_line_module)

        self._total_steps += 1

        if status == "pass":
            self._passed_steps += 1
        if status == "fail":
            self._failed_steps += 1

        self.check_status()

        self._steps.append(step)

    def get_step_by_order(self, order):
        for step in self._steps:
            if step.get_order() == order:
                return step


class StepData:

    def __init__(self,
                 order,
                 description=None,
                 status=None,
                 time=None,
                 func=None,
                 error_message=None,
                 error_line=None,
                 error_line_module=None):
        self._order = order

        if description is None:
            self._description = "There is no description"
        else:
            self._description = description
        self._status = status
        self._time = time
        self._func = func
        if error_message is None:
            self._error_message = "There is no error message"
        else:
            self._error_message = error_message
        self._error_line = error_line
        self._error_line_module = error_line_module

    def get_order(self):
        return self._order

    def get_description(self):
        return self._description

    def get_status(self):
        return self._status

    def get_time(self):
        return self._time

    def get_method(self):
        return self._func

    def get_error_message(self):
        return self._error_message

    def get_error_line(self):
        return self._error_line

    def get_error_line_module(self):
        return self._error_line_module

    def set_order(self, order):
        self._order = order

    def set_description(self, description):
        self._description = description

    def set_status(self, status):
        self._status = status

    def set_time(self, time):
        self._time = time

    def set_method(self, method):
        self._func = method

    def set_error_message(self, error_message):
        self._error_message = error_message

    def set_error_line(self, error_line):
        self._error_line = error_line

    def set_error_line_module(self, error_line_module):
        self._error_line_module = error_line_module

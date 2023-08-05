import pytest

from coverage_wrapper import CoverageWrapper
from coverage.data import CoverageData
from logger import Logger


class PytestPlugin(object):
    """Use coverage package to produce code coverage reports.
    """

    def __init__(self, options, pluginmanager):
        """Creates a coverage plugin."""

        self.current_test_name = None
        self.current_result = True
        self.logger = Logger()
        self.coverage = CoverageWrapper(
            options.coverage_config,
            options.coverage_outdir,
            self.logger
        )

    def pytest_runtest_setup(self, item):
        self.current_test_name = item.name
        self.current_result = True
        self.coverage.start(self.current_test_name)

    def pytest_runtest_teardown(self, item):
        self.coverage.finish()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):        
        outcome = yield
        report = outcome.get_result()

        is_step_success = report.outcome == "passed"
        self.current_result = self.current_result and is_step_success

        if call.when != "teardown":
            return

        self.logger.debug(self.current_result)
        self.coverage.mark_test_result(self.current_result)

    def pytest_terminal_summary(self, terminalreporter):
        self.logger.terminal_summary(terminalreporter)
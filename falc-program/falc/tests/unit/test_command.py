from unittest import TestCase

from fall.result_constants import INPUT_VALIDATION_FAILURE, INSTALL_SUCCESS, QUERY_SUCCESS, \
    UNABLE_TO_GET_PLATFORM_INFO_FAILURE

from falc.command import FwCommand, QueryCommand
from falc.falc_exception import FalcException


class TestCommand(TestCase):
    def setUp(self):
        self._fw_cmd = FwCommand()
        self._query_cmd = QueryCommand()

    def test_search_response_fw_input_validation_failure(self):
        self.assertEqual(1, self._fw_cmd.search_response(INPUT_VALIDATION_FAILURE))

    def test_search_response_query_raises(self):
        with self.assertRaises(FalcException):
            self._query_cmd.search_response(INPUT_VALIDATION_FAILURE)

    def test_return_0_success_string_fw_cmd(self):
        self.assertEqual(0, self._fw_cmd.search_response(INSTALL_SUCCESS))

    def test_return_0_success_string_query_cmd(self):
        self.assertEqual(0, self._query_cmd.search_response(QUERY_SUCCESS))

    def test_return_1_fail_string_query_cmd(self):
        self.assertEqual(1, self._query_cmd.search_response(UNABLE_TO_GET_PLATFORM_INFO_FAILURE))

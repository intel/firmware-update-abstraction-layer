from unittest import TestCase

from falc.utility import get_canonical_representation_of_path, search_keyword
from fall.result_constants import INSTALL_SUCCESS, INPUT_VALIDATION_FAILURE, INSTALL_FAILURE


class TestUtility(TestCase):

    def test_get_canonical_representation_of_absolute_path(self):
        self.assertEqual('/var/cache/manageability',
                         get_canonical_representation_of_path("/var/cache/manageability"))

    def test_search_keyword_true(self):
        output = search_keyword(
            INSTALL_FAILURE, [INSTALL_SUCCESS, INPUT_VALIDATION_FAILURE, INSTALL_FAILURE])
        self.assertTrue(output)

    def test_search_keyword_false(self):
        self.assertFalse(search_keyword(INSTALL_SUCCESS, [
                         INPUT_VALIDATION_FAILURE, INSTALL_FAILURE]))

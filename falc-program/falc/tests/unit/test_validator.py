import argparse

from unittest import TestCase
from falc.validator import validate_string_less_than_n_characters, validate_date, validate_guid


class TestValidater(TestCase):

    def test_return_value_when_less_than_max_limit(self):
        try:
            self.assertEqual('Howdy!', validate_string_less_than_n_characters('Howdy!', 'Vendor', 6))
        except argparse.ArgumentTypeError as e:
            self.fail(f"Unexpected exception raised during test: {e}")

    def test_raise_when_value_greater_than_max_limit(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError, "Vendor is greater than allowed string size: Howdy!"):
            validate_string_less_than_n_characters('Howdy!', 'Vendor', 5)

    def test_return_date_when_correct_format(self):
        try:
            self.assertEqual('2022-01-01', validate_date('2022-01-01'))
        except argparse.ArgumentTypeError as e:
            self.fail(f"Unexpected exception raised during test: {e}")

    def test_raise_when_invalid_date_format(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError, "Not a valid date - format YYYY-MM-DD: 01-01-2022"):
            validate_date('01-01-2022')

    def test_check_validate_guid_pass(self):
        self.assertEqual('6c8e136f-d3e6-4131-ac32-4687cb4abd27', validate_guid('6c8e136f-d3e6-4131-ac32-4687cb4abd27'))

    def test_fail_guid_check_with_hex_letter(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "GUID should be 36 characters displayed in five groups in the format XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX. Hexdigits are not allowed."):
            validate_guid('123e4567-h89b-12d3-a456-9AC7CBDCEE52')

    def test_fail_guid_check_too_few_characters(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "GUID should be 36 characters displayed in five groups in the format XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX. Hexdigits are not allowed."):
            validate_guid('123e4567-h89b-12d3-a456')

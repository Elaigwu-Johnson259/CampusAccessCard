import unittest

from campus_access.validation import (
    validate_fellow_id,
    validate_card_type,
    validate_request_id,
    validate_approver,
    validate_request_record,

)


class TestValidation(unittest.TestCase):

    def test_valid_fellow_id(self):
        self.assertEqual(validate_fellow_id("F001"), "F001")

    def test_blank_fellow_id_rejected(self):
        with self.assertRaises(ValueError):
            validate_fellow_id("  ")

    def test_invalid_fellow_id_rejected(self):
        with self.assertRaises(ValueError):
            validate_fellow_id("rubbish")

    def test_malformed_fellow_id_rejected(self):
        with self.assertRaises(ValueError):
            validate_fellow_id("F12")

    def test_invalid_card_type_(self):
        self.assertEqual(validate_card_type("visitor"), "visitor")

    def test_valid_card_type_rejected(self):
        with self.assertRaises(ValueError):
            validate_card_type("guest")

    def test_valid_request_id(self):
        self.assertEqual(validate_request_id("A001"), "A001")

    def test_valid_approver(self):
        with self.asserRaises(ValueError):
            validate_request_id("A12")

    def test_valid_approver(self):
        self.assertEqual(validate_approver("M01"), "M01")

    def test_blank_approver_rejected(self):
        with self.assertRaises(ValueError):
            validate_approver("")

    def test_valid_request_record(self):
        record = {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "visitor",
            "status": "requested",
            "approved_by": None,
        }

        self.assertEqual(validate_request_record(record), record)

    def test_invalid_request_record_rejected(self):
        record = {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "visitor",
            "status": "unknown",
            "approved_by": None,
        }

        with self.assertRaises(ValueError):
            validate_request_record(record)


if __name__ == "__main__":
    unittest.main()

    
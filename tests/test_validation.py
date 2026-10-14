import unittest

from campus_access.validation import (
    validate_fellow_id,
    validate_card_type,
    validate_request_id,
    validate_request_record,
)


class TestValidation(unittest.TestCase):

    def test_valid_fellow_id(self):
        validate_fellow_id("F001")

    def test_blank_fellow_id_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_fellow_id(" ")

    def test_valid_card_type(self):
        for card_type in ("visitor", "student", "staff"):
            with self.subTest(card_type=card_type):
                validate_card_type(card_type)

    def test_invalid_card_type_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_card_type("guest")

    def test_valid_request_id(self):
        validate_request_id("A001")

    def test_invalid_request_id_is_rejected(self):
        for request_id in ("A", "A01", "B001", "A00x"):
            with self.subTest(request_id=request_id):
                with self.assertRaises(ValueError):
                    validate_request_id(request_id)

    def test_valid_request_record(self):
        request = {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "student",
            "status": "requested",
            "approved_by": None,
        }
        validate_request_record(request)


if __name__ == "__main__":
    unittest.main()

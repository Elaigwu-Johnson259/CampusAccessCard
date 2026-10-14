import json
import tempfile
import unittest
from pathlib import Path

from campus_access import storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "requests.json"
        storage._requests.clear()

    def tearDown(self):
        storage._requests.clear()
        self.temp_dir.cleanup()

    def test_create_request(self):
        request = storage.create_request("F001", "student")

        self.assertEqual(request["id"], "A001")
        self.assertEqual(request["status"], "requested")

    def test_get_existing_request(self):
        created = storage.create_request("F001", "student")

        found = storage.get_request(created["id"])

        self.assertEqual(found["fellow_id"], "F001")

    def test_get_missing_request(self):
        self.assertIsNone(storage.get_request("A001"))

    def test_list_requests(self):
        storage.create_request("F001", "student")
        storage.create_request("F002", "staff")

        self.assertEqual(len(storage.list_requests()), 2)

    def test_update_request(self):
        request = storage.create_request("F001", "student")

        updated = storage.update_request(
            request["id"],
            status="approved",
            approved_by="M001",
        )

        self.assertEqual(updated["status"], "approved")
        self.assertEqual(updated["approved_by"], "M001")

    def test_save_and_load_requests(self):
        storage.create_request("F001", "student")
        storage.save_requests(self.file_path)

        storage._requests.clear()
        loaded = storage.load_requests(self.file_path)

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["id"], "A001")

    def test_invalid_json_is_rejected(self):
        self.file_path.write_text("{invalid json", encoding="utf-8")

        with self.assertRaises(ValueError):
            storage.load_requests(self.file_path)

    def test_duplicate_ids_in_saved_file_are_rejected(self):
        request = {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "student",
            "status": "requested",
            "approved_by": None,
        }
        self.file_path.write_text(
            json.dumps([request, request]),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            storage.load_requests(self.file_path)


if __name__ == "__main__":
    unittest.main()


import json
import tempfile
import unittest
from pathlib import Path

from campus_access import storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        storage._requests = []
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "requests.json"

    def tearDown(self):
        self.temp_dir.cleanup()


    def test_create_request(self):
        request = storage.create_request("F001", "visitor")

        self.assertEqual(request["id"], "A001")
        self.assertEqual(request["fellow_id"], "F001")
        self.assertEqual(request["card_type"], "visitor")
        self.assertEqual(request["status"], "requested")
        self.assertIsNone(request["approved_by"])


    def test_get_request(self):
        storage.create_request("F001", "visitor")

        request = storage.get_request("A001")

        self.assertIsNotNone(request)
        self.assertEqual(request["fellow_id"], "F001")
        self.assertIsNone(storage.get_request("A002"))


    def test_list_requests(self):
        storage.create_request("F001", "visitor")
        storage.create_request("F002", "student")

        requests = storage.list_requests()

        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0]["id"], "A001")
        self.assertEqual(requests[1]["id"], "A002")


    def test_update_request(self):
        storage.create_request("F001", "visitor")

        updated = storage.update_request(
            "A001",
            status="approved",
            approved_by="M01",
        )

        self.assertEqual(updated["status"], "approved")
        self.assertEqual(updated["approved_by"], "M01")
        self.assertEqual(storage.get_request("A001")["status"], "approved")


    def test_save_requests(self):
        storage.create_request("F001", "visitor")

        storage.save_requests(self.file_path)

        self.assertTrue(self.file_path.exists())

        with self.file_path.open("r", encoding="utf-8") as file:
            saved = json.load(file)

        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["id"], "A001")


    def test_load_requests(self):
        storage.create_request("F001", "visitor")
        storage.save_requests(self.file_path)

        storage._requests = []
        loaded = storage.load_requests(self.file_path)

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["id"], "A001")

        next_request = storage.create_request("F002", "student")
        self.assertEqual(next_request["id"], "A002")


    def test_invalid_saved_data_rejected(self):
        self.file_path.write_text(
            '{"not": "a list"}',
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            storage.load_requests(self.file_path)

    def test_duplicate_fellow_id_rejected(self):
        storage.create_request("F001", "student")

        with self.assertRaises(ValueError):
            storage.create_request("F001", "staff")


if __name__ == "__main__":
    unittest.main()

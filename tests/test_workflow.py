import tempfile
import unittest
from pathlib import Path

from campus_access import storage
from campus_access.workflow import (
    approve_request,
    issue_card,
    return_card,
)


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "requests.json"
        storage._requests.clear()
        self.original_save_requests = storage.save_requests
        storage.save_requests = lambda path=storage.DATA_FILE: (
            self.original_save_requests(self.file_path)
        )

    def tearDown(self):
        storage.save_requests = self.original_save_requests
        storage._requests.clear()
        self.temp_dir.cleanup()

    def create_request(self):
        return storage.create_request("F001", "student")

    def test_approve_request(self):
        request = self.create_request()

        result = approve_request(request["id"], "M001")

        self.assertEqual(result["status"], "approved")
        self.assertEqual(result["approved_by"], "M001")

    def test_blank_approver_is_rejected(self):
        request = self.create_request()

        with self.assertRaises(ValueError):
            approve_request(request["id"], " ")

    
    def test_cannot_issue_without_approver(self):
        request = self.create_request()
        approve_request(request["id"], "M001")

        original_get_request = storage.get_request
        storage.get_request = lambda request_id: {
            "id": request["id"],
            "fellow_id": request["fellow_id"],
            "card_type": request["card_type"],
            "status": "approved",
            "approved_by": None,
        }

        try:
            with self.assertRaises(ValueError):
                issue_card(request["id"])
        finally:
            storage.get_request = original_get_request


        with self.assertRaises(ValueError):
            issue_card(request["id"])

    
    def test_cannot_issue_without_approver(self):
        request = self.create_request()

        original_get_request = storage.get_request
        storage.get_request = lambda request_id: {
            "id": request["id"],
            "fellow_id": request["fellow_id"],
            "card_type": request["card_type"],
            "status": "approved",
            "approved_by": None,
        }

        try:
            with self.assertRaises(ValueError):
                issue_card(request["id"])
        finally:
            storage.get_request = original_get_request


    def test_cannot_return_unissued_request(self):
        request = self.create_request()

        with self.assertRaises(ValueError):
            return_card(request["id"])

    def test_complete_workflow(self):
        request = self.create_request()

        approve_request(request["id"], "M001")
        issue_card(request["id"])
        result = return_card(request["id"])

        self.assertEqual(result["status"], "returned")

    def test_cannot_return_card_twice(self):
        request = self.create_request()

        approve_request(request["id"], "M001")
        issue_card(request["id"])
        return_card(request["id"])

        with self.assertRaises(ValueError):
            return_card(request["id"])


if __name__ == "__main__":
    unittest.main()

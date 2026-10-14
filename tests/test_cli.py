import unittest
from unittest.mock import patch

from campus_access.cli import run_menu


class TestCLI(unittest.TestCase):

    @patch("builtins.input", side_effect=["8"])
    def test_menu_quits(self, mock_input):
        run_menu()
        mock_input.assert_called_once()

    @patch("builtins.input", side_effect=["invalid", "8"])
    def test_invalid_option_then_quit(self, mock_input):
        run_menu()
        self.assertEqual(mock_input.call_count, 2)


if __name__ == "__main__":
    unittest.main()

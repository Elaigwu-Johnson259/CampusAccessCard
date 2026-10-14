
"""Start the campus access-card application."""

from campus_access.storage import load_requests
from campus_access.cli import run_menu


if __name__ == "__main__":
    try:
        load_requests()
        run_menu()
    except ValueError as error:
        print(f"Error loading saved requests: {error}")
        print("The application could not start safely.")

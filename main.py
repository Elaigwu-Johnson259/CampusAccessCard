"""Start CampusAccessCard with automatic environment setup."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"

if sys.platform == "win32":
    VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
else:
    VENV_PYTHON = VENV_DIR / "bin" / "python"

REQUIREMENTS = PROJECT_ROOT / "requirements.txt"
DEPENDENCY_MARKER = VENV_DIR / ".dependencies-installed"


def prepare_environment():
    """Create the project environment and install dependencies if needed."""

    if not VENV_PYTHON.exists():
        print("First-time setup: creating Python environment...")

        subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            check=True,
        )

    if (
        not DEPENDENCY_MARKER.exists()
        or REQUIREMENTS.stat().st_mtime > DEPENDENCY_MARKER.stat().st_mtime
    ):
        print("Installing required packages. This may take a few minutes...")

        subprocess.run(
            [
                str(VENV_PYTHON),
                "-m",
                "pip",
                "install",
                "-r",
                str(REQUIREMENTS),
            ],
            check=True,
        )

        DEPENDENCY_MARKER.touch()

    env_file = PROJECT_ROOT / ".env"
    example_file = PROJECT_ROOT / ".env.example"

    if not env_file.exists() and example_file.exists():
        shutil.copy2(example_file, env_file)


if __name__ == "__main__":
    try:
        prepare_environment()

        current_python = os.path.abspath(sys.executable)
        project_python = os.path.abspath(str(VENV_PYTHON))

        if current_python != project_python:
            os.execv(
                str(VENV_PYTHON),
                [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]],
            )

    except (OSError, subprocess.CalledProcessError) as error:
        print("\n[SETUP ERROR] Could not prepare CampusAccessCard.")
        print(f"Reason: {error}")
        print("Check your internet connection and Python installation.")
        sys.exit(1)

    from campus_access.storage import load_requests
    from campus_access.cli import run_menu

    try:
        load_requests()
        run_menu()
    except ValueError as error:
        print(f"Error loading saved requests: {error}")
        print("The application could not start safely.")

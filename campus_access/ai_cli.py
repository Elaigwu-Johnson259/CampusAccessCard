"""Interactive CLI for the CampusAccessCard AI assistant."""

import os
from getpass import getpass
from pathlib import Path

from dotenv import load_dotenv, set_key


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
DEFAULT_MODEL = "gemini-3.6-flash"


def configure_gemini():
    """Load or securely request the user's Gemini configuration."""

    load_dotenv(dotenv_path=ENV_FILE)

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", "").strip() or DEFAULT_MODEL

    if not api_key:
        print("\nGemini AI setup")
        print("Get your API key from https://aistudio.google.com/apikey")
        api_key = getpass("Enter your Gemini API key: ").strip()

        if not api_key:
            print("No API key provided. Returning to the main menu.")
            return False

        set_key(str(ENV_FILE), "GEMINI_API_KEY", api_key)
        os.environ["GEMINI_API_KEY"] = api_key

    if not os.getenv("GEMINI_MODEL", "").strip():
        set_key(str(ENV_FILE), "GEMINI_MODEL", model)
        os.environ["GEMINI_MODEL"] = model

    return True


def run_ai_assistant():
    """Start an interactive session with the Gemini assistant."""

    try:
        if not configure_gemini():
            return

        from .ai_assistant import ask_campus_access_ai

    except Exception as exc:
        print("\n[AI UNAVAILABLE] Check your Gemini configuration or connection.")
        print(f"Error type: {type(exc).__name__}")
        return

    print("\n========== AI ASSISTANT ==========")
    print("Ask questions about access-card requests.")
    print("Examples:")
    print("- What is the status of A001?")
    print("- Show all pending requests.")
    print("- How many cards have been issued?")
    print("Type 'back' to return to the main menu.")
    print("==================================")

    while True:
        try:
            question = input("\nYou: ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\nReturning to the main menu.")
            break

        if question.lower() in {"back", "exit", "quit"}:
            print("Returning to the main menu.")
            break

        if not question:
            print("Please enter a question.")
            continue

        answer = ask_campus_access_ai(question)
        print(f"\nCampusAccess AI: {answer}")

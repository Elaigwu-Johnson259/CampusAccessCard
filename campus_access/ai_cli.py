"""Interactive CLI for the CampusAccessCard AI assistant."""


def run_ai_assistant():
    """Start an interactive session with the Gemini assistant."""

    # Import only when the user opens the AI assistant.
    # This keeps the normal application usable if Gemini is unavailable.
    try:
        from .ai_assistant import ask_campus_access_ai

    except Exception as exc:
        print(
            "\n[AI UNAVAILABLE] "
            "Check your Gemini configuration and dependencies."
        )
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

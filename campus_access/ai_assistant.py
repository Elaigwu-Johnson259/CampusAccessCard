"""Gemini-powered AI assistant for CampusAccessCard."""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .ai_tools import (
    lookup_request,
    list_requests_by_status,
    get_request_statistics,
)


# Explicitly load the root .env file.
# This prevents accidentally loading campus_access/.env.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing from the project-root .env file."
    )

if not MODEL:
    raise RuntimeError(
        "GEMINI_MODEL is missing from the project-root .env file."
    )


client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=60000,
        retry_options=types.HttpRetryOptions(
            attempts=3,
            initial_delay=1,
            max_delay=10,
            exp_base=2,
            jitter=1,
        ),
    ),
)


SYSTEM_INSTRUCTION = """
You are the CampusAccessCard AI assistant.

Help users understand access-card requests and application statistics.

You have access to read-only tools for:
- Looking up a request by ID.
- Listing requests, optionally filtered by status.
- Calculating request statistics.

Rules:
1. Use the tools to retrieve actual application data.
2. Never invent request IDs, statuses, or statistics.
3. If a request is not found, clearly say so.
4. Valid statuses are requested, approved, issued, and returned.
5. Explain results in simple, helpful language.
6. Never claim that you approved, issued, returned, or modified a card.
7. Never attempt to perform write operations.
8. Return only information needed to answer the user's question.
"""

chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[
            lookup_request,
            list_requests_by_status,
            get_request_statistics,
        ],
        automatic_function_calling=(
            types.AutomaticFunctionCallingConfig(
                maximum_remote_calls=4
            )
        ),
    ),
)

def ask_campus_access_ai(question: str) -> str:
    """Answer a user's question using Gemini and approved read-only tools."""

    question = question.strip()

    if not question:
        return "Please enter a question."

    if len(question) > 4000:
        return "Please shorten your question to 4,000 characters or fewer."

    try:
        response = chat.send_message(question)

        if response.text:
            return response.text

        return (
            "I couldn't generate a text response. "
            "Please try asking your question again."
        )

    except Exception as exc:
        # Do not expose the API key, request contents, or traceback.
        print(
            "Gemini assistant error:",
            type(exc).__name__,
        )
        print("Details:", str(exc)[:300])  # temporary, for debugging

        return (
            "The AI assistant is temporarily unavailable. "
            "Please try again or use the normal application menu."
        )
 
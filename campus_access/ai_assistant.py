"""OpenRouter-powered AI assistant for CampusAccessCard."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from .ai_tools import (
    lookup_request,
    list_requests_by_status,
    get_request_statistics,
)


# Explicitly load the root .env file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")

if not API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is missing from the project-root .env file."
    )

if not MODEL:
    raise RuntimeError(
        "OPENROUTER_MODEL is missing from the project-root .env file."
    )


client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
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


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_request",
            "description": (
                "Find an access-card request by its ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": (
                            "The access-card request ID, such as A001."
                        ),
                    }
                },
                "required": ["request_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_requests_by_status",
            "description": (
                "List access-card requests, optionally filtered by status."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": (
                            "Optional status: requested, approved, "
                            "issued, or returned. Leave empty for all."
                        ),
                    }
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_request_statistics",
            "description": (
                "Calculate total requests and counts for each status."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
]


LOCAL_TOOLS = {
    "lookup_request": lookup_request,
    "list_requests_by_status": list_requests_by_status,
    "get_request_statistics": get_request_statistics,
}


def _execute_tool(name: str, arguments: str) -> dict:
    """Execute one approved read-only CampusAccessCard tool."""

    tool = LOCAL_TOOLS.get(name)

    if tool is None:
        return {
            "error": f"Unknown tool: {name}",
        }

    try:
        parsed_arguments = json.loads(arguments) if arguments else {}

        if not isinstance(parsed_arguments, dict):
            return {
                "error": "Tool arguments must be a JSON object.",
            }

        result = tool(**parsed_arguments)

        if isinstance(result, dict):
            return result

        return {
            "result": result,
        }

    except Exception as exc:
        return {
            "error": f"Tool execution failed: {type(exc).__name__}",
        }


def ask_campus_access_ai(question: str) -> str:
    """Answer a user's question using OpenRouter and local read-only tools."""

    question = question.strip()

    if not question:
        return "Please enter a question."

    if len(question) > 4000:
        return "Please shorten your question to 4,000 characters or fewer."

    messages = [
        {
            "role": "system",
            "content": SYSTEM_INSTRUCTION,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    try:
        # Allow several tool calls in one conversation turn.
        for _ in range(4):
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
            )

            message = response.choices[0].message

            tool_calls = message.tool_calls or []

            if not tool_calls:
                return message.content or (
                    "I couldn't generate a text response. "
                    "Please try asking your question again."
                )

            messages.append(message.model_dump(exclude_none=True))

            for tool_call in tool_calls:
                tool_result = _execute_tool(
                    tool_call.function.name,
                    tool_call.function.arguments,
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result),
                    }
                )

        return (
            "I couldn't complete that request because too many "
            "tool calls were required."
        )

    except Exception as exc:
        # Do not expose the API key, request contents, or traceback.
        print(
            "OpenRouter assistant error:",
            type(exc).__name__,
            str(exc)[:300],
        )

        return (
            "The AI assistant is temporarily unavailable. "
            "Please try again or use the normal application menu."
        )
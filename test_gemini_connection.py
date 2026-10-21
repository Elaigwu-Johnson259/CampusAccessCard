import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load the .env file from the project root.
PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

if not api_key:
    raise SystemExit("GEMINI_API_KEY is missing from the root .env file.")

if not model:
    raise SystemExit("GEMINI_MODEL is missing from the root .env file.")

print("Gemini connection test starting...")
print(f"Configured model: {model}")
print("Request timeout: 20 seconds")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=20000),
)

try:
    print("Sending test request to Gemini...")

    response = client.models.generate_content(
        model=model,
        contents="Reply with exactly: CampusAccessCard Gemini connection successful.",
    )

    print("\nGemini response:")
    print(response.text or "Gemini returned no text.")

except Exception as exc:
    print(f"\nGemini request failed: {type(exc).__name__}: {exc}")

finally:
    client.close()
    print("\nConnection test finished.")
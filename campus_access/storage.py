import json
from pathlib import Path

from campus_access.validation import (
    validate_fellow_id,
    validate_card_type,
    validate_request_id,
    validate_request_record,
)

_requests = []
DATA_FILE = Path("data/requests.json")


def create_request(fellow_id, card_type):
    validate_fellow_id(fellow_id)
    validate_card_type(card_type)

    next_number = max(
        (int(request["id"][1:]) for request in _requests),
        default=0,
    ) + 1

    if next_number > 999:
        raise ValueError("No more request IDs are available.")

    request = {
        "id": f"A{next_number:03d}",
        "fellow_id": fellow_id,
        "card_type": card_type,
        "status": "requested",
        "approved_by": None,
    }

    validate_request_record(request)
    _requests.append(request)

    return request.copy()


def get_request(request_id):
    validate_request_id(request_id)

    for request in _requests:
        if request["id"] == request_id:
            return request.copy()

    return None


def list_requests():
    return [request.copy() for request in _requests]


def update_request(request_id, *, status, approved_by):
    validate_request_id(request_id)

    for index, request in enumerate(_requests):
        if request["id"] == request_id:
            updated_request = request.copy()
            updated_request["status"] = status
            updated_request["approved_by"] = approved_by

            validate_request_record(updated_request)

            _requests[index] = updated_request
            return updated_request.copy()

    return None

update_request("A001", status="approved", approved_by="M01")


def save_requests(path=DATA_FILE):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(_requests, file, indent=2)

        temporary_path.replace(path)

    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def load_requests(path=DATA_FILE):
    global _requests

    path = Path(path)

    if not path.exists():
        _requests = []
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            loaded_requests = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError("The saved requests file is invalid.") from error

    if not isinstance(loaded_requests, list):
        raise ValueError("Saved requests must be a JSON list.")

    seen_ids = set()

    for request in loaded_requests:
        validate_request_record(request)

        if request["id"] in seen_ids:
            raise ValueError(f"Duplicate request ID: {request['id']}")

        seen_ids.add(request["id"])

    _requests = loaded_requests
    return list_requests()


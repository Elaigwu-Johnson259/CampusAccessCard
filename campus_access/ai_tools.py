"""Read-only tools for the CampusAccessCard Gemini assistant."""

from collections import Counter

from .storage import get_request, list_requests
from .validation import STATUSES


def lookup_request(request_id: str) -> dict:
    """Find an access-card request by its ID.

    Args:
        request_id: The request ID, such as A001.

    Returns:
        A dictionary containing the request details or a not-found message.
    """

    request_id = request_id.strip().upper()

    try:
        request = get_request(request_id)
    except ValueError:
        return {
            "found": False,
            "message": "The supplied request ID is invalid.",
        }

    if request is None:
        return {
            "found": False,
            "message": f"No request was found with ID {request_id}.",
        }

    # Return only the fields needed for ordinary status enquiries.
    return {
        "found": True,
        "id": request["id"],
        "fellow_id": request["fellow_id"],
        "card_type": request["card_type"],
        "status": request["status"],
    }


def list_requests_by_status(status: str = "") -> dict:
    """List access-card requests, optionally filtered by status.

    Args:
        status: A status such as requested, approved, issued, or returned.
                An empty string means all requests.

    Returns:
        The matching requests and their count.
    """

    status = status.strip().lower()

    if status and status not in STATUSES:
        return {
            "error": "Invalid status.",
            "valid_statuses": list(STATUSES),
        }

    requests = list_requests()

    if status:
        requests = [
            request
            for request in requests
            if request["status"] == status
        ]

    # Avoid exposing approver names when listing records.
    public_requests = [
        {
            "id": request["id"],
            "fellow_id": request["fellow_id"],
            "card_type": request["card_type"],
            "status": request["status"],
        }
        for request in requests
    ]

    return {
        "count": len(public_requests),
        "requests": public_requests,
    }


def get_request_statistics() -> dict:
    """Calculate the total requests and counts for each status.

    Returns:
        Actual request counts calculated from application storage.
    """

    requests = list_requests()

    counts = Counter(
        request["status"]
        for request in requests
    )

    return {
        "total_requests": len(requests),
        "requests_by_status": {
            status: counts.get(status, 0)
            for status in STATUSES
        },
    }

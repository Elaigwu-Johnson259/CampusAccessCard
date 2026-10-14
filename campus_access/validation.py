
"""Validation rules for campus access-card requests."""

CATEGORIES = ("visitor", "student", "staff")
STATUSES = ("requested", "approved", "issued", "returned")


def validate_fellow_id(fellow_id):
    if not isinstance(fellow_id, str) or not fellow_id.strip():
        raise ValueError("Fellow ID cannot be empty.")


def validate_card_type(card_type):
    if card_type not in CATEGORIES:
        raise ValueError("Invalid card type.")


def validate_request_id(request_id):
    if (
        not isinstance(request_id, str)
        or len(request_id) != 4
        or request_id[0] != "A"
        or not all(char in "0123456789" for char in request_id[1:])
    ):
        raise ValueError("Invalid request ID.")


def validate_request_record(request):
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")

    required_fields = {
        "id",
        "fellow_id",
        "card_type",
        "status",
        "approved_by",
    }

    if set(request.keys()) != required_fields:
        raise ValueError("Request contains missing or unexpected fields.")

    validate_request_id(request["id"])
    validate_fellow_id(request["fellow_id"])
    validate_card_type(request["card_type"])

    if request["status"] not in STATUSES:
        raise ValueError("Invalid request status.")

    approved_by = request["approved_by"]

    if approved_by is not None and (
        not isinstance(approved_by, str) or not approved_by.strip()
    ):
        raise ValueError("Invalid approver name.")

    if request["status"] in ("approved", "issued", "returned"):
        if not isinstance(approved_by, str) or not approved_by.strip():
            raise ValueError("Approved requests must have an approver.")
